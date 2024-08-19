import os
from gnuradio import gr
import pmt

class payload_writer(gr.sync_block):
    def __init__(self, filepath="/home/ubuntu/LoRa_Tests/message_storage.txt"):
        gr.sync_block.__init__(
            self,
            name="payload_writer",
            in_sig=None,
            out_sig=None,
        )
        self.message_port_register_in(pmt.intern("payload"))
        self.set_msg_handler(pmt.intern("payload"), self.handle_msg)
        self.filepath = filepath
        
        # Check if the file exists
        if not os.path.exists(self.filepath):
            # Create the file if it does not exist
            with open(self.filepath, 'w') as file:
                pass
        else:
            # Overwrite the file every time the flowgraph is run if it exists
            with open(self.filepath, 'w') as file:
                file.write("")

    def handle_msg(self, msg):
        if pmt.is_pair(msg):
            payload = pmt.symbol_to_string(pmt.cdr(msg))
        else:
            payload = pmt.symbol_to_string(msg)
        
        with open(self.filepath, 'a') as file:
            file.write(payload + "\n")

    def work(self, input_items, output_items):
        return len(output_items)


