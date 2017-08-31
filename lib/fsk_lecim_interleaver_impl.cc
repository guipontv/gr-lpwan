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
#include "fsk_lecim_interleaver_impl.h"
#include <math.h> 

int lambdaPhr = 4;
int lambdaPsdu = 6;
int nPhr = 44 ;
int nPsdu = 72 ;

namespace gr {
  namespace lpwan {

    fsk_lecim_interleaver::sptr
    fsk_lecim_interleaver::make(bool phr, int nBlock, std::string len_tag)
    {
      return gnuradio::get_initial_sptr
        (new fsk_lecim_interleaver_impl(phr, nBlock, len_tag));
    }

    /*
     * The private constructor
     */
    fsk_lecim_interleaver_impl::fsk_lecim_interleaver_impl(bool phr, int nBlock, std::string len_tag)
      : gr::tagged_stream_block("fsk_lecim_interleaver",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)), len_tag),
      d_phr(phr),
      d_nBlock(nBlock)

    {
    }

    /*
     * Our virtual destructor.
     */
    fsk_lecim_interleaver_impl::~fsk_lecim_interleaver_impl()
    {
    }

    int
    fsk_lecim_interleaver_impl::calculate_output_stream_length(const gr_vector_int &ninput_items)
    {
      return ninput_items[0];
    }

    int
    fsk_lecim_interleaver_impl::interleave(int k, int nDepth, int lambda)
    {
      return int((((nDepth-1-k)%lambda)*nDepth/double(lambda))+floor((nDepth-1-k)/(double(lambda))));
    }

    int
    fsk_lecim_interleaver_impl::work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char *) output_items[0];

      int nin = ninput_items[0];
      if (d_phr){
         for (int i = 0; i < nPhr; i++){
          out[interleave(i, nPhr, lambdaPhr)] = in[i];
          }
      }
      else{
        for (int i = 0; i < d_nBlock; i++){
          for(int j = 0; j < nPsdu; j++){
            out[nPsdu*i+interleave(j, nPsdu, lambdaPsdu)] = in[i*nPsdu+j];

          }
        }
      }
      //update_length_tags(nin*d_sf,0); //we update the length tag value, because the spreading block can't do it
      return nin;
    }

  } /* namespace lpwan */
} /* namespace gr */

