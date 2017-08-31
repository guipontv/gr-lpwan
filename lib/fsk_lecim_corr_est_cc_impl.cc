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
#include "fsk_lecim_corr_est_cc_impl.h"
#include <volk/volk.h>
#include <boost/format.hpp>
#include <boost/math/special_functions/round.hpp>
#include <gnuradio/filter/pfb_arb_resampler.h>
#include <gnuradio/filter/firdes.h>


namespace gr {
  namespace lpwan {

    fsk_lecim_corr_est_cc::sptr
    fsk_lecim_corr_est_cc::make(const std::vector<gr_complex> &symbols, 
                                int sps, unsigned int mark_delay,
                                float threshold)
    {
      return gnuradio::get_initial_sptr
        (new fsk_lecim_corr_est_cc_impl(symbols, sps, mark_delay, threshold));
    }

    /*
     * The private constructor
     */
    fsk_lecim_corr_est_cc_impl::fsk_lecim_corr_est_cc_impl(const std::vector<gr_complex> &symbols,
                                                            int sps, unsigned int mark_delay,
                                                            float threshold)
      : gr::sync_block("fsk_lecim_corr_est_cc",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 2, sizeof(gr_complex))),
      d_src_id(pmt::intern(alias()))
    {
      d_sps = sps;
      d_thresh = threshold;
      const size_t nitems = 24*1024;
      set_max_noutput_items(nitems);
      d_corr = (gr_complex *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      d_phicorrection = (float *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      d_fcorrection = (gr_complex *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      d_corr_mag = (float *) volk_malloc(sizeof(float)*nitems, volk_get_alignment());

      d_ss = (gr_complex *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      d_rr = (gr_complex *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      d_doublecorr = (gr_complex *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      // Create time-reversed conjugate of symbols
      d_symbols = symbols;

      for(size_t i=0; i < d_symbols.size(); i++) {
          d_symbols[i] = conj(d_symbols[i]);
      }
      std::reverse(d_symbols.begin(), d_symbols.end());

      // Correlation filter
      d_filter = new kernel::fft_filter_ccc(1, d_symbols);

      d_nsamples  = d_filter->ntaps();
      set_output_multiple(d_filter->set_taps(d_symbols));

      //volk_8ic_x2_s32f_multiply_conjugate_32fc(d_ss, &symbols[1],&symbols[0], 1, d_nsamples-1);

      //set_tag_propagation_policy(TPP_DONT);
      set_history(d_symbols.size()+1);
      declare_sample_delay(1, 0);
      declare_sample_delay(0, d_symbols.size());
      std::cout<<" corr threshold is "<<d_nsamples*d_nsamples*d_thresh<<"\n";
    }

    /*
     * Our virtual destructor.
     */
    fsk_lecim_corr_est_cc_impl::~fsk_lecim_corr_est_cc_impl()
    {      
      delete d_filter;
      volk_free(d_corr);
      volk_free(d_corr_mag);
      volk_free(d_phicorrection);
      volk_free(d_fcorrection);
    }

    int
    fsk_lecim_corr_est_cc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      gr::thread::scoped_lock lock(d_setlock);

      const gr_complex *in = (gr_complex *)input_items[0];
      gr_complex *out = (gr_complex*)output_items[0];
      gr_complex *corr;
      if (output_items.size() > 1)
          corr = (gr_complex *) output_items[1];
      else
          corr = d_corr;

      // Our correlation filter length
      unsigned int hist_len = history() - 1;
      //volk_32fc_s32f_atan2_32f(d_phicorrection, &in[hist_len], 1/(2*M_PI), noutput_items);

      // for(int i = 0; i<noutput_items;i++){
      //   d_fcorrection[i] = lv_cmake(d_phicorrection[i], d_phicorrection[i]) ;
      // }

      // volk_32fc_x2_multiply_32fc(d_rr, d_fcorrection, &in[hist_len], noutput_items);

      d_filter->filter(noutput_items,  in, corr);

      // Find the magnitude squared of the correlation
      volk_32fc_magnitude_squared_32f(&d_corr_mag[0], corr, noutput_items);

      uint16_t local_max_index = 0;
      volk_32f_index_max_16u_a(&local_max_index, d_corr_mag, noutput_items);


      float corr_mag = d_corr_mag[local_max_index];
      if(corr_mag >= d_thresh * d_nsamples*d_nsamples){
          add_item_tag(0, nitems_written(0) + local_max_index + 1 - 48, pmt::intern("SFD_start"),
                       pmt::from_double(d_corr_mag[local_max_index]), d_src_id);
          add_item_tag(0, nitems_written(0) + local_max_index + 1, pmt::intern("phr_start"),
                       pmt::from_double(d_corr_mag[local_max_index]), d_src_id);

        }

      // Delay the output by our correlation filter length so we can
      // tag backwards in time
      memcpy(out, &in[0], sizeof(gr_complex)*noutput_items);

      return noutput_items;
    }

  } /* namespace lpwan */
} /* namespace gr */

