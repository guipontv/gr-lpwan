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

#include <boost/format.hpp>
#include <gnuradio/io_signature.h>
#include "fsk_lecim_phr_parser_impl.h"

#define msg_port_id     pmt::mp("phr_data")
#define key     pmt::intern("phr_info")
#define phr_len 14

namespace gr {
  namespace lpwan {

    fsk_lecim_phr_parser::sptr
    fsk_lecim_phr_parser::make(const std::string len_tag_key)
    {
      return gnuradio::get_initial_sptr
        (new fsk_lecim_phr_parser_impl(len_tag_key));
    }

    /*
     * The private constructor
     */
    fsk_lecim_phr_parser_impl::fsk_lecim_phr_parser_impl(const std::string len_tag_key)
      : gr::sync_block("fsk_lecim_phr_parser",
              gr::io_signature::make(1, 1, sizeof (unsigned char)),
              gr::io_signature::make(0, 0, 0))
    {
      message_port_register_out(msg_port_id);
      set_output_multiple(14);
    }

    /*
     * Our virtual destructor.
     */
    fsk_lecim_phr_parser_impl::~fsk_lecim_phr_parser_impl()
    {
    }

    int
    fsk_lecim_phr_parser_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const unsigned char *in = (const unsigned char *) input_items[0];
      int pdu_len = 0;
      int parity_bit = 0;
      if (noutput_items < phr_len) {
         return 0;
      }

      std::vector<tag_t> tags;
      get_tags_in_range(tags, 0,nitems_read(0),nitems_read(0)+phr_len);

      if (tags.empty()){
          //GR_LOG_INFO(d_logger, boost::format("No PHR detected"));
          message_port_pub(msg_port_id, pmt::PMT_F);
      } 

      else {
        pmt::pmt_t dict(pmt::make_dict());

        for (unsigned i = 0; i < tags.size(); i++) {

          for(int i = 0; i<phr_len-3;i++){
            pdu_len += (in[i]<<i);
          }
          parity_bit = in[0];
          for(int i = 1; i<phr_len-1;i++){
            parity_bit = parity_bit^in[i];  
          }

          if (parity_bit != in[13]){
            //GR_LOG_INFO(d_logger, boost::format("PHR : Parity bit error"));
            //message_port_pub(msg_port_id, pmt::PMT_F);
            //std::cout << "parity_bit error\n";
          }
          dict = pmt::dict_add(dict, key, pmt::from_long(pdu_len));
          
        }
        message_port_pub(msg_port_id, dict);
      }
      return phr_len;
    }

  } /* namespace lpwan */
} /* namespace gr */

