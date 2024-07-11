import numpy as np
from gnuradio import gr
import sys
print(sys.path)


class custom_message_to_bits(gr.basic_block):
    def __init__(self, message="Hello from FSK", interval=10, print_interval=10, preamble=[170, 170]):
        gr.basic_block.__init__(self,
            name="custom_message_to_bits",
            in_sig=None,
            out_sig=[np.uint8])

        self.message = message
        self.interval = int(interval)
        self.print_interval = int(print_interval)
        self.preamble = np.array(preamble, dtype=np.uint8)
        self.message_bytes = np.frombuffer(message.encode('utf-8'), dtype=np.uint8)
        self.set_output_multiple(8 * (len(self.preamble) + len(self.message_bytes) + 1))  # Output in bits
        self.counter = 0
        self.print_counter = 0

    def byte_to_bits(self, byte_array):
        return np.unpackbits(byte_array)

    def general_work(self, input_items, output_items):
        output = output_items[0]
        if self.counter % self.interval == 0:
            header = np.array([len(self.message_bytes)], dtype=np.uint8)
            packet = np.concatenate((self.preamble, header, self.message_bytes))
            packet_bits = self.byte_to_bits(packet)

            if self.print_counter % self.print_interval == 0:
                print(f"Header (message length): {header[0]}")
                print(f"Source Bits: {packet_bits}")

            self.print_counter += 1
            output[:len(packet_bits)] = packet_bits
            produced = len(packet_bits)
        else:
            zeros_length = 8 * (len(self.preamble) + len(self.message_bytes) + 1)
            output[:zeros_length] = np.zeros(zeros_length, dtype=np.uint8)
            produced = zeros_length
        
        self.counter += 1
        self.consume_each(0)  # No input to consume
        return produced
