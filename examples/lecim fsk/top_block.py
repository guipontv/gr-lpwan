#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Top Block
# Generated: Fri Sep  1 10:54:23 2017
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
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from lpwan_lecim_fsk_phy_tx import lpwan_lecim_fsk_phy_tx  # grc-generated hier_block
from optparse import OptionParser
import lpwan
import numpy as np
import pmt
import sip
import time
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self, index=1, pdu_len=28, resampling=2, sps=2):
        gr.top_block.__init__(self, "Top Block")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Top Block")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Parameters
        ##################################################
        self.index = index
        self.pdu_len = pdu_len
        self.resampling = resampling
        self.sps = sps

        ##################################################
        # Variables
        ##################################################
        self.samp_rate_3 = samp_rate_3 = 75000
        self.samp_rate_2 = samp_rate_2 = 37500
        self.samp_rate_1 = samp_rate_1 = 25000
        self.samp_rate_0 = samp_rate_0 = 12500

        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        	'burst',
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate_1*sps*resampling)
        self.uhd_usrp_sink_0.set_center_freq(902200000, 0)
        self.uhd_usrp_sink_0.set_gain(30, 0)
        self.uhd_usrp_sink_0.set_antenna('TX/RX', 0)
        self.qtgui_number_sink_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_NONE,
            1
        )
        self.qtgui_number_sink_0.set_update_time(0.10)
        self.qtgui_number_sink_0.set_title("")

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        units = ['', '', '', '', '',
                 '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(1):
            self.qtgui_number_sink_0.set_min(i, -1)
            self.qtgui_number_sink_0.set_max(i, 1)
            self.qtgui_number_sink_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0.set_label(i, labels[i])
            self.qtgui_number_sink_0.set_unit(i, units[i])
            self.qtgui_number_sink_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0.enable_autoscale(False)
        self._qtgui_number_sink_0_win = sip.wrapinstance(self.qtgui_number_sink_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_number_sink_0_win)
        self.lpwan_message_counter_0 = lpwan.message_counter(0, 1)
        self.lpwan_lecim_fsk_phy_tx_0 = lpwan_lecim_fsk_phy_tx(
            band=False,
            burst_tag="burst",
            data_whitening=True,
            fcs=False,
            index=index,
            pdu_len=pdu_len + 4,
            pfsk=True,
            preamble_len=64,
            resampling=resampling,
            spreading=True,
            spreading_alternating=False,
            spreading_factor=16,
            sps=sps,
        )
        self.digital_crc32_async_bb_0 = digital.crc32_async_bb(False)
        self.blocks_random_pdu_0 = blocks.random_pdu(pdu_len, pdu_len, chr(0xFF), 1)
        self.blocks_message_strobe_0 = blocks.message_strobe(pmt.intern("generate"), 2000)

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.blocks_random_pdu_0, 'generate'))
        self.msg_connect((self.blocks_random_pdu_0, 'pdus'), (self.digital_crc32_async_bb_0, 'in'))
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.lpwan_lecim_fsk_phy_tx_0, 'in_tx'))
        self.msg_connect((self.digital_crc32_async_bb_0, 'out'), (self.lpwan_message_counter_0, 'in'))
        self.connect((self.lpwan_lecim_fsk_phy_tx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.lpwan_message_counter_0, 0), (self.qtgui_number_sink_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_index(self):
        return self.index

    def set_index(self, index):
        self.index = index
        self.lpwan_lecim_fsk_phy_tx_0.set_index(self.index)

    def get_pdu_len(self):
        return self.pdu_len

    def set_pdu_len(self, pdu_len):
        self.pdu_len = pdu_len
        self.lpwan_lecim_fsk_phy_tx_0.set_pdu_len(self.pdu_len + 4)

    def get_resampling(self):
        return self.resampling

    def set_resampling(self, resampling):
        self.resampling = resampling
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate_1*self.sps*self.resampling)
        self.lpwan_lecim_fsk_phy_tx_0.set_resampling(self.resampling)

    def get_sps(self):
        return self.sps

    def set_sps(self, sps):
        self.sps = sps
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate_1*self.sps*self.resampling)
        self.lpwan_lecim_fsk_phy_tx_0.set_sps(self.sps)

    def get_samp_rate_3(self):
        return self.samp_rate_3

    def set_samp_rate_3(self, samp_rate_3):
        self.samp_rate_3 = samp_rate_3

    def get_samp_rate_2(self):
        return self.samp_rate_2

    def set_samp_rate_2(self, samp_rate_2):
        self.samp_rate_2 = samp_rate_2

    def get_samp_rate_1(self):
        return self.samp_rate_1

    def set_samp_rate_1(self, samp_rate_1):
        self.samp_rate_1 = samp_rate_1
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate_1*self.sps*self.resampling)

    def get_samp_rate_0(self):
        return self.samp_rate_0

    def set_samp_rate_0(self, samp_rate_0):
        self.samp_rate_0 = samp_rate_0


def argument_parser():
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option)
    parser.add_option(
        "", "--index", dest="index", type="eng_float", default=eng_notation.num_to_str(1),
        help="Set Modulation index [default=%default]")
    parser.add_option(
        "", "--pdu-len", dest="pdu_len", type="intx", default=28,
        help="Set PDU Length [default=%default]")
    parser.add_option(
        "", "--sps", dest="sps", type="intx", default=2,
        help="Set Sample per symbol [default=%default]")
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(index=options.index, pdu_len=options.pdu_len, sps=options.sps)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
