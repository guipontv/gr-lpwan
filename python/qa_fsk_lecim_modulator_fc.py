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
from fsk_lecim_modulator_fc import fsk_lecim_modulator_fc
from cmath import exp, pi

class qa_fsk_lecim_modulator_fc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    #FSK, sps = 4, fdev = 12.5kHz, R = 25kbit/s
    def test_001_t (self):
        src_data = (-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1)
        expected_result = tuple(exp(1j*2*pi*src_data[i/4]*12500*i/(4*25000))
        						for i in range(4*len(src_data)))
        src = blocks.vector_source_f(src_data)
        mod = fsk_lecim_modulator_fc(4, 12500, 25000)
        snk = blocks.vector_sink_c()
        null_snk = blocks.null_sink(gr.sizeof_float*1)

        self.tb.connect(src, mod)
        self.tb.connect((mod,0), snk)
        self.tb.connect((mod,1), null_snk)
        self.tb.run ()

        result_data = snk.data ()
        self.assertComplexTuplesAlmostEqual(expected_result, result_data,6)

    #P-FSK, sps = 4, fdev = 12.5kHz, R = 25kbit/s
    def test_002_t (self):
        src_data = (-1,0, 0,-1, 0,1, 0,-1, 1,0, -1,0, 0,1)
        expected_result = tuple(abs(src_data[i/4])*exp(1j*2*pi*src_data[i/4]*12500*i/(4*25000))
        						for i in range(4*len(src_data)))
        src = blocks.vector_source_f(src_data)
        mod = fsk_lecim_modulator_fc(4, 12500, 25000)
        snk = blocks.vector_sink_c()
        null_snk = blocks.null_sink(gr.sizeof_float*1)

        self.tb.connect(src, mod)
        self.tb.connect((mod,0), snk)
        self.tb.connect((mod,1), null_snk)
        self.tb.run ()

        result_data = snk.data ()
        self.assertComplexTuplesAlmostEqual(expected_result, result_data,6)

if __name__ == '__main__':
    gr_unittest.run(qa_fsk_lecim_modulator_fc, "qa_fsk_lecim_modulator_fc.xml")
