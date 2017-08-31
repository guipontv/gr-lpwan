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
import fsk_lecim_const as cst
import numpy as np
from cmath import exp, pi
from gnuradio import gr

class fsk_lecim_time_synchronizer_cc(gr.sync_block):
    """
    docstring for block fsk_lecim_time_synchronizer_cc
    """
    def __init__(self, preamble_len, sps, freq_dev, symbol_rate):
        self.sps = sps
        self.preamble_len = (preamble_len * 8 + 24) * self.sps
        self.freq_dev = freq_dev
        self.freq_off = 0
        self.symbol_rate = symbol_rate
        self.delay = 0
        self.SFD = cst.SFD
        self.hist_len = (len(self.SFD)+1)*2
        self.corr_start_detected = False
        self.key_0 = pmt.intern("phr_start")
        self.key_1 = pmt.intern("SFD_start")
        gr.sync_block.__init__(self,
            name="fsk_lecim_time_synchronizer_cc",
            in_sig=[np.complex64],
            out_sig=[np.complex64])

    def tag_handler(self, ninput_items):
        nread = self.nitems_read(0) #number of items read on port 0
        tags = self.get_tags_in_range(0, nread, nread+ninput_items)
        key_0 = pmt.intern("corr_start")
        key_1 = pmt.intern("freq_est")
        if tags:
            for i in range(len(tags)):
                if (pmt.eq(key_0, tags[i].key)):
                    offset = tags[i].offset
                    self.delay = offset % self.sps
                    self.corr_start_detected = True
                if (pmt.eq(key_1, tags[i].key)):
                    self.freq_off = -float(pmt.to_double(tags[i].value))

    def fsk_demodulator(self, in0):
        Z = [0, 0, 0, 0]
        iterable = (exp(1j*2*pi*(self.freq_dev+self.freq_off)*i/(self.sps*self.symbol_rate)) for i in range(len(in0)))
        sine  = np.fromiter(iterable, np.complex64)
        sineconj = np.conj(sine)
        A = np.array([in0 * sine, in0 * sineconj])
        inter = np.zeros((int(len(in0)/2),), dtype=int)

        for k in range(int(len(in0)/2)):
            sum0 = np.array([np.sum(A[0][k*self.sps+self.delay:(k+1)*self.sps+self.delay]),
                        np.sum(A[1][k*self.sps+self.delay:(k+1)*self.sps+self.delay])])
            Z = abs(sum0)**2

            if Z[0] - Z[1] >= 0: #Z0-Z1 Threshold 0
                inter[k] = 0
            else:
                inter[k] = 1

        for k in range(int(len(in0)/2)-len(self.SFD)):
            corr  = np.dot(self.SFD,inter[k:k+len(self.SFD)])
            
            if corr == 13:
                print "time sync done "
                a = (self.nitems_read(0)/2.0)+k
                self.add_item_tag(0, self.nitems_read(0) + (k +len(self.SFD)) * self.sps + 1, 
                                    self.key_0,  pmt.from_long(int(a)))
                self.add_item_tag(0, self.nitems_read(0) + k  * self.sps + 1, 
                                    self.key_1,  pmt.from_long(int(a)))
                self.corr_start_detected = False
                break
            

    def work(self, input_items, output_items):

        self.set_history(self.hist_len)
        self.set_output_multiple(self.sps)
        in0 = input_items[0]
        out = output_items[0]
        
        ninput_items = len(input_items[0])
        self.tag_handler(ninput_items)
        if(self.corr_start_detected):
            self.fsk_demodulator(in0)
            # if(self.corr_start_detected):
            #     self.delay=self.delay+1
            #     print "2E round"
            #     self.fsk_demodulator(in0)
        for k in range(self.hist_len,len(in0)): #range(self.hist_len,len(in0)):
            out[k-self.hist_len] = in0[k-self.hist_len]
        return len(output_items[0])

