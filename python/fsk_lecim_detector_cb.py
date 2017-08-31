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

import pmt
import numpy as np
from gnuradio import gr

class fsk_lecim_detector_cb(gr.basic_block):
    """
    docstring for block fsk_lecim_detector_cb
    """
    def __init__(self, PFSK, sps):
        self.PFSK = PFSK
        self.sps = sps
        self.delay = 0
        gr.basic_block.__init__(self,
            name="fsk_lecim_detector_cb",
            in_sig=[np.complex64, np.complex64],
            out_sig=[np.uint8])

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = (noutput_items+1)*self.sps
        self.set_output_multiple(2)

    def tag_handler(self, ninput_items):
        self.set_tag_propagation_policy(0)
        nread = self.nitems_read(0) #number of items read on port 0
        tags = self.get_tags_in_range(0, nread, nread+ninput_items)
        key = pmt.intern("phr_start")
        if tags:
            for i in range(len(tags)):
                if (pmt.eq(key, tags[i].key)):
                    offset = tags[i].offset
                    self.delay = offset % self.sps
                    offset = int(offset/self.sps)
                    value = pmt.from_double(int(pmt.to_double(tags[i].value)))
                    self.add_item_tag(0, offset, key, value)

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        out = output_items[0]

        ninput_items = len(input_items[0])

        self.tag_handler(ninput_items)

        sum0 = [0, 0]  
        Z = [0, 0, 0, 0]
        delta = [0, 0]

        if self.PFSK:
            for k in range(len(out)):
                for p in range(self.sps):
                    sum0[0] += in0[self.sps*k+p+self.delay]
                    sum0[1] += in1[self.sps*k+p+self.delay]
                if (k%2) == 0:
                    Z[0]= abs(sum0[0])**2 #Z0(2k)
                    Z[1]= abs(sum0[1])**2 #Z1(2k)
                else:
                    Z[2]= abs(sum0[0])**2 #Z0(2k+1)
                    Z[3]= abs(sum0[1])**2 #Z1(2k+1)
                    
                    delta = [Z[0]+Z[1], Z[2]+Z[3]]

                    if delta[0] - delta[1] >= 0: #Position bit
                        out[k] = 0
                        if Z[0]-Z[1]>=0:
                            out[k-1] = 0
                        else:
                            out[k-1] = 1
                    else:
                        out[k] = 1
                        if Z[2]-Z[3]>=0:
                            out[k-1] = 0
                        else:
                            out[k-1] = 1
                sum0 = [0, 0]
        else:
            for k in range(len(out)):
                sum0 = [0, 0]
                for p in range(self.sps):
                    sum0[0] += in0[self.sps*k+p+self.delay]
                    sum0[1] += in1[self.sps*k+p+self.delay]
                Z[0]= abs(sum0[0])**2 #Z0
                Z[1]= abs(sum0[1])**2 #Z1
                if Z[0] - Z[1] >= 0: #Z0-Z1 Threshold 0
                    out[k] = 0
                else:
                    out[k] = 1
                    
        self.consume(0, len(out)*self.sps)
        self.produce(0, len(out))
        return -2
