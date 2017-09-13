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

import numpy as np
from gnuradio import gr

class iterator(gr.sync_block):
    """
    docstring for block iterator
    """
    def __init__(self, block_for = 0, max0 = 10):
        self.iterator = 0
        self.counter = 0
        self.block_for = block_for
        self.num = max0
        self.produced = 0
        gr.sync_block.__init__(self,
            name="iterator",
            in_sig=None,
            out_sig=[np.uint8])


    def work(self, input_items, output_items):
        out = output_items[0]
        for i in range(len(out)):
            self.iterator +=1
            out[i] = self.iterator
        return len(out)
        # if(self.produced+len(out)<self.num):
        #     print "case 1"
        #     for i in range(len(out)):
        #         if(self.counter<self.block_for):
        #             self.counter += 1
        #         else:
        #             self.iterator += 1
        #             self.counter = 1
        #         out[i] = self.iterator
        #         self.produced += 1
        #     return len(out)
        # elif(self.produced >= self.num):
        #     print "case 2"
        #     return -1
        # else:
        #     print "case 3"
        #     for i in range(self.num-self.produced):
        #         if(self.counter<self.block_for):
        #             self.counter += 1
        #         else:
        #             self.iterator += 1
        #             self.counter = 1
        #         out[i] = self.iterator
        #         self.produced += 1
        #     return self.num-self.produced
        

