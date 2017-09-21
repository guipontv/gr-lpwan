#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Thu Sep 21 11:18:15 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from lpwan_lecim_fsk_phy import lpwan_lecim_fsk_phy  # grc-generated hier_block
from optparse import OptionParser
import foo
import lpwan
import pmt


class top_block(gr.top_block):

    def __init__(self, corr_threshold=0.9, det_threshold=0.9, freq_off=0, index=0.5, noise=0.2, pdu_len=28, resampling=1, sps=2, PFSK=0):
        gr.top_block.__init__(self, "Top Block")

        ##################################################
        # Parameters
        ##################################################
        self.corr_threshold = corr_threshold
        self.det_threshold = det_threshold
        self.freq_off = freq_off
        self.index = index
        self.noise = noise
        self.pdu_len = pdu_len
        self.resampling = resampling
        self.sps = sps
        self.PFSK = PFSK

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_2 = samp_rate_2 = 37500
        self.samp_rate_1 = samp_rate_1 = 25000
        self.samp_rate_0 = samp_rate_0 = 12500

        ##################################################
        # Blocks
        ##################################################
        self.lpwan_message_counter_0_0_0_0_2 = lpwan.message_counter(0, 1, False)
        self.lpwan_message_counter_0_0_0_0_0 = lpwan.message_counter(0, 1, False)
        self.lpwan_lecim_fsk_phy_0 = lpwan_lecim_fsk_phy(
            band=False,
            burst_tag="burst",
            data_whitening=False,
            fcs=False,
            index=index,
            pdu_len=pdu_len+4,
            pfsk=1,
            preamble_len=64,
            resampling=resampling,
            spreading=True,
            spreading_alternating=False,
            spreading_factor=2,
            sps=sps,
            threshold_0=0.6,
            threshold_1=0.6,
        )
        self.foo_periodic_msg_source_0 = foo.periodic_msg_source(pmt.intern("generate"), 500, 500, False, False)
        self.digital_crc32_async_bb_1 = digital.crc32_async_bb(True)
        self.digital_crc32_async_bb_0 = digital.crc32_async_bb(False)
        self.blocks_vector_sink_x_1 = blocks.vector_sink_f(1)
        self.blocks_vector_sink_x_0 = blocks.vector_sink_f(1)
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate_1*sps*resampling,True)
        self.blocks_random_pdu_0 = blocks.random_pdu(pdu_len, pdu_len, chr(0xFF), 1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.analog_noise_source_x_0 = analog.noise_source_c(analog.GR_GAUSSIAN, noise, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.digital_crc32_async_bb_0, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.lpwan_lecim_fsk_phy_0, 'in_tx'))
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.lpwan_message_counter_0_0_0_0_0, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self.lpwan_message_counter_0_0_0_0_2, 'in'))
        self.msg_connect((self.foo_periodic_msg_source_0, 'out'), (self.blocks_random_pdu_0, 'generate'))
        self.msg_connect((self.lpwan_lecim_fsk_phy_0, 'out_rx'), (self.digital_crc32_async_bb_1, 'in'))
        self.connect((self.analog_noise_source_x_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.lpwan_lecim_fsk_phy_0, 0))
        self.connect((self.lpwan_lecim_fsk_phy_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.lpwan_message_counter_0_0_0_0_0, 0), (self.blocks_vector_sink_x_0, 0))
        self.connect((self.lpwan_message_counter_0_0_0_0_2, 0), (self.blocks_vector_sink_x_1, 0))

    def get_corr_threshold(self):
        return self.corr_threshold

    def set_corr_threshold(self, corr_threshold):
        self.corr_threshold = corr_threshold

    def get_det_threshold(self):
        return self.det_threshold

    def set_det_threshold(self, det_threshold):
        self.det_threshold = det_threshold

    def get_freq_off(self):
        return self.freq_off

    def set_freq_off(self, freq_off):
        self.freq_off = freq_off

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
        self.lpwan_lecim_fsk_phy_0.set_index(self.index)

    def get_noise(self):
        return self.noise

    def set_noise(self, noise):
        self.noise = noise
        self.analog_noise_source_x_0.set_amplitude(self.noise)

    def get_pdu_len(self):
        return self.pdu_len

    def set_pdu_len(self, pdu_len):
        self.pdu_len = pdu_len
        self.lpwan_lecim_fsk_phy_0.set_pdu_len(self.pdu_len+4)

    def get_resampling(self):
        return self.resampling

    def set_resampling(self, resampling):
        self.resampling = resampling
        self.lpwan_lecim_fsk_phy_0.set_resampling(self.resampling)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate_1*self.sps*self.resampling)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.lpwan_lecim_fsk_phy_0.set_sps(self.sps)
        self.blocks_throttle_0.set_sample_rate(self.samp_rate_1*self.sps*self.resampling)

    def get_PFSK(self):
        return self.PFSK

    def set_PFSK(self, PFSK):
        self.PFSK = PFSK

    def get_samp_rate_2(self):
        return self.samp_rate_2

    def set_samp_rate_2(self, samp_rate_2):
        self.samp_rate_2 = samp_rate_2

    def get_samp_rate_1(self):
        return self.samp_rate_1

    def set_samp_rate_1(self, samp_rate_1):
        self.samp_rate_1 = samp_rate_1
        self.blocks_throttle_0.set_sample_rate(self.samp_rate_1*self.sps*self.resampling)

    def get_samp_rate_0(self):
        return self.samp_rate_0

    def set_samp_rate_0(self, samp_rate_0):
        self.samp_rate_0 = samp_rate_0


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--corr-threshold", dest="corr_threshold", type="eng_float", default=eng_notation.num_to_str(0.9),
        help="Set Correlation threshold [default=%default]")
    parser.add_option(
        "", "--det-threshold", dest="det_threshold", type="eng_float", default=eng_notation.num_to_str(0.9),
        help="Set Detection threshold [default=%default]")
    parser.add_option(
        "", "--freq-off", dest="freq_off", type="eng_float", default=eng_notation.num_to_str(0),
        help="Set Frequency offset [default=%default]")
    parser.add_option(
        "", "--index", dest="index", type="eng_float", default=eng_notation.num_to_str(0.5),
        help="Set Modulation index [default=%default]")
    parser.add_option(
        "", "--noise", dest="noise", type="eng_float", default=eng_notation.num_to_str(0.2),
        help="Set Noise [default=%default]")
    parser.add_option(
        "", "--pdu-len", dest="pdu_len", type="intx", default=28,
        help="Set PDU Length [default=%default]")
    parser.add_option(
        "", "--resampling", dest="resampling", type="intx", default=1,
        help="Set resampling [default=%default]")
    parser.add_option(
        "", "--sps", dest="sps", type="intx", default=2,
        help="Set Sample per symbol [default=%default]")
    parser.add_option(
        "", "--PFSK", dest="PFSK", type="intx", default=0,
        help="Set P-FSK [default=%default]")
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(corr_threshold=options.corr_threshold, det_threshold=options.det_threshold, freq_off=options.freq_off, index=options.index, noise=options.noise, pdu_len=options.pdu_len, resampling=options.resampling, sps=options.sps, PFSK=options.PFSK)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
