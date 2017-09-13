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

#include <iostream>
#include <math.h>

#include <gnuradio/io_signature.h>
#include "fsk_lecim_phr_pdu_demux_impl.h"

namespace gr {
  namespace lpwan {

    enum demux_states_t {
      STATE_SEARCH_SIGNAL,       // Wait for signal (corr_start)
      STATE_PHR,             // Copy phr
      STATE_WAIT_FOR_PHR_INFO,       // Null state (wait until msg from header demod)
      STATE_HEADER_RX_SUCCESS,  // Header processing
      STATE_HEADER_RX_FAIL,     //       "
      STATE_PDU             // Copy payload
    };

    enum out_port_indexes_t {
      PORT_PHR= 0,
      PORT_PDU = 1,
      PORT_INPUTDATA = 0
    };

    #define msg_port_id pmt::mp("phr_data")

    fsk_lecim_phr_pdu_demux::sptr
    fsk_lecim_phr_pdu_demux::make(int sps, int symbol_rate, int sf, bool output_symbols)
    {
      return gnuradio::get_initial_sptr
        (new fsk_lecim_phr_pdu_demux_impl(sps, symbol_rate, sf, output_symbols));
    }

    /*
     * The private constructor
     */
    fsk_lecim_phr_pdu_demux_impl::fsk_lecim_phr_pdu_demux_impl(int sps, int symbol_rate, int sf, bool output_symbols)
      : gr::block("fsk_lecim_phr_pdu_demux",
              gr::io_signature::make(1, 2,  (output_symbols ?  sizeof(unsigned char) : sizeof (gr_complex))),  //sizeof(gr_complex)
              gr::io_signature::make(2, 2,  (output_symbols ?  sizeof(unsigned char) : sizeof (gr_complex)))), //sizeof(gr_complex)
      d_header_len(44),
      d_sps(sps),
      d_symbol_rate(symbol_rate), // unuseful
      d_state(STATE_SEARCH_SIGNAL),
      d_phr_error(0),
      d_sf(sf),
      d_key(pmt::intern("phr_start")),
      d_len_tag_key(pmt::intern("phr_info")),
      d_output_symbols(output_symbols), //not relevant anymore
      d_itemsize(0),
      d_curr_payload_len(0),
      d_nblock(1),
      d_counter(0),
      d_counter_phr(0),
      d_counter_pdu(0),
      d_n_to_send(0)
    {
      if (d_output_symbols){
        d_itemsize = sizeof (unsigned char);
      }
      else{
        d_itemsize = sizeof (gr_complex);
        set_output_multiple(d_sps);
      }
      message_port_register_in(msg_port_id);
      set_msg_handler(msg_port_id, boost::bind(&fsk_lecim_phr_pdu_demux_impl::parse_header_data_msg, this, _1));
    }

    /*
     * Our virtual destructor.
     */
    fsk_lecim_phr_pdu_demux_impl::~fsk_lecim_phr_pdu_demux_impl()
    {
    }

    void
    fsk_lecim_phr_pdu_demux_impl::forecast (int noutput_items, gr_vector_int &ninput_items_required)
    {
      int n_items_reqd = 0;
      if (d_state == STATE_PHR) {
        n_items_reqd = d_output_symbols ? d_header_len * d_sf : d_header_len * d_sf * d_sps;
      } 
      else if (d_state == STATE_PDU) {
        n_items_reqd = d_n_to_send; //d_nblock * 72 * d_sf * d_sps;
      } 
      else {
        n_items_reqd = noutput_items ;
      }

       for (unsigned i = 0; i < ninput_items_required.size(); i++) {
         ninput_items_required[i] = n_items_reqd;
       }
    }
bool fsk_lecim_phr_pdu_demux_impl::check_buffers_ready(
        int output_items_reqd,
        int noutput_items,
        int input_items_reqd,
        gr_vector_int &ninput_items,
        int n_items_read
    ) {
      // Check there's enough space on the output buffer
      if (noutput_items < output_items_reqd) {
        return false;
      }
      // Check there's enough items on the input
      if ((ninput_items[0]-n_items_read) < input_items_reqd) {
        return false;
      }
      // All good
      return true;
    }

    int
    fsk_lecim_phr_pdu_demux_impl::general_work (int noutput_items,
                       gr_vector_int &ninput_items,
                       gr_vector_const_void_star &input_items,
                       gr_vector_void_star &output_items)
    {
      unsigned char *in = (unsigned char *) input_items[0];
      unsigned char *out_phr = (unsigned char *) output_items[PORT_PHR];
      unsigned char *out_pdu = (unsigned char *) output_items[PORT_PDU];

      const int n_input_items = ninput_items[0];
      // Items read going into general_work()
      const uint64_t n_items_read_base = nitems_read(PORT_INPUTDATA);
      // Items read during this call to general_work()
      int n_items_read = 0;      
      
      #define CONSUME_ITEMS(items_to_consume) \
          consume(PORT_INPUTDATA, items_to_consume); \
          n_items_read += (items_to_consume); \
          in += (items_to_consume)*d_itemsize;

      switch (d_state) {

        case STATE_WAIT_FOR_PHR_INFO:
          // we wait for a msg
          return 0;
        

        case STATE_SEARCH_SIGNAL: {
          //std::cout<<"WAITING FOR SIGNAL\n";
          const int max_rel_offset = n_input_items - n_items_read;

          const int signal_offset = find_signal(max_rel_offset, n_items_read_base + n_items_read,
              ((const unsigned char *) input_items[PORT_INPUTDATA]) + n_items_read);

          if (signal_offset < max_rel_offset) {
            d_state = STATE_PHR;
          }
          const int items_to_consume = signal_offset;
          CONSUME_ITEMS(items_to_consume);
          break;
        } /* case STATE_SEARCH_SIGNAL*/
        case STATE_PHR: {
          //std::cout<<"STATE_PHR "<<nitems_read(PORT_INPUTDATA)<<" no /////////////////// "<<d_phr_error<<"\n";
          if (check_buffers_ready(
                d_output_symbols ? d_header_len * d_sf : d_header_len * d_sf * d_sps, // * d_sps,
                noutput_items,
                d_output_symbols ? d_header_len * d_sf : d_header_len * d_sf * d_sps, // * d_sps,
                ninput_items,
                n_items_read)) {

            copy_n_items(
                in,
                out_phr,
                PORT_PHR,
                d_output_symbols ? d_header_len * d_sf : d_header_len * d_sf * d_sps // Number of items to copy
                );

            add_item_tag(0, d_output_symbols ? d_header_len * d_sf * d_counter_phr : d_header_len * d_sf * d_sps * d_counter_phr, 
                    pmt::intern("packet_len"), pmt::from_long(d_header_len));

            d_counter_phr += 1;
            d_state = STATE_WAIT_FOR_PHR_INFO;
          }
          break;
        } /* case STATE_PHR */
        
        case STATE_HEADER_RX_FAIL:
          //std::cout<<"Rx fail\n";
          // Actions:
          // - Consume a single item to make sure we're not deleting any other
          //   info
          CONSUME_ITEMS(1);
          d_phr_error +=1;
          if(d_phr_error > 1){
            d_phr_error = d_counter + 1;
            std::cout<<"Rx fail\n";
            d_state = STATE_SEARCH_SIGNAL;
          }
          else{
            d_state = STATE_PHR;
          }
          break;

        case STATE_HEADER_RX_SUCCESS: {
          d_counter++;
          //std::cout<<"SUCCESS no /////////////////// "<<d_phr_error<<" /// "<< d_counter <<"\n";
          //d_phr_error =0;
          const int items_to_consume = d_output_symbols ? d_header_len * d_sf : d_header_len * d_sf * d_sps; 
          CONSUME_ITEMS(items_to_consume);
          float a = (float) (8*d_curr_payload_len+6)/36; 
          d_nblock = ceil(a);
          d_n_to_send = d_output_symbols ? d_nblock * 72 * d_sf : d_nblock * 72 * d_sf * d_sps; 
          d_state = STATE_PDU;
          break;  
        }

        case STATE_PDU: {

          if (d_n_to_send == d_output_symbols ? d_nblock * 72 * d_sf : d_nblock * 72 * d_sf * d_sps){
            add_item_tag(1, d_output_symbols ? d_nblock * 72 * d_sf * d_counter_pdu : d_nblock * 72 * d_sf * d_sps * d_counter_pdu, pmt::intern("pdu_len"), pmt::from_long(d_curr_payload_len));
            add_item_tag(1, d_output_symbols ? d_nblock * 72 * d_sf * d_counter_pdu : d_nblock * 72 * d_sf * d_sps * d_counter_pdu, pmt::intern("packet_len"), pmt::from_long(72 * d_nblock));
            d_counter_pdu += 1;
          }

          // Assumptions:
          // - Input buffer is in the right spot to just start copying
          if (check_buffers_ready(d_n_to_send, noutput_items, d_n_to_send, ninput_items, n_items_read)) {

            // Write payload
            copy_n_items(in, out_pdu, PORT_PDU, d_n_to_send);

            // Consume payload
            const int items_to_consume = int(d_n_to_send);
            CONSUME_ITEMS(items_to_consume);
            //set_min_noutput_items(d_sps);
            d_state = STATE_SEARCH_SIGNAL;
          }
          else{
            if(noutput_items < d_n_to_send){
              //std::cout<<"inf\n";
              copy_n_items(in, out_pdu, PORT_PDU, noutput_items);
              const int items_to_consume = noutput_items;
              CONSUME_ITEMS(items_to_consume);
              d_n_to_send -= noutput_items;
              //std::cout<<"left to send "<< d_n_to_send<<"\n";
              d_state =  STATE_PDU;
            } 
          }
          break;
        } /* case STATE_PDU */
        
        default:
          throw std::runtime_error("invalid state");        
        } /* switch */

      return WORK_CALLED_PRODUCE;
    }

    int
    fsk_lecim_phr_pdu_demux_impl::get_n_block()
    {
      return d_nblock;
    }
    
    int
    fsk_lecim_phr_pdu_demux_impl::find_signal(
          int max_rel_offset,
          uint64_t base_offset,
          const unsigned char *in
    ) {
        int rel_offset = max_rel_offset;
        std::vector<tag_t> tags;
        get_tags_in_range(
            tags,
            PORT_INPUTDATA,
            base_offset,
            base_offset + max_rel_offset,
            d_key
        );
        if (!tags.empty() && pmt::to_double(tags[0].value)>0) {
          std::sort(tags.begin(), tags.end(), tag_t::offset_compare);
          double max = 0;
          int max_index = 0;
          for(int i = 0; i<tags.size(); i++){
            //std::cout<<"OFFSET "<<tags[i].offset<<" /// "<< pmt::to_double(tags[i].value) <<"\n";
            if(pmt::to_double(tags[i].value) > max){
              max = pmt::to_double(tags[i].value);
              max_index = i;
            }
          }

          const int tag_rel_offset = tags[max_index].offset - base_offset;
          if (tag_rel_offset < rel_offset) {
            rel_offset = tag_rel_offset;
          }
        }
      return rel_offset;
    } /* find_signal() */

    void
    fsk_lecim_phr_pdu_demux_impl::copy_n_items(
        const unsigned char *in,
        unsigned char *out,
        int port,
        int n_items)
   {
        memcpy(
             (void *) out,
             (void *) in,
             n_items * d_itemsize
        );
      const int items_to_produce = n_items;
      produce(port, items_to_produce);
    } /* copy_n_items() */

    void
    fsk_lecim_phr_pdu_demux_impl::parse_header_data_msg(pmt::pmt_t header_data)
    {
      d_state = STATE_HEADER_RX_FAIL;

      if (pmt::is_dict(header_data)) {
        pmt::pmt_t dict_items(pmt::dict_items(header_data));
        while (!pmt::is_null(dict_items)) {
          pmt::pmt_t this_item(pmt::car(dict_items));

          if (pmt::equal(pmt::car(this_item), d_len_tag_key)) {
            d_curr_payload_len = pmt::to_long(pmt::cdr(this_item));
            d_state = STATE_HEADER_RX_SUCCESS;
          }
          dict_items = pmt::cdr(dict_items);
        }
        if (d_state == STATE_HEADER_RX_FAIL) {
          //GR_LOG_CRIT(d_logger, "no payload length passed from header data");
          std::cout<<"Msg 1\n";
        }
      } 
      else if (header_data == pmt::PMT_F || pmt::is_null(header_data)) {
        //GR_LOG_INFO(d_logger, boost::format("Parser returned %1%") % pmt::write_string(header_data));
        std::cout<<"Msg 2\n";
        d_state = STATE_HEADER_RX_FAIL;
      } 
      else {
        //GR_LOG_ALERT(d_logger, boost::format("Received illegal header data (%1%)") % pmt::write_string(header_data));
        std::cout<<"Msg 3\n";
        d_state = STATE_HEADER_RX_FAIL;
      }

      if (d_state == STATE_HEADER_RX_SUCCESS)
      {
        if (d_curr_payload_len < 0 || d_curr_payload_len != 32) {
          //GR_LOG_WARN(d_logger, boost::format("Detected a packet larger than max frame size (%1% symbols)") % d_curr_payload_len);
          d_curr_payload_len = 0;
          d_state = STATE_HEADER_RX_FAIL;
          //std::cout<<"Msg 4\n";
        }
        if ( (d_output_symbols ? d_curr_payload_len * 8 * d_sf :d_curr_payload_len * 8 * d_sf * d_sps ) > max_output_buffer(1)/2) {

          d_state = STATE_HEADER_RX_FAIL;
          std::cout<<"Msg 5\n";
          //GR_LOG_INFO(d_logger, boost::format("Detected a packet larger than max frame size (%1% symbols)") % d_curr_payload_len);
        } 
        else {
          set_min_noutput_items(d_output_symbols ? d_curr_payload_len * 8 * d_sf :d_curr_payload_len * 8 * d_sf * d_sps);
        }
      }
    } /* parse_header_data_msg() */


  } /* namespace lpwan */
} /* namespace gr */

