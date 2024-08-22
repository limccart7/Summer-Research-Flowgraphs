import os
import configparser
import itertools

# Define the configuration file path
config_file_path = "/home/ubuntu/LoRa_Tests/LoRa_config.ini"

# Parameters
spreading_factors = [7, 9, 11]
bandwidths = [62500, 125000, 250000, 500000]
coding_rates = [5, 8]

# Function to update config file using configparser
def update_config_file(sf, bw, cr):
    config = configparser.ConfigParser()
    config['LoRa'] = {
        'SF': sf,
        'BW': bw,
        'CR': cr
    }
    with open(config_file_path, 'w') as config_file:
        config.write(config_file)

# Iterate over all combinations of parameters
for sf, bw, cr in itertools.product(spreading_factors, bandwidths, coding_rates):
    
    # Update the config file with current parameters
    update_config_file(sf, bw, cr)
    
    # Print the current parameters to the terminal
    print(f"Testing with SF={sf}, BW={bw}, CR={cr}")

    # Prompt user to proceed
    while True:
        user_input = input("Press Enter to proceed to the next parameters or type 'exit' to quit: ").strip().lower()
        if user_input == '' or user_input == 'exit':
            break

print("BER testing completed for all parameter sets.")

