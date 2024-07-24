/*
* Author: Ben Duval
* Program Intention: This program sets up SPI communication with the SX1262 LoRa shield,
*                    and sends commands to configure the packet type, modulation parameters,
*                    and packet parameters.
* Date: 7/24/24
* Revision #1
* GPIO Layout Information: 
* NSS - GPIO 8
* MOSI - GPIO 10
* MISO - GPIO 9
* SCLK - GPIO 11
* SXNRESET - GPIO 5
* DIO1 - GPIO 27
* BUSY - GPIO 17
*  - SPI Channel: 0 (SPI 0)
*  - SPI Speed: 500kHz
*/

#include <wiringPi.h>
#include <wiringPiSPI.h>
#include <iostream>
#include <unistd.h>

// Define SPI channel and speed
#define SPI_CHANNEL 0 // SPI 0
#define SPI_SPEED 500000 // 500kHz

// Define SX1262 Commands
#define SET_PACKET_TYPE 0x8A
#define SET_MODULATION_PARAMS 0x8B
#define SET_PACKET_PARAMS 0x8C

// Function to send SPI commands to SX1262
void sendSPICommand(unsigned char *cmd, int length) {
    std::cout << "Sending SPI command: ";
    for (int i = 0; i < length; i++) {
        printf("0x%02X ", cmd[i]);
    }
    std::cout << std::endl;

    wiringPiSPIDataRW(SPI_CHANNEL, cmd, length);

    std::cout << "Response: ";
    for (int i = 0; i < length; i++) {
        printf("0x%02X ", cmd[i]);
    }
    std::cout << std::endl;
}

int main() {
    // Initialize wiringPi library
    if (wiringPiSetup() == -1) {
        std::cerr << "WiringPi initialization failed." << std::endl;
        return 1;
    }

    // Set up SPI communication
    if (wiringPiSPISetup(SPI_CHANNEL, SPI_SPEED) == -1) {
        std::cerr << "SPI setup failed." << std::endl;
        return 1;
    }

    // Set the packet type to FSK
    unsigned char cmd1[] = {SET_PACKET_TYPE, 0x00}; // FSK
    sendSPICommand(cmd1, 2);

    // Set modulation parameters
    unsigned char cmd2[] = {SET_MODULATION_PARAMS, 0x00, 0x1A, 0x00}; // Modulation parameters
    sendSPICommand(cmd2, 4);

    // Set packet parameters
    unsigned char cmd3[] = {SET_PACKET_PARAMS, 0x08, 0xFF, 0x00, 0x00, 0x00}; // Packet parameters
    sendSPICommand(cmd3, 6);

    return 0;
}
