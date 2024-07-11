import numpy as np
from gnuradio import gr

class blk(gr.sync_block):
    def __init__(self, samp_rate=1e6, fsk_deviation=500e3):
        gr.sync_block.__init__(
            self,
            name='FSK Modulation',
            in_sig=[np.uint8],
            out_sig=[np.complex64]
        )
        self.samp_rate = samp_rate
        self.fsk_deviation = fsk_deviation
        self.center_freq = 0
        self.phase_inc0 = 2.0 * np.pi * (self.center_freq - self.fsk_deviation) / self.samp_rate
        self.phase_inc1 = 2.0 * np.pi * (self.center_freq + self.fsk_deviation) / self.samp_rate
        self.phase = 0
        self.counter = 0  # Initialize 

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        for i in range(len(in0)):
            if in0[i] == 0:
                self.phase += self.phase_inc0
            else:
                self.phase += self.phase_inc1
            out[i] = np.exp(1j * self.phase)
            if self.phase > 2.0 * np.pi:
                self.phase -= 2.0 * np.pi

        # Print first 10 modulated bits every 1000 iterations
        #if self.counter % 1000 == 0:
         #   print("Modulated Bits:", in0[:0])
        #self.counter += 1

        return len(output_items[0])
