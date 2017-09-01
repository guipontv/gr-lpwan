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

#ifndef INCLUDED_LPWAN_FSK_LECIM_INTERLEAVER_IMPL_H
#define INCLUDED_LPWAN_FSK_LECIM_INTERLEAVER_IMPL_H

#include <lpwan/fsk_lecim_interleaver.h>

namespace gr {
  namespace lpwan {

    class fsk_lecim_interleaver_impl : public fsk_lecim_interleaver
    {
     private:
      bool d_phr;
      int d_nBlock;

     protected:
      int calculate_output_stream_length(const gr_vector_int &ninput_items);

     public:
      fsk_lecim_interleaver_impl(bool phr, int nBlock, std::string len_tag);
      ~fsk_lecim_interleaver_impl();

      int interleave(int k, int nDepth, int lambda);
      
      // Where all the action really happens
      int work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace lpwan
} // namespace gr

#endif /* INCLUDED_LPWAN_FSK_LECIM_INTERLEAVER_IMPL_H */

