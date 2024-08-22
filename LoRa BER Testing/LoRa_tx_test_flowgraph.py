#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: LoRa_tx_test_flowgraph
# Author: ubuntu
# GNU Radio version: 3.10.3.0

from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import LoRa_tx_test_flowgraph_epy_block_0 as epy_block_0  # embedded python block
import configparser
import gnuradio.lora_sdr as lora_sdr




class LoRa_tx_test_flowgraph(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "LoRa_tx_test_flowgraph", catch_exceptions=True)

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
        self._bw_config = configparser.ConfigParser()
        self._bw_config.read('/home/ubuntu/LoRa_Tests/LoRa_config.ini')
        try: bw = self._bw_config.getint('LoRa', 'bw')
        except: bw = 62500
        self.bw = bw

        ##################################################
        # Blocks
        ##################################################
        self.soapy_limesdr_sink_0 = None
        dev = 'driver=lime'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_limesdr_sink_0 = soapy.sink(dev, "fc32", 1, '',
                                  stream_args, tune_args, settings)
        self.soapy_limesdr_sink_0.set_sample_rate(0, samp_rate)
        self.soapy_limesdr_sink_0.set_bandwidth(0, 0.0)
        self.soapy_limesdr_sink_0.set_frequency(0, freq)
        self.soapy_limesdr_sink_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_sink_0.set_gain(0, min(max(30.0, -12.0), 64.0))
        self.lora_tx_0 = lora_sdr.lora_sdr_lora_tx(
            bw=bw,
            cr=1,
            has_crc=True,
            impl_head=False,
            samp_rate=1000000,
            sf=sf,
         ldro_mode=2,frame_zero_padd=1280 )
        self.epy_block_0 = epy_block_0.FileLineTransmitter(file_path="/home/ubuntu/Desktop/LoRa BER Testing/tx_test_data.txt", sf=sf, bw=bw, cr=5)
        self.blocks_message_debug_0 = blocks.message_debug(True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'out'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.epy_block_0, 'out'), (self.lora_tx_0, 'in'))
        self.connect((self.lora_tx_0, 0), (self.soapy_limesdr_sink_0, 0))


    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.epy_block_0.sf = self.sf
        self.lora_tx_0.set_sf(self.sf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.soapy_limesdr_sink_0.set_sample_rate(0, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_limesdr_sink_0.set_frequency(0, self.freq)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw
        self.epy_block_0.bw = self.bw




def main(top_block_cls=LoRa_tx_test_flowgraph, options=None):
    tb = top_block_cls()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        sys.exit(0)

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    tb.start()

    try:
        input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
