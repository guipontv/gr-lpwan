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
#include "fsk_lecim_deinterleaver_impl.h"
#include <math.h> 

int lambdaPhr1 = 4;
int lambdaPsdu1 = 6;
int nPhr1 = 44;
int nPsdu1 = 72;

namespace gr {
  namespace lpwan {

    fsk_lecim_deinterleaver::sptr
    fsk_lecim_deinterleaver::make(bool phr, int nBlock, std::string len_tag)
    {
      return gnuradio::get_initial_sptr
        (new fsk_lecim_deinterleaver_impl(phr, nBlock, len_tag));
    }

    /*
     * The private constructor
     */
    fsk_lecim_deinterleaver_impl::fsk_lecim_deinterleaver_impl(bool phr, int nBlock, std::string len_tag)
      : gr::tagged_stream_block("fsk_lecim_deinterleaver",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)), len_tag),
      d_phr(phr),
      d_nBlock(nBlock)
    {}

    /*
     * Our virtual destructor.
     */
    fsk_lecim_deinterleaver_impl::~fsk_lecim_deinterleaver_impl()
    {
    }

    int
    fsk_lecim_deinterleaver_impl::calculate_output_stream_length(const gr_vector_int &ninput_items)
    {
      return ninput_items[0];
    }

    int
    fsk_lecim_deinterleaver_impl::deinterleave(int k, int nDepth, int lambda)
    {
      return int((nDepth-1-k)*lambda-(nDepth-1)*floor((nDepth-1-k)*lambda/double(nDepth)));
    }

    int
    fsk_lecim_deinterleaver_impl::work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];

      int nin = ninput_items[0];
      if (d_phr){
         for (int i = 0; i < nPhr1; i++){
          out[deinterleave(i, nPhr1, lambdaPhr1)] = in[i];
          }
      }
      else{
              for (int i = 0; i < d_nBlock; i++){
                        for(int j = 0; j < nPsdu1; j++){
                          out[nPsdu1*i+deinterleave(j, nPsdu1, lambdaPsdu1)] = in[i*nPsdu1+j];
                        }
              }
      }
      return nin;
    }

  } /* namespace lpwan */
} /* namespace gr */

