# Firmware Instructions

## What to do first

First I would recommend starting with a fresh install of RPi OS with a new SD card. So do that. 

RPi came out with a great remote desktop (that is free!) which should make developing this easier. 

## Hardware Check

If you're developing the program first on a breadboard, I recomend making sure the E-Ink is connected to the correct GPIO so that we don't fry the expensive display. Thank you Waveshare for making this process accessible! 

|E-Ink Pin| GPIO | Physical Pin Number|
|---------|------|--------------------|
|VCC      | 3.3V | 3.3V               |
|GND      | GND  | GND                |
|DIN      | MOSI | 19                 |
|CLK      | SCLK | 23                 |
|CS       | CE0  | 24                 |
|DC       | 25   | 22                 |
|RST      | 17   | 11                 |
|BUSY     | 24   | 18                 |


Here's a reminder of what pin is what for RPis! This layout is consistant for all RPi boards with 40 pins. 

<img width="2064" height="1185" alt="image" src="https://github.com/user-attachments/assets/4d8ac120-e9af-44b6-bb69-23b28b07faca" />


