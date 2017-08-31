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

import pmt
import numpy as np
import fsk_lecim_const as cst
from gnuradio import gr

class fsk_lecim_spreading_bb(gr.interp_block):
    """
    docstring for block fsk_lecim_spreading_bb
    """
    def __init__(self, spreading = False, spreading_factor = 1, alternating = True):
        self.spreading = spreading
        self.factor = spreading_factor if self.spreading else 1
        self.alternate = alternating
        self.data_out_0 = 0
        self.data_out_1 = 1
        self.setup = 0
        gr.interp_block.__init__(self,
            name="fsk_lecim_spreading_bb",
            in_sig=[np.uint8],
            out_sig=[np.uint8], interp = self.factor)

    #Tag handler : new offset = old offset * factor
    def tag_propagation(self, ninput_items):
        self.set_tag_propagation_policy(0)
        nread = self.nitems_read(0) #number of items read on port 0
        tags = self.get_tags_in_range(0, nread, nread+ninput_items)
        key = pmt.intern("packet_len")
        if tags:
            for i in range(len(tags)):
                offset = tags[i].offset*self.factor
                value = pmt.from_long(pmt.to_long(tags[i].value)*self.factor)
                self.add_item_tag(0, offset, key, value)

    #Init : load the spreading shape only once
    def setup_1(self):
        if self.spreading:
            if self.alternate:
                self.data_out_0 = np.tile(cst.spreading_alternating_0,self.factor/2)
                self.data_out_1 = np.tile(cst.spreading_alternating_1,self.factor/2)
            else:
                if self.factor <= 4:
                    self.data_out_0 = np.tile(cst.spreading_alternating_1,self.factor/2)
                    self.data_out_1 = np.tile(cst.spreading_alternating_0,self.factor/2)
                if self.factor == 8:
                    self.data_out_0 = cst.spreading_non_alternating8_0
                    self.data_out_1 = cst.spreading_non_alternating8_1
                if self.factor == 16:
                    self.data_out_0 = cst.spreading_non_alternating16_0
                    self.data_out_1 = cst.spreading_non_alternating16_1
        self.setup = 1

    def work(self, input_items, output_items):
        
        in0 = input_items[0]
        out = output_items[0]
        
        ninput_items = len(input_items[0])
        self.tag_propagation(ninput_items)

        if(self.setup == 0):
            self.setup_1()

        for i in range(len(in0)):
            if in0[i]==0:
                for j in range(self.factor):
                    out[i*self.factor+j]=self.data_out_0[j] 
            else:
                for j in range(self.factor):
                    out[i*self.factor+j]=self.data_out_1[j]  

        return len(output_items[0])

