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

#ifndef INCLUDED_LPWAN_FSK_LECIM_CORR_EST_CC_IMPL_H
#define INCLUDED_LPWAN_FSK_LECIM_CORR_EST_CC_IMPL_H

#include <lpwan/fsk_lecim_corr_est_cc.h>
#include <gnuradio/filter/fft_filter.h>

using namespace gr::filter;

namespace gr {
  namespace lpwan {

    class fsk_lecim_corr_est_cc_impl : public fsk_lecim_corr_est_cc
    {
     private:
      pmt::pmt_t d_src_id;
      std::vector<gr_complex> d_symbols;
      int d_nsamples;
      int d_sps;
      int d_ctr;
      unsigned int d_mark_delay, d_stashed_mark_delay;
      float d_thresh, d_stashed_threshold;
      kernel::fft_filter_ccc *d_filter;

      gr_complex *d_ss;
      gr_complex *d_rr;
      gr_complex *d_doublecorr;
      gr_complex *d_corr;
      float *d_phicorrection;
      gr_complex *d_fcorrection;
      float *d_corr_mag;

      void _set_mark_delay(unsigned int mark_delay);
      void _set_threshold(float threshold);

     public:
      fsk_lecim_corr_est_cc_impl(const std::vector<gr_complex> &symbols,
                       int sps, unsigned int mark_delay,
                       float threshold=0.9);
      ~fsk_lecim_corr_est_cc_impl();

      std::vector<gr_complex> symbols() const;

      unsigned int mark_delay() const;
      void set_mark_delay(unsigned int mark_delay);

      void set_threshold(float threshold);

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace lpwan
} // namespace gr

#endif /* INCLUDED_LPWAN_FSK_LECIM_CORR_EST_CC_IMPL_H */

