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

class fsk_lecim_whitening_bb(gr.sync_block):
    """
    docstring for block fsk_lecim_whitening_bb
    """
    def __init__(self, whitening):
        self.white = whitening
        self.PN9 = np.ones((9, ), dtype=int)

        gr.sync_block.__init__(self,
            name="fsk_lecim_whitening_bb",
            in_sig=[np.uint8],
            out_sig=[np.uint8])

    #Tag handler : the PN9 sequence has to be reset for each packet
    def tag_handler(self, n_input_items):
        n_read = self.nitems_read(0) #number of items read on port 0
        tags = self.get_tags_in_range(0, n_read, n_read+n_input_items)
        key = pmt.intern("packet_len")
        if tags:
            for i in range(len(tags)):
                if (pmt.eq(key, tags[i].key)):
                   self.PN9 = np.ones((9, ), dtype=int)
                    
    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        self.tag_handler(len(in0))
        if self.white:
            for i in range(len(out)):
                PN9n = self.PN9[3]^self.PN9[8]
                self.PN9 = np.insert(self.PN9, 0, PN9n)
                self.PN9 = np.delete(self.PN9, 9)
                out[i] = in0[i]^self.PN9[0]
        else:
            out[:] = in0
        return len(output_items[0])

