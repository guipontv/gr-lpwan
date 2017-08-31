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

from cmath import exp, pi
import numpy as np
from gnuradio import gr

class fsk_lecim_correlator_ccc(gr.sync_block):
    """
    docstring for block fsk_lecim_correlator_ccc
    """
    def __init__(self, sps, freq_dev, symbol_rate):
        self.sps = sps
        self.freq_dev = freq_dev
        self.symbol_rate = symbol_rate
        gr.sync_block.__init__(self,
            name="fsk_lecim_correlator_ccc",
            in_sig=[np.complex64],
            out_sig=[np.complex64, np.complex64])

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out0 = output_items[0]
        out1 = output_items[1]
        # <+signal processing here+>
        for i in range(len(in0)):
            out0[i] = in0[i]*exp(1j*2*pi*self.freq_dev*i/(self.sps*self.symbol_rate))
            out1[i] = in0[i]*exp(1j*-2*pi*self.freq_dev*i/(self.sps*self.symbol_rate))
        return len(output_items[0])

