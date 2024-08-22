#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: ubuntu
# GNU Radio version: 3.10.3.0

from gnuradio import blocks
import pmt
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import soapy
import LoRa_Loopback_epy_block_0_0 as epy_block_0_0  # embedded python block
import configparser
import gnuradio.lora_sdr as lora_sdr




class LoRa_Loopback(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)

        ##################################################
        # Variables
        ##################################################
        self._sf_config = configparser.ConfigParser()
        self._sf_config.read('/home/ubuntu/LoRa_Tests/LoRa_config.ini')
        try: sf = self._sf_config.getint('LoRa', 'sf')
        except: sf = 7
        self.sf = sf
        self.samp_rate = samp_rate = 1000000
        self.impl_head = impl_head = False
        self.has_crc = has_crc = True
        self.cr = cr = 1
        self.center_freq = center_freq = 915000000
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
        self.soapy_limesdr_source_0.set_frequency(0, center_freq)
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
        self.soapy_limesdr_sink_0.set_frequency(0, center_freq)
        self.soapy_limesdr_sink_0.set_frequency_correction(0, 0)
        self.soapy_limesdr_sink_0.set_gain(0, min(max(20.0, -12.0), 64.0))
        self.lora_sdr_whitening_0 = lora_sdr.whitening(False,False,',','packet_len')
        self.lora_sdr_modulate_0 = lora_sdr.modulate(sf, samp_rate, bw, [8,16], (int(20*2**sf*samp_rate/bw)),8)
        self.lora_sdr_modulate_0.set_min_output_buffer(10000000)
        self.lora_sdr_interleaver_0 = lora_sdr.interleaver(cr, sf, 0, 125000)
        self.lora_sdr_header_0 = lora_sdr.header(impl_head, has_crc, cr)
        self.lora_sdr_hamming_enc_0 = lora_sdr.hamming_enc(cr, sf)
        self.lora_sdr_gray_demap_0 = lora_sdr.gray_demap(sf)
        self.lora_sdr_add_crc_0 = lora_sdr.add_crc(has_crc)
        self.lora_rx_0 = lora_sdr.lora_sdr_lora_rx( bw=125000, cr=1, has_crc=True, impl_head=False, pay_len=255, samp_rate=samp_rate, sf=7, soft_decoding=True, ldro_mode=2, print_rx=[True,True])
        self.epy_block_0_0 = epy_block_0_0.payload_writer(filepath="/home/ubuntu/Desktop/Summer-Research-Flowgraphs/message_storage.txt")
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.blocks_file_source_0 = blocks.file_source(gr.sizeof_char*1, '/home/ubuntu/Desktop/Summer-Research-Flowgraphs/LoRa BER Testing/random_hex_file.txt', False, 0, 0)
        self.blocks_file_source_0.set_begin_tag(pmt.PMT_NIL)


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.lora_rx_0, 'out'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.lora_rx_0, 'out'), (self.epy_block_0_0, 'payload'))
        self.connect((self.blocks_file_source_0, 0), (self.lora_sdr_whitening_0, 0))
        self.connect((self.lora_sdr_add_crc_0, 0), (self.lora_sdr_hamming_enc_0, 0))
        self.connect((self.lora_sdr_gray_demap_0, 0), (self.lora_sdr_modulate_0, 0))
        self.connect((self.lora_sdr_hamming_enc_0, 0), (self.lora_sdr_interleaver_0, 0))
        self.connect((self.lora_sdr_header_0, 0), (self.lora_sdr_add_crc_0, 0))
        self.connect((self.lora_sdr_interleaver_0, 0), (self.lora_sdr_gray_demap_0, 0))
        self.connect((self.lora_sdr_modulate_0, 0), (self.soapy_limesdr_sink_0, 0))
        self.connect((self.lora_sdr_whitening_0, 0), (self.lora_sdr_header_0, 0))
        self.connect((self.soapy_limesdr_source_0, 0), (self.lora_rx_0, 0))


    def get_sf(self):
        return self.sf

    def set_sf(self, sf):
        self.sf = sf
        self.lora_sdr_gray_demap_0.set_sf(self.sf)
        self.lora_sdr_hamming_enc_0.set_sf(self.sf)
        self.lora_sdr_interleaver_0.set_sf(self.sf)
        self.lora_sdr_modulate_0.set_sf(self.sf)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.soapy_limesdr_sink_0.set_sample_rate(0, self.samp_rate)
        self.soapy_limesdr_source_0.set_sample_rate(0, self.samp_rate)

    def get_impl_head(self):
        return self.impl_head

    def set_impl_head(self, impl_head):
        self.impl_head = impl_head

    def get_has_crc(self):
        return self.has_crc

    def set_has_crc(self, has_crc):
        self.has_crc = has_crc

    def get_cr(self):
        return self.cr

    def set_cr(self, cr):
        self.cr = cr
        self.lora_sdr_hamming_enc_0.set_cr(self.cr)
        self.lora_sdr_header_0.set_cr(self.cr)
        self.lora_sdr_interleaver_0.set_cr(self.cr)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.soapy_limesdr_sink_0.set_frequency(0, self.center_freq)
        self.soapy_limesdr_source_0.set_frequency(0, self.center_freq)

    def get_bw(self):
        return self.bw

    def set_bw(self, bw):
        self.bw = bw




def main(top_block_cls=LoRa_Loopback, options=None):
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
