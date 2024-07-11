import numpy as np
from gnuradio import gr

class bits_to_message(gr.sync_block):
    def __init__(self, preamble=[0xAB, 0xCD, 0xEF], header_length=1):
        gr.sync_block.__init__(
            self,
            name='Bits to Message',
            in_sig=[np.uint8],
            out_sig=[]
        )
        self.preamble = np.unpackbits(np.array(preamble, dtype=np.uint8))
        self.header_length = header_length
        self.buffer = np.array([], dtype=np.uint8)
        self.max_buffer_size = 1000000  # Set max buffer size

    def detect_preamble(self, data):
        preamble_length = len(self.preamble)
        for i in range(len(data) - preamble_length + 1):
            if np.array_equal(data[i:i + preamble_length], self.preamble):
                return i + preamble_length
        return -1

    def work(self, input_items, output_items):
        self.buffer = np.concatenate((self.buffer, input_items[0]))

        while True:
            preamble_index = self.detect_preamble(self.buffer)
            if preamble_index == -1:
                break
            
            header_end = preamble_index + self.header_length * 8
            if header_end > len(self.buffer):
                break
            
            header = np.array(self.buffer[preamble_index:header_end], dtype=np.uint8)
            
            if len(header) == 0:
                break
            
            message_length = np.packbits(header)[0]
            message_start = header_end
            message_end = message_start + message_length * 8

            if message_end > len(self.buffer):
                break

            message_bits = np.array(self.buffer[message_start:message_end], dtype=np.uint8)
            
            if len(message_bits) == 0:
                break
            
            message_bytes = np.packbits(message_bits)
            
            # Print the decoded message 
            try:
                message_text = message_bytes.tobytes().decode('utf-8')
                print("Decoded message:", message_text)
            except UnicodeDecodeError:
                pass  

            self.buffer = self.buffer[message_end:]

        # Prevent buffer from growing 
        if len(self.buffer) > self.max_buffer_size:
            self.buffer = self.buffer[-self.max_buffer_size:]

        self.consume(0, len(input_items[0]))
        return 0

