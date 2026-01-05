# Firmware Instructions

## What to do first

First I would recommend starting with a fresh install of RPi OS with a new SD card. So do that. 

RPi came out with a great remote desktop (that is free!) which should make developing this easier.

## Turn SPI on!

The E-Ink I chose for this project uses SPI to communicate between the display and the RPi. To make sure that can happen, we have to turn SPI on. Here's how you can do that:

``` sudo raspi-config ```

Then with the GUI, click Interfacing Options -> SPI -> Yes 

After, we have to reboot our pi for this to take effect. 

``` sudo reboot ```

## Hardware Check

### Part 1: Wiring Things Up
If you're developing the program first on a breadboard, I recomend making sure the E-Ink is connected to the correct GPIO so that we don't fry the expensive display. Thank you Waveshare for making this process accessible! 

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


Here's a reminder of what pin is what for RPis! This layout is consistant for all RPi boards with 40 pins. 

<img width="2064" height="1185" alt="image" src="https://github.com/user-attachments/assets/4d8ac120-e9af-44b6-bb69-23b28b07faca" />


Connect all the pins. Just to be safe, though, don't connect VCC, that'll make sure we don't accidentally fry our board. 

### Part 2: Creating a Test Directory

Later we're going to be creating a virtual environment. It makes it easier if we make a dedicated test directory. For ease of access, I like making mine in the desktop. Here's how you can do that:

``` cd Desktop ``` 

This brings us to the desktop directory. Now we're going to create a test directory. 

``` mkdir test ```

Now we're going to enter that directory. 
``` cd test```

### Part 3: Installing function libraries

now, we will install the libraries we need for our project to work. 

First we need to update apt. This is a package manager. Think of it kinda like an app store, but for your command line. 

```
sudo apt-get update
```

Next, with the package manager we just updated, we're going to install pip!
```
sudo apt-get install python3-pip
```
```
sudo apt-get install python3-pil
```
```
sudo apt-get install python3-numpy
```

All the above should install normally. For the next thing we need to isntall (spidev), we need a python virtual environment. 

We need a virtual environment because RPi OS protects the system's python install. Because packages can mess with the system OS, we can only install this in a virtual environment. 

In a nutshell, a virtual environment is an isolated workspace that has its own interpreter, packages, and dependencies; it's a sandbox in which we can experiment without crashing the system. To make one, first make sure we are in our test directory, then type the following:

``` python3 -m venv venv```

Then to activate, type

``` source venv/bin/activate ```

Now, to install spidev, type this:

```
pip3 install spidev
```

Note how we don't need sudo! this is because we are in a venv!

Now we're going to install gpiozero:

``` sudo apt install python3-gpiozero ```

Note that we do have a sudo here. This is because we want to install this to the system. 

Next, we are going to check to see if git is updated. This is how we're going to be installing the test files from waveshare:



``` sudo apt install git ```

Next, we are going to clone thier repository:

``` git clone https://github.com/waveshare/e-Paper.git ```

You can check this worked properly by accessing teh rpi via hdmi. This way, you can see the test folder in the desktop, and then when you click on it, you'll see a e-paper directory and a venv directory. Now back to terminal. Now we're going to get to the demo. 

``` cd e-Paper/RaspberryPi_JetsonNano/python/examples/ ```

Now, connect the VCC wire to 3v3. 

now we'll exit teh virtual envrionment

``` deactivate``` 

Now run. 

``` python3 epd_4in2_V2_test.py ```


If the test worked successfully, you should see teh e-ink update and go through a test sequence. Congrats! You worked you e-ink!