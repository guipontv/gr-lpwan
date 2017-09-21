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
from cmath import exp, pi
from math import log

class fsk_lecim_freq_offset_est_cc(gr.basic_block):
    """
    docstring for block fsk_lecim_freq_offset_est_cc
    """
    def __init__(self, preamble, sps, freq_dev, symbol_rate):
        self.sps = sps
        self.freq_dev = freq_dev
        self.freq_off = 0
        self.key = pmt.intern("freq_est")
        self.offset = 0
        self.symbol_rate = symbol_rate
        self.preamble = preamble
        self.len = len(self.preamble)
        self.n_input_items = 0
        self.n_output_items = 0
        self.num = 0
        self.phase_off = 0
        self.len_out = 0
        self.n_to_produce = 0
        self.factor = 25000/float(self.symbol_rate)
        gr.basic_block.__init__(self,
            name="fsk_lecim_freq_offset_est_cc",
            in_sig=[np.complex64],
            out_sig=[np.complex64])

    def forecast(self, noutput_items, ninput_items_required):
        self.set_output_multiple(self.sps)
        #setup size of input_items[i] for work call
        if self.num == 0:
            ninput_items_required[0] = noutput_items
        if self.num == 1:
            ninput_items_required[0] = self.n_to_produce
        if self.num == 2:
            ninput_items_required[0] = self.len*4

    def wait_for_tag(self, in0):
        nread = self.nitems_read(0) #number of items read on port 0
        tags = self.get_tags_in_range(0, nread, nread+self.n_input_items)
        key = pmt.intern("corr_start")
        if tags:
            for i in range(len(tags)):
                if (pmt.eq(key, tags[i].key) and self.offset != tags[i].offset): 
                    self.offset = tags[i].offset
                    self.n_to_produce = self.offset - nread
                    self.num = 1 
                    self.len_out = 0
        else:
            self.num = 0

    def produce_until_tag(self, in0):
        self.len_out = min(self.n_output_items, self.n_input_items, self.n_to_produce)
        self.n_to_produce = self.n_to_produce - self.len_out
        if self.n_to_produce==0:
            self.num = 2
        else:
            self.num = 1

    def freq_off_estimation(self, in0):
        K = 2
        r1 = np.zeros((self.len,), dtype=complex)
        r2 = np.zeros((self.len,), dtype=complex)
        
        #transform preamble
        for j in range(int(self.len/self.sps)):
            if(j<int(self.len/4/self.sps) or j >=int(3*self.len/4/self.sps)):    
                for i in range(self.sps):
                    if j%2==0:
                        r1[self.sps*j+i] = in0[self.sps*j+i] * exp(1j*2*pi*self.freq_dev*(self.sps*j+i)/(self.sps*self.symbol_rate))#*exp(1j*4*pi*modulator.freq_dev*(sps*j+i)/(sps*modulator.symbol_rate))
                    else:
                        r1[self.sps*j+i] = in0[self.sps*j+i] * exp(-1j*2*pi*self.freq_dev*(self.sps*j+i)/(self.sps*self.symbol_rate))
            else:
                for i in range(self.sps):
                    if j%2==1:
                         r2[self.sps*j+i] = in0[self.sps*j+i] * exp(1j*6*pi*self.freq_dev*(self.sps*j+i)/(self.sps*self.symbol_rate)) #* exp(1j*4*pi*modulator.freq_dev*(sps*j+i)/(sps*modulator.symbol_rate))
                    else:
                        r2[self.sps*j+i] = in0[self.sps*j+i] * exp(1j*2*pi*self.freq_dev*(self.sps*j+i)/(self.sps*self.symbol_rate))

        # for j in range(int(self.len/self.sps)):
        #     if j%2==0:
        #         for i in range(self.sps):
        #             r1[self.sps*j+i]= in0[self.sps*j+i]*exp(-1j*2*pi*self.freq_dev*(self.sps*j+i)/(self.sps*self.symbol_rate))
        #     if j%2==1:
        #         for i in range(self.sps):
        #             r2[self.sps*j+i]= in0[self.sps*j+i]*exp(1j*2*pi*self.freq_dev*(self.sps*j+i)/(self.sps*self.symbol_rate))

        X = abs(np.fft.fft(r1, K*self.len))+abs(np.fft.fft(r2, K*self.len))
        freq = np.fft.fftfreq(K*self.len)

        maximum = 0
        maxindex = 0
        
        #coarse tuning
        for i in range(len(X)):
            if X[i]>maximum:
                maximum = X[i]
                maxindex = freq[i]
        # if(maxindex == K*self.len - 1 ):
        #     maxindex = -1
        #fine tuning 
        # if(X[maxindex-1]>0 and X[maxindex]>0 and X[maxindex+1]>0):
        #     fine = ( (log(X[maxindex-1])-log(X[maxindex+1])) / (2*( log(X[maxindex-1])+log(X[maxindex+1])-2*log(X[maxindex]) )) )
        # else:
        #     fine = 0
        indexfine =  maxindex #+ fine
        freq_off = indexfine  * self.factor * self.sps * self.symbol_rate 
        
        if(maxindex == 0 and freq_off == 0):
            freq_off = self.freq_off
        self.freq_off = freq_off

        print self.nitems_read(0), self.offset, maxindex, freq_off, self.freq_off
        self.add_item_tag(0, self.offset, self.key, pmt.from_double(self.freq_off))
        self.num = 0

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0] 
        self.n_input_items = len(input_items[0])
        self.n_output_items = len(out)
        self.len_out = min(self.n_input_items, self.n_output_items)
        options = {0 : self.wait_for_tag, 1 : self.produce_until_tag, 2 : self.freq_off_estimation,}
        options[self.num](in0)
        for i in range(self.len_out):
            out[i] = exp(-1j*2*pi*i*self.freq_off/(self.symbol_rate*self.sps))#*exp(1j*self.phase_off)
        self.phase_off = np.angle(out[-1])+2*pi*self.freq_off/(self.sps*self.symbol_rate)
        self.consume(0, self.len_out)
        self.produce(0, self.len_out)
        return -2
