#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr, gr_unittest
from gnuradio import blocks
from fsk_lecim_whitening_bb import fsk_lecim_whitening_bb

class qa_fsk_lecim_whitening_bb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    #Whitening
    def test_001_t (self):
    	src_data = (0,0,0,1,1,1,0,1,1,0,1,0,0,1,0,1,0,1,0,1,1,1,0,0,0,0,1,0,0,0)
        PN9n = (0,0,0,0,1,1,1,1,0,1,1,1,0,0,0,0,1,0,1,1,0,0,1,1,0,1,1,0,1,1)
        expected_result = tuple(src_data[i]^PN9n[i] for i in range(len(src_data)))
        
        src = blocks.vector_source_b(src_data)
        white = fsk_lecim_whitening_bb(True)
        snk = blocks.vector_sink_b()

        self.tb.connect (src, white)
        self.tb.connect (white, snk)
        self.tb.run ()

        result_data = snk.data ()
        self.assertEqual (expected_result, result_data)

    #Dewhitening
    def test_002_t (self):
    	src_data = (0,0,0,1,0,0,1,0,1,1,0,1,0,1,0,1,1,1,1,0,1,1,1,1,0,1,0,0,1,1)
        PN9n = (0,0,0,0,1,1,1,1,0,1,1,1,0,0,0,0,1,0,1,1,0,0,1,1,0,1,1,0,1,1)
        expected_result = tuple(src_data[i]^PN9n[i] for i in range(len(src_data)))
        
        src = blocks.vector_source_b(src_data)
        dewhite = fsk_lecim_whitening_bb(True)
        snk = blocks.vector_sink_b()

        self.tb.connect (src, dewhite)
        self.tb.connect (dewhite, snk)
        self.tb.run ()

        result_data = snk.data ()
        self.assertEqual (expected_result, result_data)


if __name__ == '__main__':
    gr_unittest.run(qa_fsk_lecim_whitening_bb, "qa_fsk_lecim_whitening_bb.xml")
