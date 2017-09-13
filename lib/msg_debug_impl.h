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

#ifndef INCLUDED_LPWAN_MSG_DEBUG_IMPL_H
#define INCLUDED_LPWAN_MSG_DEBUG_IMPL_H

#include <lpwan/msg_debug.h>

namespace gr {
  namespace lpwan {

      class msg_debug_impl : public msg_debug
    {
    private:

      /*!
       * \brief Messages received in this port are printed to stdout.
       *
       * This port receives messages from the scheduler's message
       * handling mechanism and prints it to stdout. This message
       * handler function is only meant to be used by the scheduler to
       * handle messages posted to port 'print'.
       *
       * \param msg A pmt message passed from the scheduler's message handling.
       */
      void print(pmt::pmt_t msg);

      /*!
       * \brief PDU formatted messages received in this port are printed to stdout.
       *
       * This port receives messages from the scheduler's message
       * handling mechanism and prints it to stdout. This message
       * handler function is only meant to be used by the scheduler to
       * handle messages posted to port 'print'.
       *
       * \param pdu A PDU message passed from the scheduler's message handling.
       */
      void print_pdu(pmt::pmt_t pdu);

      /*!
       * \brief Messages received in this port are stored in a vector.
       *
       * This port receives messages from the scheduler's message
       * handling mechanism and stores it in a vector. Messages can be
       * retrieved later using the 'get_message' function. This
       * message handler function is only meant to be used by the
       * scheduler to handle messages posted to port 'store'.
       *
       * \param msg A pmt message passed from the scheduler's message handling.
       */
      void store(pmt::pmt_t msg);

      gr::thread::mutex d_mutex;
      std::vector<pmt::pmt_t> d_messages;

    public:
      msg_debug_impl();
      ~msg_debug_impl();

      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    


      int num_messages();
      pmt::pmt_t get_message(int i);
    };

  } // namespace lpwan
} // namespace gr

#endif /* INCLUDED_LPWAN_MSG_DEBUG_IMPL_H */

