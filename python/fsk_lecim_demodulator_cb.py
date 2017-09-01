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
import fsk_lecim_const as cst
import numpy as np
from cmath import exp, pi
from gnuradio import gr

class fsk_lecim_demodulator_cb(gr.basic_block):
    """
    docstring for block fsk_lecim_demodulator_cb
    """
    def __init__(self, PFSK, sps, freq_dev, symbol_rate): 
        self.PFSK = PFSK
        self.sps = sps
        self.freq_dev = freq_dev
        self.symbol_rate = symbol_rate
        self.delay = 0
        self.phase_off = 0
        gr.basic_block.__init__(self,
            name="fsk_lecim_demodulator_cb",
            in_sig=[np.complex64],
            out_sig=[np.uint8])

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        ninput_items_required[0] = (noutput_items+1)*self.sps
        #self.set_history(len(self.SFD))
        self.set_output_multiple(2)

    def tag_handler(self, ninput_items):
        self.set_tag_propagation_policy(0)
        nread = self.nitems_read(0) #number of items read on port 0
        tags = self.get_tags_in_range(0, nread, nread+ninput_items)
        key_1 = pmt.intern("corr_start")
        key_2 = pmt.intern("phr_start")
        key_4 = pmt.intern("SFD_start")
        if tags:
            for i in range(len(tags)):
                if (pmt.eq(key_1, tags[i].key)):
                    offset = tags[i].offset
                    value = pmt.from_double(float(pmt.to_double(tags[i].value)))
                    self.add_item_tag(0, offset, key_1, value)
                if (pmt.eq(key_2, tags[i].key)):
                    offset = int(tags[i].offset/self.sps)
                    value = pmt.from_double(float(pmt.to_double(tags[i].value)))
                    self.add_item_tag(0, offset, key_2, value)
                if (pmt.eq(key_4, tags[i].key)):
                    self.delay = tags[i].offset % self.sps


    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]
        ninput_items = len(input_items[0])

        self.tag_handler(ninput_items)

        Z = [0, 0, 0, 0]
        
        sine = np.array([exp(1j*2*pi*self.freq_dev*i/(self.sps*self.symbol_rate)) for i in range(len(in0))])
        self.phase_off = np.angle(sine[-1])+2*pi*self.freq_dev/(self.sps*self.symbol_rate)
        sineconj = np.conj(sine)
        A = np.array([in0 * sine, in0 * sineconj])
        if self.PFSK:
            for k in range(len(out)):
                sum0 = np.array([np.sum(A[0][k*self.sps+self.delay:(k+1)*self.sps+self.delay]),
                                np.sum(A[1][k*self.sps+self.delay:(k+1)*self.sps+self.delay])])
                if (k%2) == 1:
                    Z[0:2] = abs(sum0)**2
                else:
                    Z[2:] = abs(sum0)**2
                    
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
        else:
            for k in range(len(out)):
                sum0 = np.array([np.sum(A[0][k*self.sps+self.delay:(k+1)*self.sps+self.delay]),
                                np.sum(A[1][k*self.sps+self.delay:(k+1)*self.sps+self.delay])])
                Z = abs(sum0)**2
                if Z[0] - Z[1] >= 0: #Z0-Z1 Threshold 0
                    out[k] = 0
                else:
                    out[k] = 1


        self.consume(0, len(out)*self.sps)
        self.produce(0, len(out))
        return -2

