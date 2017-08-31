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


#ifndef INCLUDED_LPWAN_FSK_LECIM_INTERLEAVER_H
#define INCLUDED_LPWAN_FSK_LECIM_INTERLEAVER_H

#include <lpwan/api.h>
#include <gnuradio/tagged_stream_block.h>

namespace gr {
  namespace lpwan {

    /*!
     * \brief <+description of block+>
     * \ingroup lpwan
     *
     */
    class lpwan_API fsk_lecim_interleaver : virtual public gr::tagged_stream_block
    {
     public:
      typedef boost::shared_ptr<fsk_lecim_interleaver> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of lpwan::fsk_lecim_interleaver.
       *
       * To avoid accidental use of raw pointers, lpwan::fsk_lecim_interleaver's
       * constructor is in a private implementation
       * class. lpwan::fsk_lecim_interleaver::make is the public interface for
       * creating new instances.
       */
      static sptr make(bool phr, int nBlock, std::string len_tag);
    };

  } // namespace lpwan
} // namespace gr

#endif /* INCLUDED_LPWAN_FSK_LECIM_INTERLEAVER_H */

