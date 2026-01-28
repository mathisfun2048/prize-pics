#!/bin/bash
cd "$(dirname "$0")"

echo "Starting E-Ink Picture Frame..."

source venv/bin/activate
python src/main.py
```

---

# Setup Instructions for Fresh Raspberry Pi Zero 2W

## Hardware Requirements

- Raspberry Pi Zero 2W
- Waveshare 4.2" e-Paper display (V2)
- MicroSD card (16GB+ recommended)
- Button connected to GPIO 18 and GND
- Power supply

## Step 1: Install Raspberry Pi OS

1. Download Raspberry Pi Imager: https://www.raspberrypi.com/software/
2. Flash **Raspberry Pi OS Lite (64-bit)** to SD card
3. Before ejecting, enable SSH:
   - Create empty file named `ssh` in boot partition
4. Configure WiFi (optional):
   - Create `wpa_supplicant.conf` in boot partition:
```
   country=US
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1

   network={
       ssid="YOUR_WIFI_NAME"
       psk="YOUR_WIFI_PASSWORD"
   }