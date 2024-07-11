#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
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

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import FSK_LB_OTA_epy_block_0 as epy_block_0  # embedded python block
import FSK_LB_OTA_epy_block_1 as epy_block_1  # embedded python block
import FSK_LB_OTA_epy_block_12_0 as epy_block_12_0  # embedded python block
import FSK_LB_OTA_epy_block_2 as epy_block_2  # embedded python block



from gnuradio import qtgui

class FSK_LB_OTA(gr.top_block, Qt.QWidget):

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

        self.settings = Qt.QSettings("GNU Radio", "FSK_LB_OTA")

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
        self.samp_rate = samp_rate = 1000000

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
        self.soapy_limesdr_source_0.set_bandwidth(0, samp_rate)
        self.soapy_limesdr_source_0.set_frequency(0, 915e6)
        self.soapy_limesdr_source_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_source_0.set_gain(0, min(max(40, -12.0), 61.0))
        self.soapy_limesdr_sink_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_sink_0.set_bandwidth(0, samp_rate)
        self.soapy_limesdr_sink_0.set_frequency(0, 915e6)
        self.soapy_limesdr_sink_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_sink_0.set_gain(0, min(max(40, -12.0), 64.0))
        self.root_raised_cosine_filter_0_0 = filter.fir_filter_ccf(
            10,
            firdes.root_raised_cosine(
                10,
                samp_rate,
                (samp_rate/5),
                1,
                1000))
        self.root_raised_cosine_filter_0 = filter.interp_fir_filter_ccf(
            10,
            firdes.root_raised_cosine(
                1,
                samp_rate,
                (samp_rate/5),
                1,
                1000))
        self.qtgui_time_sink_x_0 = qtgui.time_sink_c(
            1024, #size
            samp_rate, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-1, 1)

        self.qtgui_time_sink_x_0.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_0.enable_tags(True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(True)
        self.qtgui_time_sink_x_0.enable_grid(False)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)


        labels = ['Signal 1', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(2):
            if len(labels[i]) == 0:
                if (i % 2 == 0):
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

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.epy_block_2 = epy_block_2.fsk_demod(samp_rate=samp_rate, fsk_deviation=samp_rate/10)
        self.epy_block_12_0 = epy_block_12_0.bits_to_message(preamble=[0xAB, 0xCD, 0xEF], header_length=1)
        self.epy_block_1 = epy_block_1.custom_message_to_bits(message="Hello, This is a test message.............", interval=10, print_interval=10000, preamble=[0xAB, 0xCD, 0xEF])
        self.epy_block_0 = epy_block_0.blk(samp_rate=samp_rate, fsk_deviation=samp_rate/10)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.epy_block_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.epy_block_1, 0), (self.epy_block_0, 0))
        self.connect((self.epy_block_2, 0), (self.epy_block_12_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.soapy_limesdr_sink_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.epy_block_2, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.root_raised_cosine_filter_0_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FSK_LB_OTA")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.epy_block_0.fsk_deviation = self.samp_rate/10
        self.epy_block_0.samp_rate = self.samp_rate
        self.epy_block_2.fsk_deviation = self.samp_rate/10
        self.epy_block_2.samp_rate = self.samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.samp_rate, (self.samp_rate/5), 1, 1000))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(10, self.samp_rate, (self.samp_rate/5), 1, 1000))
        self.soapy_limesdr_sink_0.set_sample_rate(0, self.samp_rate)
        self.soapy_limesdr_sink_0.set_bandwidth(0, self.samp_rate)
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)
        self.soapy_limesdr_source_0.set_bandwidth(0, self.samp_rate)




def main(top_block_cls=FSK_LB_OTA, options=None):

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
