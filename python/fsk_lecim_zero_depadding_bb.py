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
from gnuradio import gr

class fsk_lecim_zero_depadding_bb(gr.basic_block):
    """
    docstring for block fsk_lecim_zero_depadding_bb
    """
    def __init__(self):
        self.num = 0 
        self.pdu_len = 0
        self.offset_rel = 0
        self.offset_tag = 0
        self.n_input_items = 0
        gr.basic_block.__init__(self,
            name="fsk_lecim_zero_depadding_bb",
            in_sig=[np.uint8],
            out_sig=[np.uint8])

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        if self.num == 0:
            ninput_items_required[0] = noutput_items
        if self.num == 1:
            ninput_items_required[0] = self.pdu_len

    #Wait for tags, and extract the PDU length for depadding
    def wait_tags(self, in0, out):
        n_read = self.nitems_read(0) #Number of items read on port 0
        tags = self.get_tags_in_range(0, n_read, n_read+self.n_input_items)
        key = pmt.intern("pdu_len")
        if tags:
            for i in range(len(tags)):
                if (pmt.eq(key, tags[i].key)):
                    self.offset_rel = tags[i].offset - n_read 
                    self.pdu_len = pmt.to_long(tags[i].value) * 8
                    self.add_item_tag(0, self.offset_tag, key, pmt.from_long(self.pdu_len))
                    self.offset_tag = self.offset_tag + self.pdu_len
                    self.num = 1
                    break
            self.consume(0,self.offset_rel)
        else:
            self.num = 0

    #Copy the input to the output without the padding
    def copy(self, in0, out):
        for i in range(self.pdu_len):
            out[i] = in0[i]
        self.consume(0, self.pdu_len)
        self.produce(0, self.pdu_len)
        self.num = 0

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        self.set_tag_propagation_policy(0)
        #Switch case alike
        #if 0 : wait for tags
        #else : copy
        options = {0 : self.wait_tags, 1 : self.copy,}
        self.n_input_items = len(input_items[0])
        options[self.num](in0, out)
        return -2
