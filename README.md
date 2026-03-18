# prize-pics
<img width="583" height="665" alt="Screenshot 2026-03-18 at 5 25 27 PM" src="https://github.com/user-attachments/assets/0a9a3c33-9beb-40a4-8d8d-b3163735cfa3" />


## Overview

### tldr: Kindle For Your Photos App

This is an e-ink picture frame. Similar products on the market cost upwards of $200, this only costs $50 and is open source. 

The e-ink module used is the waveshare 4.2" b/w and the brains is a raspberry pi zero 2w. 

There are 2 main components to this project: the physical hardware and the online interface. 

hardware:

<img width="438" height="500" alt="Screenshot 2026-03-18 at 5 25 27 PM" src="https://github.com/user-attachments/assets/0a9a3c33-9beb-40a4-8d8d-b3163735cfa3" />

online interface:

<img width="450" height="500" alt="Screenshot 2026-03-18 at 5 32 00 PM" src="https://github.com/user-attachments/assets/fa3d34fe-25ae-476d-b5f9-25aa4a5f7575" />


## Hardware Specifics

As stated above, the main hardware elements are the e-ink and the rpi. Additionally is a button that allows the user to skip the image on view to the next one in the queue. 

This project does utalize a custom PCB that is listed in another one of my projects. This is open source, feel free to reproduce and edit as you see fit. 



<img width="849" height="834" alt="Screenshot 2026-03-18 at 5 48 54 PM" src="https://github.com/user-attachments/assets/d610bc15-f248-4b98-bf57-3f4bced010aa" />



## Interface Specifics

The key functionality of the software is to 1) allow photo uploads 2) see the queue 3) see a preview and 4) skip the image on view with the skip button. 



## Firmware Specifics

To make this project run, there are a number of different firmware parts that work together. 

The most important pipeline in this project is the image transformation process. The user uploads a full-color jpg, png, jpeg and we need to turn this into 1s, 0s that the b/w e-ink can understand. This is done through dithering that makes b/w images look greyscale to our eyes. 

A key design consideration is that the uploaded image is not stored locally, after it is processed it is deleted. The processed image is cached in memory. This was to ensure security. 


## Build Instructions

All build instructions can be found in hardware_instructions and firmware_instructions.md. The pcb design can be found in another one of my repos, PaperCAM. The hardware is identical between the two projects; however, the firmware is different. Use the firmware in this repo for the prize-pics functionality. 

## Cost

Free.99. This project is open source. 

## Demo

https://www.youtube.com/shorts/J4L4dThzBjg
