import time
import tkinter as tk
from tkinter import simpledialog
from gnuradio import gr
import pmt

class FileLineTransmitter(gr.sync_block):
    def __init__(self, file_path = "/home/ubuntu/Desktop/LoRa BER Testing/tx_test_data", sf=7, bw=62.5, cr=5):
        gr.sync_block.__init__(
            self,
            name="FileLineTransmitter",
            in_sig=None,
            out_sig=None,
        )
        self.message_port_register_out(pmt.intern("out"))

        # Open the file and read lines
        self.lines = self.load_file(file_path)
        self.current_index = 0
        self.transmit_delay = 1.5  # seconds
        self.sf = sf
        self.bw = bw
        self.cr = cr

    def load_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.readlines()
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    def work(self, input_items, output_items):
        if self.current_index < len(self.lines):
            # Prepare the message to send
            print("Transmitting line at: " + str(self.sf) + str(self.bw) + str(self.cr))
            line = self.lines[self.current_index].strip()
            message = pmt.intern(line)
            
            # Send the message
            self.message_port_pub(pmt.intern("out"), message)
            self.current_index += 1
            
            # Sleep for the specified delay
            time.sleep(self.transmit_delay)
        else:
            print("file done transmitting")

        # Indicate that we have finished processing
        return len(output_items)

