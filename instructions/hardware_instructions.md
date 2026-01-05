# Hardware Instructions

## Required Hardware

- Raspberry Pi Zero 2W
- Waveshare 4.2" e-ink (https://www.waveshare.com/4.2inch-e-paper-module.htm?srsltid=AfmBOoo4vrPUlG0oTe8azoQ6DSLTgx3QTpRYrzyAuB1PCSKYtxH1Sgqt)
- sd card
- 2 bulk capacitors
- 2 low pass filter capacitors
- button 

## Connections

Follow the pcb schematics!

|E-Ink Pin| GPIO | Physical Pin Number|
|---------|------|--------------------|
|VCC      | 3.3V | 1                  |
|GND      | GND  | 6                  |
|DIN      | MOSI | 19                 |
|CLK      | SCLK | 23                 |
|CS       | CE0  | 24                 |
|DC       | 25   | 22                 |
|RST      | 17   | 11                 |
|BUSY     | 24   | 18                 |

button connected to physical pin 12 / gpio 18



