# Google Assistant memo thermal printer
Add a post-it printer feature for Google Home with Raspberry, a chines 200dpi thermal printer and IFTTT.

![GA_Printer](https://user-images.githubusercontent.com/59627714/142873517-01c6a2e7-8d10-43d4-815c-9df0b648dd9d.png)


**This scripts enables printing on chiness copy of Peripage A6. Due to the use of Python this script should be portable to any environment supported by [PyBluez](https://github.com/pybluez/pybluez). This script only print text.**

## Introduction
Projet provide a low-cast post'it printing solution.
Hardware needed :
 - RaspberryPi or any other product with network, Bluetooth Low Energy communication and support Python 3 and Bluez.
 - Chiness thermal printer BLE 200dpi ~20$ on [Aliexpress](https://fr.aliexpress.com/item/1005003351851277.html)
 - Google Home (or any device with Google Assistant)

Software used :
 - Raspberry Pi OS (if Raspberry Pi is used)
 - Python 3.7
 - PyBluez
 - IFTT

### Thermal printer communication
Chiness copy of Peripage A6 is an inexpensive portable thermo printer. It provides by Bluetooth Low Energy.

Trame is composed by

| Header      | data lenght | ?? | DATA           | CRC8 | end of line |
|:------:     |:-----------:|:--:|:----:          |:----:|:-----------:| 
| 51:78:XX:00 | 05          | 00 | 82:7f:7f:7e:82 | 60   | ff          |   


Header XX :
   - bf : Print 384 dot
   - a1 : move forward paper (eg: data=01:00 => 1 dot forward)

Print data (eg 82 -> 1000 0010) :
  - bit[0] : 1 = Black, 0 = White
  - bit[2-7] : number of dot

## Installation

### Prerequisites

 - RaspberryPi with [RaspberriPi OS Lite Bullseye](https://downloads.raspberrypi.org/raspios_lite_armhf/images/raspios_lite_armhf-2021-11-08/2021-10-30-raspios-bullseye-armhf-lite.zip)

### Install dependencies

apt install git python-pip3 python3-bluez libopenjp2-7

### Clone project and Python dependencies

git clone https://github.com/Tb7386/GA_Post-it_thermal_printer.git
pip3 install -r requirements.txt



The next step is to identify the Bluetooth MAC address of your printer. On Linux, this can be easily done using `hcitool`:

```bash
elias@luna:~$ hcitool scan
Scanning ...
B5:5B:13:08:F6:22	PeriPage_F622
elias@luna:~$ 
