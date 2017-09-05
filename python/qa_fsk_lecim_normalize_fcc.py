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
import lpwan_swig as lpwan
from cmath import exp, pi
import numpy as np

class qa_fsk_lecim_normalize_by_fcc (gr_unittest.TestCase):

    def setUp (self):
        self.tb = gr.top_block ()

    def tearDown (self):
        self.tb = None

    def test_001_t (self):
        data = (-1,-1,-1,1,1,1,-1,1,-1,-1,-1,1,1,1)
        src_data_1 = tuple(0.25*exp(1j*2*pi*data[i/4]*12500*i/(4*25000)) for i in range(4*len(data)))
        src_data_2 = (np.var(src_data_1) for i in range(4*len(data)))
        expected_result = src_data_1/np.sqrt(np.var(src_data_1))

        src_1 = blocks.vector_source_c(src_data_1)
        src_2 = blocks.vector_source_f(src_data_2)
        norm = fsk_lecim_normalize_by_fcc()
        snk = blocks.vector_sink_c()

        self.tb.connect(src_1, (norm, 0))
        self.tb.connect(src_2, (norm, 1))
        self.tb.connect(norm, snk)
        self.tb.run ()

        result_data = snk.data ()
        self.assertComplexTuplesAlmostEqual(expected_result, result_data,6)


if __name__ == '__main__':
    gr_unittest.run(qa_fsk_lecim_normalize_by_fcc, "qa_fsk_lecim_normalize_by_fcc.xml")
