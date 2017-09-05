/* -*- c++ -*- */
/* 
 * Copyright 2017 <+YOU OR YOUR COMPANY+>.
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

#include <gnuradio/math.h>
#include <gnuradio/io_signature.h>
#include "fsk_lecim_correlation_filter_impl.h"
#include <volk/volk.h>
#include <boost/format.hpp>
#include <boost/math/special_functions/round.hpp>
#include <gnuradio/filter/pfb_arb_resampler.h>
#include <gnuradio/filter/firdes.h>

namespace gr {
  namespace lpwan {

    fsk_lecim_correlation_filter::sptr
    fsk_lecim_correlation_filter::make(const std::vector<gr_complex> &preamble, int sps, int delay)
    {
      return gnuradio::get_initial_sptr
        (new fsk_lecim_correlation_filter_impl(preamble, sps, delay));
    }

    /*
     * The private constructor
     */
    fsk_lecim_correlation_filter_impl::fsk_lecim_correlation_filter_impl(const std::vector<gr_complex> &preamble, 
                                                                          int sps, int delay)
      : gr::sync_block("fsk_lecim_correlation_filter",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(float)))
    {
      d_sps = sps;
      d_delay = delay;
      const size_t nitems = 24*1024;
      set_max_noutput_items(nitems);
      d_doublecorr = (gr_complex *) volk_malloc(sizeof(gr_complex)*nitems, volk_get_alignment());
      // Create the filter taps
      d_preamble = preamble;
      for(size_t i=0; i < d_preamble.size()-d_delay; i++) {
          d_preamble[i] = conj(d_preamble[i])*d_preamble[i+d_delay];
      }
      for(size_t i=0; i < d_delay; i++){
        d_preamble.pop_back();
      }
      std::reverse(d_preamble.begin(), d_preamble.end());
      d_filter = new kernel::fft_filter_ccc(1, d_preamble);
      set_output_multiple(d_filter->set_taps(d_preamble));
      set_history(d_preamble.size());
      declare_sample_delay(0, d_preamble.size());
      std::cout<<d_preamble.size()<<"\n";
    }

    /*
     * Our virtual destructor.
     */
    fsk_lecim_correlation_filter_impl::~fsk_lecim_correlation_filter_impl()
    {
      delete d_filter;
      volk_free(d_doublecorr);
    }

    int
    fsk_lecim_correlation_filter_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in = (const gr_complex *) input_items[0];
      float *out = (float *) output_items[0];

      unsigned int hist_len = history();

      d_filter->filter(noutput_items, in, d_doublecorr);
      volk_32fc_magnitude_32f(out, d_doublecorr, noutput_items);
      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace lpwan */
} /* namespace gr */

