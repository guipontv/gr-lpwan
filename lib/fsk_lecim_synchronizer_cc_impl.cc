/* -*- c++ -*- */
/* 
 * Copyright 2017 Victor Guipont.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <gnuradio/math.h>
#include <math.h>
#include "fsk_lecim_synchronizer_cc_impl.h"
#include <volk/volk.h>
#include <boost/format.hpp>
#include <boost/math/special_functions/round.hpp>
#include <gnuradio/filter/pfb_arb_resampler.h>
#include <gnuradio/filter/firdes.h>


namespace gr {
  namespace lpwan {

    fsk_lecim_synchronizer_cc::sptr
    fsk_lecim_synchronizer_cc::make(const std::vector<gr_complex> &preamble, int sps, float threshold)
    {
      return gnuradio::get_initial_sptr
        (new fsk_lecim_synchronizer_cc_impl(preamble, sps, threshold));
    }

    /*
     * The private constructor
     */
    fsk_lecim_synchronizer_cc_impl::fsk_lecim_synchronizer_cc_impl(const std::vector<gr_complex> &preamble, 
                                                                    int sps, float threshold)
      : gr::sync_block("fsk_lecim_synchronizer_cc",
              gr::io_signature::make(4, 4, sizeof(gr_complex)),
              gr::io_signature::make2(1, 2, sizeof(gr_complex), sizeof(float))),
      d_src_id(pmt::intern(alias()))
    {
      d_sps = sps;
      d_threshold = threshold;
      const size_t nitems = 24*1024;
      set_max_noutput_items(nitems);
      d_doublecorr = (gr_complex *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      d_doublecorr1 = (gr_complex *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      d_doublecorr2 = (gr_complex *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      d_rr = (float *) volk_malloc(sizeof(float)*nitems, volk_get_alignment());

      // Create the filter taps
      d_preamble = preamble;
      d_preamble1 = preamble;
      d_preamble2 = preamble;

      for(size_t i=0; i < d_preamble.size()-1; i++) {
          d_preamble[i] = conj(d_preamble[i])*d_preamble[i+1];
      }
      d_preamble.pop_back();
      std::reverse(d_preamble.begin(), d_preamble.end());

      for(size_t i=0; i < d_preamble1.size()-2; i++) {
          d_preamble1[i] = conj(d_preamble1[i])*d_preamble1[i+2];
      }
      d_preamble1.pop_back();
      d_preamble1.pop_back();
      std::reverse(d_preamble1.begin(), d_preamble1.end());

      for(size_t i=0; i < d_preamble1.size()-3; i++) {
          d_preamble2[i] = conj(d_preamble2[i])*d_preamble2[i+3];
      }
      d_preamble2.pop_back();
      d_preamble2.pop_back();
      d_preamble2.pop_back();
      std::reverse(d_preamble2.begin(), d_preamble2.end());

      d_filter = new kernel::fft_filter_ccc(1, d_preamble);
      d_filter1 = new kernel::fft_filter_ccc(1, d_preamble1);
      d_filter2 = new kernel::fft_filter_ccc(1, d_preamble2);
      d_nsamples  = d_preamble.size();
      //d_filter->set_taps(d_preamble);//d_preamble.size();
      set_output_multiple(d_filter->set_taps(d_preamble));
      set_history(d_preamble.size()+1);
      declare_sample_delay(0, d_preamble.size());
      std::cout<<"detection threshold is "<<d_nsamples*3*d_threshold<<"\n";
    }

    /*
     * Our virtual destructor.
     */
    fsk_lecim_synchronizer_cc_impl::~fsk_lecim_synchronizer_cc_impl()
    {
      delete d_filter;
      volk_free(d_doublecorr);
      volk_free(d_doublecorr1);
      volk_free(d_doublecorr2);
      volk_free(d_rr);
    }

    int
    fsk_lecim_synchronizer_cc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      const gr_complex *in1 = (const gr_complex *) input_items[1];
      const gr_complex *in2 = (const gr_complex *) input_items[2];
      const gr_complex *in3 = (const gr_complex *) input_items[3];
      gr_complex *out = (gr_complex *) output_items[0];

      float *drr;
      if (output_items.size() > 1)
          drr = (float *) output_items[1];
      else
          drr = d_rr;

      uint16_t index_local_max = 0;
      unsigned int hist_len = history()-1;


      d_filter->filter(noutput_items, in1, d_doublecorr);
      d_filter1->filter(noutput_items, in2, d_doublecorr1);
      d_filter2->filter(noutput_items, in3, d_doublecorr2);

      //volk_32fc_magnitude_32f(d_rr, in, noutput_items);
      for(int i = 0; i<noutput_items; i++){
        drr[i] = abs(d_doublecorr[i])+abs(d_doublecorr1[i])+abs(d_doublecorr2[i]);
      }
      volk_32f_index_max_16u(&index_local_max, drr, noutput_items);

      if(drr[index_local_max]>d_nsamples*3*d_threshold){
        //std::cout<<d_rr[index_local_max]<<" "<<pow(abs(doublecorr[index_local_max]),2)<<"\n";
        //for(int i = 0; i<10; i++){
          //float result;
          //volk_32f_accumulator_s32f(&result, &d_rr[index_local_max + i - hist_len + 1], noutput_items - index_local_max - i);
          //std::cout<< i <<" "<<result + 2*abs(doublecorr[index_local_max])<<"\n";
        //}
        add_item_tag(0, nitems_written(0) + index_local_max - hist_len + 1, pmt::intern("corr_start"),
                      pmt::from_double(drr[index_local_max]), d_src_id);
        //add_item_tag(0, nitems_written(0) + index_local_max - hist_len + 1 + 1024, pmt::intern("SFD_start"),
        //              pmt::from_double(pow(d_rr[index_local_max],2)), d_src_id);
        //add_item_tag(0, nitems_written(0) + index_local_max - hist_len + 1 + 1056, pmt::intern("phr_start"),
        //              pmt::from_double(pow(d_rr[index_local_max],2)), d_src_id);
      }

      memcpy(out, &in[0], sizeof(gr_complex)*noutput_items);
      
      return noutput_items;
    }

  } /* namespace lpwan */
} /* namespace gr */

