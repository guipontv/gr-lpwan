#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 Victor Guipont.
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
from fsk_lecim_spreading_bb import fsk_lecim_spreading_bb

class qa_fsk_lecim_spreading_bb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

	# Spreading alternate, spreading factor (sf) = 8 
    def test_001_t (self):
        # set up fg
        src_data = (0,0,0,1,1,1,0)
        expected_result = (0,1,0,1,0,1,0,1, 
        					0,1,0,1,0,1,0,1, 
        					0,1,0,1,0,1,0,1, 
        					1,0,1,0,1,0,1,0, 
        					1,0,1,0,1,0,1,0, 
        					1,0,1,0,1,0,1,0, 
        					0,1,0,1,0,1,0,1)
        src = blocks.vector_source_b(src_data)
        spread = fsk_lecim_spreading_bb(True, 8, True)
        snk = blocks.vector_sink_b()

        self.tb.connect (src, spread)
        self.tb.connect (spread, snk)
        self.tb.run ()
        result_data = snk.data ()
        # check data
        self.assertEqual (expected_result, result_data)

	# Spreading non alternate, spreading factor (sf) = 4 
    def test_002_t (self):
        # set up fg
        src_data = (0,0,0,1,1,1,0)
        expected_result = (1,0,1,0,
        					1,0,1,0, 
        					1,0,1,0,
        					0,1,0,1, 
        					0,1,0,1, 
        					0,1,0,1, 
        					1,0,1,0)
        src = blocks.vector_source_b(src_data)
        spread = fsk_lecim_spreading_bb(True, 4, False)
        snk = blocks.vector_sink_b()

        self.tb.connect (src, spread)
        self.tb.connect (spread, snk)
        self.tb.run ()
        result_data = snk.data ()
        # check data
        self.assertEqual (expected_result, result_data)

    # Spreading non alternate, spreading factor (sf) = 8 
    def test_003_t (self):
        # set up fg
        src_data = (0,0,0,1,1,1,0)
        expected_result = (1,0,1,1,0,0,0,1,
        					1,0,1,1,0,0,0,1,
        					1,0,1,1,0,0,0,1,
        					0,1,0,0,1,1,1,0, 
        					0,1,0,0,1,1,1,0, 
        					0,1,0,0,1,1,1,0,
        					1,0,1,1,0,0,0,1)
        src = blocks.vector_source_b(src_data)
        spread = fsk_lecim_spreading_bb(True, 8, False)
        snk = blocks.vector_sink_b()

        self.tb.connect (src, spread)
        self.tb.connect (spread, snk)
        self.tb.run ()
        result_data = snk.data ()
        # check data
        self.assertEqual (expected_result, result_data)

    # Spreading non alternate, spreading factor (sf) = 16 
    def test_004_t (self):
        # set up fg
        src_data = (0,0,0,1,1,1,0)
        expected_result = (0,0,1,0, 0,0,1,1, 1,1,0,1, 0,1,1,0,
        					0,0,1,0, 0,0,1,1, 1,1,0,1, 0,1,1,0,
        					0,0,1,0, 0,0,1,1, 1,1,0,1, 0,1,1,0,
        					1,1,0,1, 1,1,0,0, 0,0,1,0, 1,0,0,1, 
        					1,1,0,1, 1,1,0,0, 0,0,1,0, 1,0,0,1,
        					1,1,0,1, 1,1,0,0, 0,0,1,0, 1,0,0,1,
        					0,0,1,0, 0,0,1,1, 1,1,0,1, 0,1,1,0)
        src = blocks.vector_source_b(src_data)
        spread = fsk_lecim_spreading_bb(True, 16, False)
        snk = blocks.vector_sink_b()

        self.tb.connect (src, spread)
        self.tb.connect (spread, snk)
        self.tb.run ()
        result_data = snk.data ()
        # check data
        self.assertEqual (expected_result, result_data)

if __name__ == '__main__':
    gr_unittest.run(qa_fsk_lecim_spreading_bb, "qa_fsk_lecim_spreading_bb.xml")
