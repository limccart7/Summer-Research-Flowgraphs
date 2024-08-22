import os
import configparser
import itertools
import subprocess

# Define the configuration file path
config_file_path = "/home/ubuntu/LoRa_Tests/LoRa_config.ini"

# Parameters
spreading_factors = [7, 9, 11]
bandwidths = [62500, 125000, 250000, 500000]
coding_rates = [5, 8]

# Function to update config file using configparser
def update_config_file(sf, bw, cr, file_path):
    config = configparser.ConfigParser()
    config['LoRa'] = {
        'SF': sf,
        'BW': bw,
        'CR': cr,
        'file_path': file_path
    }
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

# Function to create output file path
def create_output_file(sf, bw, cr):
    output_file_name = f"rx_data_{sf}_{bw}_{cr}.txt"
    output_file_path = os.path.join("/home/ubuntu/LoRa_Tests", output_file_name)
    return output_file_path

# Iterate over all combinations of parameters
for sf, bw, cr in itertools.product(spreading_factors, bandwidths, coding_rates):
    # Create the output file path
    output_file_path = create_output_file(sf, bw, cr)
    
    # Update the config file with current parameters and output file path
    update_config_file(sf, bw, cr, output_file_path)
    
    # Print the current parameters to the terminal
    print(f"Testing with SF={sf}, BW={bw}, CR={cr}")
    print(f"Output file path: {output_file_path}")
    
    # Call the flowgraph script
    process = subprocess.Popen(["python3", "/path/to/LoRa_recv_testing.py"])
    
    # Wait for the user to press the space bar to continue
    input("Press the space bar to quit the flowgraph and proceed to the next parameters...")
    
    # Terminate the flowgraph process
    process.terminate()
    process.wait()

print("BER testing completed for all parameter sets.")

