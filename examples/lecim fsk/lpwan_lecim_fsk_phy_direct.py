#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: LPWAN LECIM FSK PHY
# Author: Victor Guipont
# Generated: Wed Aug  9 12:34:43 2017
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import fec
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from lecim_fsk_modulator import lecim_fsk_modulator  # grc-generated hier_block
from lecim_fsk_zero_padding import lecim_fsk_zero_padding  # grc-generated hier_block
from optparse import OptionParser
import lpwan
import numpy as np
import pmt
import random as rnd
import sip
from gnuradio import qtgui


class lpwan_lecim_fsk_phy_direct(gr.top_block, Qt.QWidget):

    def __init__(self, band=False, burst_tag="burst", data_whitening=True, fcs=False, index=0.5, pdu_len=32, pfsk=False, preamble_len=64, spreading=True, spreading_alternating=False, spreading_factor=16, sps=2):
        gr.top_block.__init__(self, "LPWAN LECIM FSK PHY")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("LPWAN LECIM FSK PHY")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "lpwan_lecim_fsk_phy_direct")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.band = band
        self.burst_tag = burst_tag
        self.data_whitening = data_whitening
        self.fcs = fcs
        self.index = index
        self.pdu_len = pdu_len
        self.pfsk = pfsk
        self.preamble_len = preamble_len
        self.spreading = spreading
        self.spreading_alternating = spreading_alternating
        self.spreading_factor = spreading_factor
        self.sps = sps

        ##################################################
        # Variables
        ##################################################
        self.phy = phy = lpwan.fsk_lecim_phy.physical_layer(sps, index, band, preamble_len, fcs, data_whitening, pfsk, spreading, spreading_alternating, spreading_factor, pdu_len)
        self.cc_poly = cc_poly = [121,91]
        self.samp_rate = samp_rate = phy.symbol_rate*phy.sps
        self.len_tag_var = len_tag_var = "packet_len"


        self.cc_encoder_PHR = cc_encoder_PHR = fec.cc_encoder_make(16, 7, 2, (cc_poly), 0, fec.CC_TERMINATED, False)



        self.cc_encoder_PDU = cc_encoder_PDU = fec.cc_encoder_make(phy.n_block*9*8, 7, 2, (cc_poly), 0, fec.CC_TERMINATED, False)



        self.cc_decoder_PHR = cc_decoder_PHR = fec.cc_decoder.make(44, 7, 2, (cc_poly), 0, -1, fec.CC_TERMINATED, True)



        self.cc_decoder_PDU = cc_decoder_PDU = fec.cc_decoder.make(phy.n_block*9*8, 7, 2, (cc_poly), 0, -1, fec.CC_TERMINATED, False)

        self.SHR = SHR = phy.SHR
        self.PHR = PHR = phy.PHR

        ##################################################
        # Blocks
        ##################################################
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
        	1072*6, #size
        	phy.symbol_rate*phy.sps, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(2):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.lpwan_fsk_lecim_zero_depadding_bb_0 = lpwan.fsk_lecim_zero_depadding_bb()
        self.lpwan_fsk_lecim_whitening_bb_1 = lpwan.fsk_lecim_whitening_bb(phy.data_whitening)
        self.lpwan_fsk_lecim_whitening_bb_0 = lpwan.fsk_lecim_whitening_bb(phy.data_whitening)
        self.lpwan_fsk_lecim_spreading_bb_0_0 = lpwan.fsk_lecim_spreading_bb(phy.phyLecimFskSpreading, phy.phyLecimFskSpreadingFactor, phy.phyLecimFskSpreadingAlternating)
        self.lpwan_fsk_lecim_spreading_bb_0 = lpwan.fsk_lecim_spreading_bb(phy.phyLecimFskSpreading, phy.phyLecimFskSpreadingFactor, phy.phyLecimFskSpreadingAlternating)
        self.lpwan_fsk_lecim_phr_pdu_demux_0 = lpwan.fsk_lecim_phr_pdu_demux(phy.sps, phy.symbol_rate, phy.phyLecimFskSpreadingFactor, True)
        self.lpwan_fsk_lecim_phr_parser_0 = lpwan.fsk_lecim_phr_parser("packet_len")
        self.lpwan_fsk_lecim_interleaver_1 = lpwan.fsk_lecim_interleaver(False, phy.n_block, 'packet_len')
        self.lpwan_fsk_lecim_interleaver_0 = lpwan.fsk_lecim_interleaver(True, phy.n_block, len_tag_var)
        self.lpwan_fsk_lecim_despreading_bb_1_0 = lpwan.fsk_lecim_despreading_bb(phy.phyLecimFskSpreading, phy.phyLecimFskSpreadingFactor, phy.phyLecimFskSpreadingAlternating)
        self.lpwan_fsk_lecim_despreading_bb_1 = lpwan.fsk_lecim_despreading_bb(phy.phyLecimFskSpreading, phy.phyLecimFskSpreadingFactor, phy.phyLecimFskSpreadingAlternating)
        self.lpwan_fsk_lecim_demodulator_cb_0 = lpwan.fsk_lecim_demodulator_cb(phy.PFSK, phy.sps, phy.freq_dev, phy.symbol_rate)
        self.lpwan_fsk_lecim_deinterleaver_0_0 = lpwan.fsk_lecim_deinterleaver(False, phy.n_block, 'packet_len')
        self.lpwan_fsk_lecim_deinterleaver_0 = lpwan.fsk_lecim_deinterleaver(True, phy.n_block, 'packet_len')
        self.lpwan_fsk_lecim_corr_est_cc_0 = lpwan.fsk_lecim_corr_est_cc((phy.SHR_mod), phy.PFSK, phy.sps, 1, 0.999)
        self.lecim_fsk_zero_padding_0 = lecim_fsk_zero_padding(
            len_tag_var="packet_len",
            pad=phy.n_pad,
        )
        self.lecim_fsk_modulator_0 = lecim_fsk_modulator(
            burst_tag=burst_tag,
            freq_dev=phy.freq_dev,
            packet_len=len(SHR)+(44+72*phy.n_block)*spreading_factor,
            pfsk=phy.PFSK,
            sps=phy.sps,
            symbol_rate=phy.symbol_rate,
        )
        self.fec_extended_tagged_encoder_0 = fec.extended_tagged_encoder(encoder_obj_list=cc_encoder_PDU, puncpat='11', lentagname=len_tag_var, mtu=phy.n_block*9)
        self.fec_extended_tagged_encoder = fec.extended_tagged_encoder(encoder_obj_list=cc_encoder_PHR, puncpat='11', lentagname=len_tag_var, mtu=2)
        self.fec_extended_tagged_decoder_0_0 = self.fec_extended_tagged_decoder_0_0 = fec_extended_tagged_decoder_0_0 = fec.extended_tagged_decoder(decoder_obj_list=cc_decoder_PDU, ann=None, puncpat='11', integration_period=10000, lentagname='packet_len', mtu=phy.n_block*9)
        self.fec_extended_tagged_decoder_0 = self.fec_extended_tagged_decoder_0 = fec_extended_tagged_decoder_0 = fec.extended_tagged_decoder(decoder_obj_list=cc_decoder_PHR, ann=None, puncpat='11', integration_period=10000, lentagname='packet_len', mtu=6)
        self.digital_chunks_to_symbols_xx_0_0_0 = digital.chunks_to_symbols_bf((-1,1), 1)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bf((-1,1), 1)
        self.blocks_vector_source_x_1 = blocks.vector_source_b(PHR, True, 1, [gr.tag_utils.python_to_tag((0, pmt.intern(len_tag_var), pmt.from_long(len(PHR))))])
        self.blocks_vector_source_x_0 = blocks.vector_source_b(SHR, True, 1, [gr.tag_utils.python_to_tag((0, pmt.intern(len_tag_var), pmt.from_long(len(SHR))))])
        self.blocks_throttle_0 = blocks.throttle(gr.sizeof_gr_complex*1, samp_rate,True)
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, 'pdu_len')
        self.blocks_stream_mux_0 = blocks.stream_mux(gr.sizeof_char*1, (len(SHR), (len(PHR)*2+12)*spreading_factor if phy.phyLecimFskSpreading else len(PHR)*2+12, phy.n_block*9*8*spreading_factor if phy.phyLecimFskSpreading else phy.n_block*9*8))
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, 1, len_tag_var, True, gr.GR_LSB_FIRST)
        self.blocks_repack_bits_bb_0 = blocks.repack_bits_bb(1, 8, 'pdu_len', False, gr.GR_LSB_FIRST)
        self.blocks_random_pdu_0 = blocks.random_pdu(pdu_len, pdu_len, chr(0xFF), 1)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("generate"), 1000)
        self.blocks_message_debug_0 = blocks.message_debug()
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, 0)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_random_pdu_0, 'generate'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self.blocks_message_debug_0, 'print_pdu'))
        self.msg_connect((self.lpwan_fsk_lecim_phr_parser_0, 'phr_data'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.lpwan_fsk_lecim_phr_parser_0, 'phr_data'), (self.lpwan_fsk_lecim_phr_pdu_demux_0, 'phr_data'))
        self.connect((self.blocks_delay_0, 0), (self.lpwan_fsk_lecim_corr_est_cc_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.blocks_repack_bits_bb_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.lecim_fsk_zero_padding_0, 0))
        self.connect((self.blocks_stream_mux_0, 0), (self.lecim_fsk_modulator_0, 0))
        self.connect((self.blocks_throttle_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_mux_0, 0))
        self.connect((self.blocks_vector_source_x_1, 0), (self.fec_extended_tagged_encoder, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.fec_extended_tagged_decoder_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0_0, 0), (self.fec_extended_tagged_decoder_0_0, 0))
        self.connect((self.fec_extended_tagged_decoder_0, 0), (self.lpwan_fsk_lecim_phr_parser_0, 0))
        self.connect((self.fec_extended_tagged_decoder_0_0, 0), (self.lpwan_fsk_lecim_zero_depadding_bb_0, 0))
        self.connect((self.fec_extended_tagged_encoder, 0), (self.lpwan_fsk_lecim_interleaver_0, 0))
        self.connect((self.fec_extended_tagged_encoder_0, 0), (self.lpwan_fsk_lecim_interleaver_1, 0))
        self.connect((self.lecim_fsk_modulator_0, 0), (self.blocks_throttle_0, 0))
        self.connect((self.lecim_fsk_zero_padding_0, 0), (self.fec_extended_tagged_encoder_0, 0))
        self.connect((self.lpwan_fsk_lecim_corr_est_cc_0, 0), (self.lpwan_fsk_lecim_demodulator_cb_0, 0))
        self.connect((self.lpwan_fsk_lecim_corr_est_cc_0, 1), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.lpwan_fsk_lecim_deinterleaver_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.lpwan_fsk_lecim_deinterleaver_0_0, 0), (self.digital_chunks_to_symbols_xx_0_0_0, 0))
        self.connect((self.lpwan_fsk_lecim_demodulator_cb_0, 0), (self.lpwan_fsk_lecim_phr_pdu_demux_0, 0))
        self.connect((self.lpwan_fsk_lecim_despreading_bb_1, 0), (self.lpwan_fsk_lecim_deinterleaver_0, 0))
        self.connect((self.lpwan_fsk_lecim_despreading_bb_1_0, 0), (self.lpwan_fsk_lecim_whitening_bb_1, 0))
        self.connect((self.lpwan_fsk_lecim_interleaver_0, 0), (self.lpwan_fsk_lecim_spreading_bb_0, 0))
        self.connect((self.lpwan_fsk_lecim_interleaver_1, 0), (self.lpwan_fsk_lecim_whitening_bb_0, 0))
        self.connect((self.lpwan_fsk_lecim_phr_pdu_demux_0, 0), (self.lpwan_fsk_lecim_despreading_bb_1, 0))
        self.connect((self.lpwan_fsk_lecim_phr_pdu_demux_0, 1), (self.lpwan_fsk_lecim_despreading_bb_1_0, 0))
        self.connect((self.lpwan_fsk_lecim_spreading_bb_0, 0), (self.blocks_stream_mux_0, 1))
        self.connect((self.lpwan_fsk_lecim_spreading_bb_0_0, 0), (self.blocks_stream_mux_0, 2))
        self.connect((self.lpwan_fsk_lecim_whitening_bb_0, 0), (self.lpwan_fsk_lecim_spreading_bb_0_0, 0))
        self.connect((self.lpwan_fsk_lecim_whitening_bb_1, 0), (self.lpwan_fsk_lecim_deinterleaver_0_0, 0))
        self.connect((self.lpwan_fsk_lecim_zero_depadding_bb_0, 0), (self.blocks_repack_bits_bb_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lpwan_lecim_fsk_phy_direct")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_band(self):
        return self.band

    def set_band(self, band):
        self.band = band
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_burst_tag(self):
        return self.burst_tag

    def set_burst_tag(self, burst_tag):
        self.burst_tag = burst_tag
        self.lecim_fsk_modulator_0.set_burst_tag(self.burst_tag)

    def get_data_whitening(self):
        return self.data_whitening

    def set_data_whitening(self, data_whitening):
        self.data_whitening = data_whitening
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_fcs(self):
        return self.fcs

    def set_fcs(self, fcs):
        self.fcs = fcs
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_pdu_len(self):
        return self.pdu_len

    def set_pdu_len(self, pdu_len):
        self.pdu_len = pdu_len
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_pfsk(self):
        return self.pfsk

    def set_pfsk(self, pfsk):
        self.pfsk = pfsk
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_preamble_len(self):
        return self.preamble_len

    def set_preamble_len(self, preamble_len):
        self.preamble_len = preamble_len
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_spreading(self):
        return self.spreading

    def set_spreading(self, spreading):
        self.spreading = spreading
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_spreading_alternating(self):
        return self.spreading_alternating

    def set_spreading_alternating(self, spreading_alternating):
        self.spreading_alternating = spreading_alternating
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_spreading_factor(self):
        return self.spreading_factor

    def set_spreading_factor(self, spreading_factor):
        self.spreading_factor = spreading_factor
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))
        self.lecim_fsk_modulator_0.set_packet_len(len(self.SHR)+(44+72*phy.n_block)*self.spreading_factor)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.set_phy(lpwan.fsk_lecim_phy.physical_layer(self.sps, self.index, self.band, self.preamble_len, self.fcs, self.data_whitening, self.pfsk, self.spreading, self.spreading_alternating, self.spreading_factor, self.pdu_len))

    def get_phy(self):
        return self.phy

    def set_phy(self, phy):
        self.phy = phy

    def get_cc_poly(self):
        return self.cc_poly

    def set_cc_poly(self, cc_poly):
        self.cc_poly = cc_poly

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.blocks_throttle_0.set_sample_rate(self.samp_rate)

    def get_len_tag_var(self):
        return self.len_tag_var

    def set_len_tag_var(self, len_tag_var):
        self.len_tag_var = len_tag_var
        self.blocks_vector_source_x_1.set_data(self.PHR, [gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_var), pmt.from_long(len(self.PHR))))])
        self.blocks_vector_source_x_0.set_data(self.SHR, [gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_var), pmt.from_long(len(self.SHR))))])

    def get_cc_encoder_PHR(self):
        return self.cc_encoder_PHR

    def set_cc_encoder_PHR(self, cc_encoder_PHR):
        self.cc_encoder_PHR = cc_encoder_PHR

    def get_cc_encoder_PDU(self):
        return self.cc_encoder_PDU

    def set_cc_encoder_PDU(self, cc_encoder_PDU):
        self.cc_encoder_PDU = cc_encoder_PDU

    def get_cc_decoder_PHR(self):
        return self.cc_decoder_PHR

    def set_cc_decoder_PHR(self, cc_decoder_PHR):
        self.cc_decoder_PHR = cc_decoder_PHR

    def get_cc_decoder_PDU(self):
        return self.cc_decoder_PDU

    def set_cc_decoder_PDU(self, cc_decoder_PDU):
        self.cc_decoder_PDU = cc_decoder_PDU

    def get_SHR(self):
        return self.SHR

    def set_SHR(self, SHR):
        self.SHR = SHR
        self.lecim_fsk_modulator_0.set_packet_len(len(self.SHR)+(44+72*phy.n_block)*self.spreading_factor)
        self.blocks_vector_source_x_0.set_data(self.SHR, [gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_var), pmt.from_long(len(self.SHR))))])

    def get_PHR(self):
        return self.PHR

    def set_PHR(self, PHR):
        self.PHR = PHR
        self.blocks_vector_source_x_1.set_data(self.PHR, [gr.tag_utils.python_to_tag((0, pmt.intern(self.len_tag_var), pmt.from_long(len(self.PHR))))])


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--burst-tag", dest="burst_tag", type="string", default="burst",
        help="Set Burst Tag (for USRP) [default=%default]")
    parser.add_option(
        "", "--index", dest="index", type="eng_float", default=eng_notation.num_to_str(0.5),
        help="Set Modulation index [default=%default]")
    parser.add_option(
        "", "--pdu-len", dest="pdu_len", type="intx", default=32,
        help="Set PDU Length [default=%default]")
    parser.add_option(
        "", "--preamble-len", dest="preamble_len", type="intx", default=64,
        help="Set Preamble Length [default=%default]")
    parser.add_option(
        "", "--spreading-factor", dest="spreading_factor", type="intx", default=16,
        help="Set Spreading factor [default=%default]")
    parser.add_option(
        "", "--sps", dest="sps", type="intx", default=2,
        help="Set Sample per symbol [default=%default]")
    return parser


def main(top_block_cls=lpwan_lecim_fsk_phy_direct, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(burst_tag=options.burst_tag, index=options.index, pdu_len=options.pdu_len, preamble_len=options.preamble_len, spreading_factor=options.spreading_factor, sps=options.sps)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
