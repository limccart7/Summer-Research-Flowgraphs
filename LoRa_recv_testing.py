#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: ubuntu
# GNU Radio version: 3.10.3.0

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import LoRa_recv_testing_epy_block_0_0 as epy_block_0_0  # embedded python block
import configparser
import gnuradio.lora_sdr as lora_sdr



from gnuradio import qtgui

class LoRa_recv_testing(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
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

        self.settings = Qt.QSettings("GNU Radio", "LoRa_recv_testing")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self._sf_config = configparser.ConfigParser()
        self._sf_config.read('/home/ubuntu/LoRa_Tests/LoRa_config.ini')
        try: sf = self._sf_config.getint('LoRa', 'sf')
        except: sf = 7
        self.sf = sf
        self.samp_rate = samp_rate = 1000000
        self.freq = freq = 915000000
        self._file_path_config = configparser.ConfigParser()
        self._file_path_config.read('/home/ubuntu/LoRa_Tests/LoRa_config.ini')
        try: file_path = self._file_path_config.get('LoRa', file_path)
        except: file_path = '0'
        self.file_path = file_path
        self._bw_config = configparser.ConfigParser()
        self._bw_config.read('/home/ubuntu/LoRa_Tests/LoRa_config.ini')
        try: bw = self._bw_config.getint('LoRa', 'bw')
        except: bw = 62500
        self.bw = bw

        ##################################################
        # Blocks
        ##################################################
        self.soapy_limesdr_source_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_source_0 = soapy.source(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_source_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_source_0.set_bandwidth(0, 0.0)
        self.soapy_limesdr_source_0.set_frequency(0, freq)
        self.soapy_limesdr_source_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_source_0.set_gain(0, min(max(40, -12.0), 61.0))
        self.lora_rx_0 = lora_sdr.lora_sdr_lora_rx( bw=125000, cr=1, has_crc=True, impl_head=False, pay_len=255, samp_rate=samp_rate, sf=sf, soft_decoding=True, ldro_mode=2, print_rx=[True,True])
        self.epy_block_0_0 = epy_block_0_0.payload_writer(filepath="/home/ubuntu/LoRa_Tests/message_storage.txt")
        self.blocks_message_debug_0 = blocks.message_debug(True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_rx_0, 'out'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.lora_rx_0, 'out'), (self.epy_block_0_0, 'payload'))
        self.connect((self.soapy_limesdr_source_0, 0), (self.lora_rx_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "LoRa_recv_testing")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_limesdr_source_0.set_frequency(0, self.freq)

    def get_file_path(self):
        return self.file_path

    def set_file_path(self, file_path):
        self.file_path = file_path
        self._file_path_config = configparser.ConfigParser()
        self._file_path_config.read('/home/ubuntu/LoRa_Tests/LoRa_config.ini')
        if not self._file_path_config.has_section('LoRa'):
        	self._file_path_config.add_section('LoRa')
        self._file_path_config.set('LoRa', self.file_path, str(None))
        self._file_path_config.write(open('/home/ubuntu/LoRa_Tests/LoRa_config.ini', 'w'))

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw




def main(top_block_cls=LoRa_recv_testing, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
