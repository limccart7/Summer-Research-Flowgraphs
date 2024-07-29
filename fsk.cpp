#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <wiringPi.h>
#include <wiringPiSPI.h>

#define TRUE (1==1)
#define FALSE (!TRUE)

// SPI Config parameters
#define SPI_CHAN 0
#define NUM_ITERATIONS 10000
#define MAX_SIZE (1024*1024)
////////////////////////////

#define FSK 0x00 // FSK

// Set pa Config Parameter definitions
#define paDutyCycle 0x04
#define hpMax 0x07
#define deviceSel 0x00 // for sx1262
#define paLut 0x01 // ALWAYS
///////////////////////////////////////

// SETRXTXFallBackMode parameter defitinions 
#define FS 0x40 // radio goes into FS mode after tx or rx done
#define STDBY_XOSC 0x30 // radio goes into Standby XOSC mode after done
#define STDBY_RC 0x20 // radio goes into stdby rc after done
///////////////////////////////////////////////////////////////////////

// SET TX parameter defintions
#define power 0x16 // + 22dBm for high power
#define RampTime 0x04 // 200 us
///////////////////////////////


// SET modulation parameter defintions for FSK ONLY, things change for LoRa
#define ModParam1 0x00 // br1
#define ModParam2 0x0D // br2
#define ModParam3 0x55 // br3    ** bit rate = {br1, br2, br3} == br = 32*Fxtal / bit rate ( for bit rate = 300kbps) = 0xD55
#define ModParam4 0x08 // Pulse shape Gaussian BT 1
#define ModParam5 0x09 // Bandwidth of 467kHz
#define ModParam6 0x00 // Frequency deviation1
#define ModParam7 0xCC // Frequency deviation2             Fdev = (FreqDeviation*2^25)/Fxtal = 52,429 = 0xCCCD
#define ModParam8 0xCD // Frequency deviation3    
/////////////////////////////////////////////////////////////////////////////

// Set Pacet Parameter Definitions
#define PacketParam1 0xFF // preamble legnth
#define PacketParam2 0xFF // preamble length
#define PacketParam3 0x05 // Preamble Detector length 16 bits
#define PacketParam4 0x40 // Sync word 8 bytes STARTS at register address 0x06C0 and ends at 0x06C7
#define PacketParam5 0x00 // AddrComp Address filtering disabled
#define PacketParam6 0x00 // Packet type 0x00 (packet length known by both sides, not included in payload)
#define PacketParam7 0xFF // MAX Payload length
#define PacketParam8 0x02 // CRC type CRC_2_BYTES computed o 2nd byte
#define PacketParam9 0x01 // Whitening enabled     
//////////////////////////////////////////////

// DSET_DIO_IRQ_PARAMS definitions
#define irq_mask 0x01 
#define DI01Mask 0x01
#define DI02Mask 0x00 
#define DI03Mask 0x00

#define TX_Base_addr 0x00
#define RX_Base_addr 0x00

// Define SX1262 Commands and other commands
#define SET_SLEEP 0x84 // put into sleep mode
#define SET_STANDBY 0x80 // set in standby mode **BUSY should go low**
#define SET_PACKET_TYPE 0x8A // FSK is 0x00
#define SET_RF_FREQUENCY 0x86
#define SET_PA_CONFIG 0x95
#define SET_TX_PARAMS 0x8E
#define SET_BUFFER_BASE_ADDRESS 0x8F
#define WRITE_BUFFER 0x0E
#define SET_MODULATION_PARAMS 0x8B
#define SET_PACKET_PARAMS 0x8C
#define SET_DIO_IRQ_PARAMS 0x08 
#define WRITE_REG 0x0D
#define SET_TX 0x83
#define GET_IRQ_STATUS 0x12
#define CLEAR_IRQ_STATUS 0x02
#define READ_BUFFER 0x1E
#define SET_CONTINOUS_WAVE_TX 0xD1
#define SETRXTXFallBackMode 0x93 
//////////////////////////////////////////////////////////////////////

// Define PINS with wiringPi #
#define BUSY_PIN 6 // Busy Pin
#define RESET 21 // Reset
#define CS_PIN 10 // CS Pin


static int myFd;

void spiSetup(int speed) {
    if ((myFd = wiringPiSPISetup(SPI_CHAN, speed)) < 0) {
        fprintf(stderr, "Can't open the SPI bus: %s\n", strerror(errno));
        exit(EXIT_FAILURE);
    }
}

// Function to wait for tbusy to go low
void waitForReady(void) {
    while (digitalRead(BUSY_PIN) == HIGH) {
        usleep(100); 
    }
}

int sendSPICommand(unsigned char *cmd, int len) {
    //digitalWrite(CS_PIN, HIGH);
    //usleep(50);
    //digitalWrite(CS_PIN, LOW);
    waitForReady();
    //usleep(500);
    if (wiringPiSPIDataRW(SPI_CHAN, cmd, len) == -1) {
        fprintf(stderr, "SPI command failed: %s\n", strerror(errno));
        return FALSE;
    }
    //digitalWrite(CS_PIN, HIGH);
    return TRUE;
}

int main(void) {
    wiringPiSetup();
    usleep(500);
    spiSetup(16000000); // 1 MHz
    
    pinMode(BUSY_PIN, INPUT);
    pinMode(RESET, OUTPUT);
    pinMode(CS_PIN, OUTPUT);

    digitalWrite(RESET, HIGH);
    usleep(500);
    digitalWrite(RESET, LOW);
    usleep(500);
    
    digitalWrite(CS_PIN, LOW); // set cs low before sending commands
    usleep(500);

    unsigned char cmd1[] = {SET_STANDBY, 0x00}; // Standby RC mode
    unsigned char cmd2[] = {SET_PACKET_TYPE, FSK}; 
    unsigned char cmd3[] = {SET_RF_FREQUENCY, 0x39, 0x65, 0xA4, 0x80}; // Calculated frequency of 962, 962, 560 According to Fxtal 32MHz,RF freq = 915MHz, (RF freq * Fxtal) / 2^25
    unsigned char cmd4[] = {SET_PA_CONFIG, paDutyCycle, hpMax, deviceSel, paLut}; // SX1262  22dBm DATASHEET Page 79
    unsigned char cmd5[] = {SET_TX_PARAMS, power, RampTime};
    unsigned char cmd6[] = {SET_BUFFER_BASE_ADDRESS, TX_Base_addr, RX_Base_addr};
    unsigned char cmd7[] = {SET_MODULATION_PARAMS, ModParam1, ModParam2, ModParam3, ModParam4, ModParam5, ModParam6, ModParam7, ModParam8};
    unsigned char cmd8[] = {SET_PACKET_PARAMS, PacketParam1, PacketParam2, PacketParam3, PacketParam4, PacketParam5, PacketParam6, PacketParam7, PacketParam8, PacketParam9};
    unsigned char cmd9[] = {SET_DIO_IRQ_PARAMS, irq_mask, DI01Mask, DI02Mask, DI03Mask};
    unsigned char syncWord[] = {WRITE_REG, 0x00, 0x06, 0xC0}; // start of sync word address 0x06C0
    unsigned char cmd10[] = {SET_TX, 0x00, 0x00, 0x00}; // timeout disabled
    unsigned char irqStatus[] = {GET_IRQ_STATUS, 0x00, 0x00};
    unsigned char clearIrq[] = {CLEAR_IRQ_STATUS, 0x08};

    unsigned char payload[1024];
    for (int j = 0; j < 1024; ++j) {
        payload[j] = j % 256; // Fill the payload 
    }

    unsigned char bufferCmd[] = {WRITE_BUFFER, TX_Base_addr}; 
    unsigned char fullPayload[sizeof(bufferCmd) + sizeof(payload)];
    memcpy(fullPayload, bufferCmd, sizeof(bufferCmd));
    memcpy(fullPayload + sizeof(bufferCmd), payload, sizeof(payload));

    for (int i = 0; i < NUM_ITERATIONS; i++) {
        sendSPICommand(cmd1, sizeof(cmd1));
        sendSPICommand(cmd2, sizeof(cmd2));
        sendSPICommand(cmd3, sizeof(cmd3));
        sendSPICommand(cmd4, sizeof(cmd4));
        sendSPICommand(cmd5, sizeof(cmd5));
        sendSPICommand(cmd6, sizeof(cmd6));
        sendSPICommand(fullPayload, sizeof(fullPayload));
        sendSPICommand(cmd7, sizeof(cmd7));
        sendSPICommand(cmd8, sizeof(cmd8));
        sendSPICommand(cmd9, sizeof(cmd9));
        sendSPICommand(syncWord, sizeof(syncWord));
        sendSPICommand(cmd10, sizeof(cmd10));
        sendSPICommand(irqStatus, sizeof(irqStatus));
        sendSPICommand(clearIrq, sizeof(clearIrq));
    }

    close(myFd);
    digitalWrite(CS_PIN, HIGH); // set cs high after all commands sent
    return 0;
}
