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

#ifndef INCLUDED_LPWAN_FSK_LECIM_PHR_PDU_DEMUX_IMPL_H
#define INCLUDED_LPWAN_FSK_LECIM_PHR_PDU_DEMUX_IMPL_H

#include <lpwan/fsk_lecim_phr_pdu_demux.h>

namespace gr {
  namespace lpwan {

    class fsk_lecim_phr_pdu_demux_impl : public fsk_lecim_phr_pdu_demux
    {
     private:
      int d_header_len;
      int d_sps;
      int d_symbol_rate;
      int d_state;
      int d_phr_error;
      int d_sf;
      pmt::pmt_t d_key;
      pmt::pmt_t d_len_tag_key;
      bool d_output_symbols;
      size_t d_itemsize;
      int d_curr_payload_len;
      int d_counter;
      int d_counter_phr;
      int d_counter_pdu;
      int d_nblock;
      int d_n_to_send;

     public:
      //! Checks if there are enough items on the inputs and enough space on the output buffers to copy \p n_items items
      bool check_buffers_ready(
          int output_items_reqd,
          int noutput_items,
          int input_items_reqd,
          gr_vector_int &ninput_items,
          int n_items_read
      );

      //! Return N block
      int get_n_block();

      //! Message handler: Reads the result from the header demod and sets length tag (and other tags)
      void parse_header_data_msg(pmt::pmt_t header_data);

      //! Helper function that returns the rel offset of the corr start tag
      int find_signal(
          int noutput_items,
          uint64_t base_offset,
          const unsigned char *in
      );

      //! Copies n items from in to out.
      void copy_n_items(
          const unsigned char *in,
          unsigned char *out,
          int port,
          int n_items
      );

      fsk_lecim_phr_pdu_demux_impl(int sps, int symbol_rate, int sf, bool output_symbols);
      ~fsk_lecim_phr_pdu_demux_impl();

      // Where all the action really happens
      void forecast (int noutput_items, gr_vector_int &ninput_items_required);

      int general_work(int noutput_items,
           gr_vector_int &ninput_items,
           gr_vector_const_void_star &input_items,
           gr_vector_void_star &output_items);
    };

  } // namespace lpwan
} // namespace gr

#endif /* INCLUDED_LPWAN_FSK_LECIM_PHR_PDU_DEMUX_IMPL_H */

