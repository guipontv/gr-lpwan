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

import fsk_lecim_const as cst
import numpy as np
from gnuradio import gr

class fsk_lecim_SFD_corr_bb(gr.basic_block):
    """
    docstring for block fsk_lecim_SFD_corr_bb
    """
    def __init__(self):
        self.SFD = cst.SFD
        gr.basic_block.__init__(self,
            name="fsk_lecim_SFD_corr_bb",
            in_sig=[np.complex64],
            out_sig=[np.complex64])

    def forecast(self, noutput_items, ninput_items_required):
            ninput_items_required[0] = len(self.SFD)

    def general_work(self, input_items, output_items):
        np.vdot(self.SFD)
        output_items[0][:] = input_items[0]
        consume(0, len(input_items[0]))
        #self.consume_each(len(input_items[0]))
        return len(output_items[0])
