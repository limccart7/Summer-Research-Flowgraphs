import time
import tkinter as tk
from tkinter import simpledialog
from gnuradio import gr
import pmt

class message_prompt(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(
            self,
            name="message_prompt",
            in_sig=None,
            out_sig=None,
        )
        self.message_port_register_out(pmt.intern("out"))
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main Tkinter window
        self.schedule_next_prompt()

    def schedule_next_prompt(self):
        self.root.after(0, self.prompt_for_message)

    def prompt_for_message(self):
        payload = simpledialog.askstring("Input", "Enter payload:")
        if payload is not None:
            message = pmt.intern(payload)
            for _ in range(3):
                self.message_port_pub(pmt.intern("out"), message)
                time.sleep(2)
        self.schedule_next_prompt()

    def work(self, input_items, output_items):
        return len(output_items)

