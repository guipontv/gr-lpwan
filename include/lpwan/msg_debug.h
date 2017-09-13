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


#ifndef INCLUDED_LPWAN_MSG_DEBUG_H
#define INCLUDED_LPWAN_MSG_DEBUG_H

#include <lpwan/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace lpwan {

    /*!
     * \brief <+description of block+>
     * \ingroup lpwan
     *
     */
    class lpwan_API msg_debug : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<msg_debug> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of lpwan::msg_debug.
       *
       * To avoid accidental use of raw pointers, lpwan::msg_debug's
       * constructor is in a private implementation
       * class. lpwan::msg_debug::make is the public interface for
       * creating new instances.
       */
      static sptr make();

      virtual int num_messages() = 0;
      virtual pmt::pmt_t get_message(int i) = 0;
    };

  } // namespace lpwan
} // namespace gr

#endif /* INCLUDED_LPWAN_MSG_DEBUG_H */

