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

#include <math.h>   
#include <gnuradio/io_signature.h>
#include "fsk_lecim_normalize_fcc_impl.h"

namespace gr {
  namespace lpwan {

    fsk_lecim_normalize_fcc::sptr
    fsk_lecim_normalize_fcc::make()
    {
      return gnuradio::get_initial_sptr
        (new fsk_lecim_normalize_fcc_impl());
    }

    /*
     * The private constructor
     This block divide the signal by the local standard deviation 
     */
    fsk_lecim_normalize_fcc_impl::fsk_lecim_normalize_fcc_impl()
      : gr::sync_block("fsk_lecim_normalize_fcc",
              gr::io_signature::make2(2, 2, sizeof(gr_complex), sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
      d_noise = 0;
    }

    /*
     * Our virtual destructor.
     */
    fsk_lecim_normalize_fcc_impl::~fsk_lecim_normalize_fcc_impl()
    {
    }

    int
    fsk_lecim_normalize_fcc_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in0 = (const gr_complex *) input_items[0];
      const float *in1 = (const float *) input_items[1];
      gr_complex *out = (gr_complex *) output_items[0];
      float factor = 1;
      for(int i = 0; i<noutput_items; i++){

        if(in1[i]>0.000005){
        factor = sqrt(in1[i]-d_noise);
        }
        else{
          d_noise = in1[i] ;
        }
        out[i] = in0[i]/factor;
        float factor = 1;
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace lpwan */
} /* namespace gr */

