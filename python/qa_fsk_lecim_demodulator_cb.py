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
from fsk_lecim_demodulator_cb import fsk_lecim_demodulator_cb
from cmath import exp, pi

class qa_fsk_lecim_demodulator_cb (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    #FSK, sps = 4, fdev = 12.5kHz, R = 25kbit/s
    def test_001_t (self):
        src_data_mapped = (0,-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1,1,1,1,1)
        src_data = tuple(exp(1j*2*pi*src_data_mapped[i/4]*12500*i/(4*25000))
        						for i in range(4*len(src_data_mapped)))
        expected_result =(0,0,0,0,1,1,1,0,1,0,0,0,1,1,1,1,1,1,1)

        src = blocks.vector_source_c(src_data)
        demod = fsk_lecim_demodulator_cb(False, 4, 12500, 25000)
        snk = blocks.vector_sink_b()

        self.tb.connect(src, demod)
        self.tb.connect(demod, snk)
        self.tb.run ()

        result_data = snk.data ()
        self.assertEqual(expected_result[:-1], result_data)

    #P-FSK, sps = 4, fdev = 12.5kHz, R = 25kbit/s
    def test_002_t (self):
        src_data_mapped = (0, 0,0,-1,0, 0,-1, 0,1, 0,-1, 1,0, -1,0, 0,1)
        src_data = tuple(abs(src_data_mapped[i/4])*exp(1j*2*pi*src_data_mapped[i/4]*12500*i/(4*25000))
        						for i in range(4*len(src_data_mapped)))
        expected_result = (0,0, 0,1, 1,1, 0,1, 1,0, 0,0, 1,1)

        src = blocks.vector_source_c(src_data)
        demod = fsk_lecim_demodulator_cb(True, 4, 12500, 25000)
        snk = blocks.vector_sink_b()

        self.tb.connect(src, demod)
        self.tb.connect(demod, snk)
        self.tb.run()

        result_data = snk.data()
        self.assertEqual(expected_result[:-2], result_data[3:-1])


if __name__ == '__main__':
    gr_unittest.run(qa_fsk_lecim_demodulator_cb, "qa_fsk_lecim_demodulator_cb.xml")
