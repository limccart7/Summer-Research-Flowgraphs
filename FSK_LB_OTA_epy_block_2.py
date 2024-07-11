import numpy as np
from gnuradio import gr

class fsk_demod(gr.sync_block):
    def __init__(self, samp_rate=1e6, fsk_deviation=500e3):
        gr.sync_block.__init__(
            self,
            name='FSK Demodulation',
            in_sig=[np.complex64],
            out_sig=[np.int8]
        )
        self.samp_rate = samp_rate
        self.fsk_deviation = fsk_deviation
        self.counter = 0  # Initialize the counter

    def work(self, input_items, output_items):
        in0 = input_items[0]
        out = output_items[0]

        for i in range(1, len(in0)):
            phase_diff = np.angle(in0[i] * np.conj(in0[i-1]))
            out[i] = 1 if phase_diff > 0 else 0

        # Print first 10 demodulated bits every 1000 iterations
        #if self.counter % 1 == 0:
            #print("Demodulated Bits:", out[:0])
        #self.counter += 1

        return len(output_items[0])
