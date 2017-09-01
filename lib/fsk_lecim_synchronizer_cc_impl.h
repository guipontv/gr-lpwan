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

#ifndef INCLUDED_LPWAN_FSK_LECIM_SYNCHRONIZER_CC_IMPL_H
#define INCLUDED_LPWAN_FSK_LECIM_SYNCHRONIZER_CC_IMPL_H

#include <lpwan/fsk_lecim_synchronizer_cc.h>
#include <gnuradio/filter/fft_filter.h>

using namespace gr::filter;

namespace gr {
  namespace lpwan {

    class fsk_lecim_synchronizer_cc_impl : public fsk_lecim_synchronizer_cc
    {
     private:
      pmt::pmt_t d_src_id;
      std::vector<gr_complex> d_preamble;
      std::vector<gr_complex> d_preamble1;
      std::vector<gr_complex> d_preamble2;
      int d_nsamples;
      int d_sps;
      float d_threshold;
      bool d_detected;
      kernel::fft_filter_ccc *d_filter;
      kernel::fft_filter_ccc *d_filter1;
      kernel::fft_filter_ccc *d_filter2;

      gr_complex *d_doublecorr;
      gr_complex *d_doublecorr1;
      gr_complex *d_doublecorr2;
      float *d_rr;


     public:
      fsk_lecim_synchronizer_cc_impl(const std::vector<gr_complex> &preamble, int sps, float threshold);
      ~fsk_lecim_synchronizer_cc_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace lpwan
} // namespace gr

#endif /* INCLUDED_LPWAN_FSK_LECIM_SYNCHRONIZER_CC_IMPL_H */

