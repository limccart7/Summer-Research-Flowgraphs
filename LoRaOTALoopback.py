#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: LoRa OTA Loopback
# Author: root
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
import LoRaOTALoopback_epy_block_0 as epy_block_0  # embedded python block
import LoRaOTALoopback_epy_block_0_0 as epy_block_0_0  # embedded python block
import gnuradio.lora_sdr as lora_sdr




class LoRaOTALoopback(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "LoRa OTA Loopback", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 1000000
        self.freq = freq = 915000000

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
        self.soapy_limesdr_source_0.set_gain(0, min(max(20.0, -12.0), 61.0))
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
        self.soapy_limesdr_sink_0.set_gain(0, min(max(20.0, -12.0), 64.0))
        self.lora_tx_0 = lora_sdr.lora_sdr_lora_tx(
            bw=125000,
            cr=1,
            has_crc=True,
            impl_head=False,
            samp_rate=1000000,
            sf=7,
         ldro_mode=2,frame_zero_padd=1280 )
        self.lora_rx_0 = lora_sdr.lora_sdr_lora_rx( bw=125000, cr=1, has_crc=True, impl_head=False, pay_len=255, samp_rate=samp_rate, sf=7, soft_decoding=True, ldro_mode=2, print_rx=[True,True])
        self.epy_block_0_0 = epy_block_0_0.payload_writer(filepath="/home/ubuntu/Documents/Summer-Research-Flowgraphs/message_storage.txt")
        self.epy_block_0 = epy_block_0.message_prompt()
        self.blocks_message_debug_0 = blocks.message_debug(True)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0, 'out'), (self.lora_tx_0, 'in'))
        self.msg_connect((self.lora_rx_0, 'out'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.lora_rx_0, 'out'), (self.epy_block_0_0, 'payload'))
        self.connect((self.lora_tx_0, 0), (self.soapy_limesdr_sink_0, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.lora_rx_0, 0))


    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.soapy_limesdr_sink_0.set_sample_rate(0, self.samp_rate)
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.soapy_limesdr_sink_0.set_frequency(0, self.freq)
        self.soapy_limesdr_source_0.set_frequency(0, self.freq)




def main(top_block_cls=LoRaOTALoopback, options=None):
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
