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

#ifndef INCLUDED_LPWAN_FSK_LECIM_CORRELATION_FILTER_IMPL_H
#define INCLUDED_LPWAN_FSK_LECIM_CORRELATION_FILTER_IMPL_H

#include <lpwan/fsk_lecim_correlation_filter.h>
#include <gnuradio/filter/fft_filter.h>

using namespace gr::filter;

namespace gr {
  namespace lpwan {

    class fsk_lecim_correlation_filter_impl : public fsk_lecim_correlation_filter
    {
     private:
      std::vector<gr_complex> d_preamble;
      int d_sps;
      int d_delay;
      kernel::fft_filter_ccc *d_filter;
      gr_complex *d_doublecorr;

     public:
      fsk_lecim_correlation_filter_impl(const std::vector<gr_complex> &preamble, int sps, int delay);
      ~fsk_lecim_correlation_filter_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace lpwan
} // namespace gr

#endif /* INCLUDED_LPWAN_FSK_LECIM_CORRELATION_FILTER_IMPL_H */

