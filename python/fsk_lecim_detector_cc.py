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
import scipy.signal as sig
from gnuradio import gr

class fsk_lecim_detector_cc(gr.sync_block):
    """
    docstring for block fsk_lecim_detector_cc
    """
    def __init__(self, preamble, sps, threshold):
        self.preamble = preamble
        self.len = len(self.preamble)
        self.sps = sps
        self.threshold = threshold
        self.key_1 = pmt.intern("corr_start")
        self.key_2 = pmt.intern("phr_start")
        self.double_corr = []
        self.detected = False
        self.delta0 = 0
        self.multi_preamble = self.preamble[0:self.len-1]*np.conj(self.preamble[1:self.len])
        self.taps = np.flipud(np.conj(self.preamble[0:self.len-1])*self.preamble[1:self.len])
        gr.sync_block.__init__(self,
            name="fsk_lecim_detector_cc",
            in_sig=[np.complex64],
            out_sig=[np.complex64, np.float32])

    def double_correlation(self, in0):
        self.delta0 = 0
        double_corr = np.zeros((abs(len(in0)-self.len),), dtype=float)
        #A = in0[0:len(in0)-1] * np.conj(in0[1:len(in0)])
        A = np.conj(in0[0:len(in0)-1]) * in0[1:len(in0)]
        double_corr = abs(sig.convolve(A, self.taps, "full", "fft"))
        for elt in double_corr:
            self.delta0 += 1
            if(elt**2>(self.len*self.len*self.threshold/4.0)) and (self.detected == False):
                print "detected"
                self.detected = True
        # for k in range(self.len,len(in0)):
        #     LD = abs(np.vdot(A[k-self.len:k-1],self.multi_preamble))**2
            # if((LD**2>self.len*self.len*self.threshold) and (self.detected == False)):
            #     self.detected = True
            # double_corr[k-self.len] = LD
        self.double_corr = double_corr
        return double_corr

    def delay_estimator(self, in0):
        likelihood_vector = np.zeros((abs(len(in0)-self.len-self.delta0),), dtype=float)
        for i in range(len(likelihood_vector)):
            likelihood_vector[i] = np.linalg.norm(in0[i+self.len:]) + 2*self.double_corr[i+self.len]
        index_local_max = np.argmax(likelihood_vector)
        local_max  = np.amax(likelihood_vector)
        self.add_item_tag(0, self.nitems_read(0) + index_local_max + self.delta0, self.key_1,  pmt.from_double(float(local_max**2)))
        self.add_item_tag(1, self.nitems_read(0) + index_local_max + self.delta0, self.key_1,  pmt.from_double(float(local_max**2)))
        self.add_item_tag(0, self.nitems_read(0) + index_local_max + self.delta0 + self.len + 48, self.key_2,  pmt.from_double(float(local_max**2)))
        self.detected = False

    def work(self, input_items, output_items):
        self.set_output_multiple(3*self.len)
        self.set_history(self.len)
        in0 = input_items[0]
        out = output_items[0]
        out1 = output_items[1]
        double_corr = self.double_correlation(in0)
        if(self.detected):
            self.delay_estimator(in0)
        for k in range(self.len,len(in0)):
            out[k-self.len] = in0[k-self.len]
            out1[k-self.len] = double_corr[k]**2
        return len(output_items[0])

