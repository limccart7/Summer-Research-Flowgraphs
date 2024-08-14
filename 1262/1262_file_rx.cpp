#include <iostream>
#include <fstream>
#include <RadioLib.h>
#include "PiHal.h"
#include <chrono> // For timestamping
 
// Create a new instance of the HAL class
PiHal* hal = new PiHal(0);
 
// Create the radio module instance
// NSS pin: WiringPi 10 (GPIO 8)
// DIO1 pin: WiringPi 2 (GPIO 27)
// NRST pin: WiringPi 21 (GPIO 5)
// BUSY pin: WiringPi 0 (GPIO 17)
SX1262 radio = new Module(hal, 10, 2, 21, 0);
 
void dio1Handler() {
  // Handler for DIO1 interrupt, will be called when a packet is received
}
 
int main() {
  // Initialize the radio module with XTAL configuration
  printf("[SX1262] Initializing ... ");
  int state = radio.begin(915.0, 125.0, 7, 5, 18,10, 8, 0.0, false);
  if (state != RADIOLIB_ERR_NONE) {
    printf("Initialization failed, code %d\n", state);
    return 1;
  }
  printf("Initialization success!\n");
 
  // Set up the DIO1 interrupt handler
  hal->attachInterrupt(2, dio1Handler, PI_RISING);
 
  // Start receiving packets
  printf("[SX1262] Starting receiver ... ");
  state = radio.startReceive(RADIOLIB_SX126X_RX_TIMEOUT_INF);
  if (state != RADIOLIB_ERR_NONE) {
    printf("Start receive failed, code %d\n", state);
    return 1;
  }
  printf("Receiver started!\n");
 
  // Open file for logging received data
  std::ofstream outfile("received_data.txt", std::ios::out);
  if (!outfile.is_open()) {
    printf("Failed to open file for writing\n");
    return 1;
  }
 
  int packet_count = 0;
 
  // Main loop
  while (true) {
    // Check if a packet has been received
    if (radio.getIrqStatus() & RADIOLIB_SX126X_IRQ_RX_DONE) {
      // Capture the current time as the reception timestamp
      auto now = std::chrono::high_resolution_clock::now();
      auto reception_timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
 
      // Read the received packet
      uint8_t data[64];
      size_t len = sizeof(data);
      state = radio.readData(data, len);
      if (state == RADIOLIB_ERR_NONE) {
        // Successfully read the data
        packet_count++;
        printf("Received packet #%d: %s\n", packet_count, data);
 
        // Extract the transmission timestamp from the received data
        long long transmission_timestamp;
        sscanf((char*)data, "Timestamp: %lld", &transmission_timestamp);
        
      // Restart the receiver
      state = radio.startReceive(RADIOLIB_SX126X_RX_TIMEOUT_INF);
      if (state != RADIOLIB_ERR_NONE) {
        printf("Restart receive failed, code %d\n", state);
        return 1;
      }
    }
 
    // Small delay to avoid busy waiting
    hal->delay(100);
  }
 
  // Close the file 
  outfile.close();
 
  return 0;
}
}