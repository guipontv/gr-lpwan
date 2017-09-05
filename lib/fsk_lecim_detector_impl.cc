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

#include <gnuradio/io_signature.h>
#include "fsk_lecim_detector_impl.h"
#include <volk/volk.h>

namespace gr {
  namespace lpwan {

    fsk_lecim_detector::sptr
    fsk_lecim_detector::make(int len_preamble, int delay, float threshold)
    {
      return gnuradio::get_initial_sptr
        (new fsk_lecim_detector_impl(len_preamble, delay, threshold));
    }

    /*
     * The private constructor
     */
    fsk_lecim_detector_impl::fsk_lecim_detector_impl(int len_preamble, int delay, float threshold)
      : gr::sync_block("fsk_lecim_detector",
              gr::io_signature::make2(2, 2, sizeof(gr_complex), sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_src_id(pmt::intern(alias()))
    {
      d_len = len_preamble;
      d_delay = delay;
      d_threshold = 0;
      for(int i=1;i<=d_delay;i++){
        d_threshold += d_len - i;
      }
     d_threshold *= threshold;
      set_output_multiple(d_len*4);
      std::cout<<"detection threshold is "<<d_threshold<<"\n";
    }

    /*
     * Our virtual destructor.
     */
    fsk_lecim_detector_impl::~fsk_lecim_detector_impl()
    {
    }

    int
    fsk_lecim_detector_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const gr_complex *in0 = (const gr_complex *) input_items[0];
      const float *in1 = (const float *) input_items[1];
      gr_complex *out = (gr_complex *) output_items[0];

      uint16_t index_local_max = 0;
      volk_32f_index_max_16u(&index_local_max, in1, noutput_items);

      if(in1[index_local_max]>=d_threshold){

        add_item_tag(0, nitems_read(0) + index_local_max, pmt::intern("corr_start"),
                      pmt::from_double(in1[index_local_max]), d_src_id);
      }
      memcpy(out, in0, sizeof(gr_complex)*noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace lpwan */
} /* namespace gr */

