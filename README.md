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
```
apt install git python-pip3 python3-bluez libopenjp2-7
```
### Clone project and Python dependencies
```
git clone https://github.com/Tb7386/GA_Post-it_thermal_printer.git
pip3 install -r ./GA_Post-it_thermal_printer/requirements.txt
```
## CLI Usage
```
python3 ./GA_Post-it_thermal_printer/ga_printer.py OPTIONS
```

### OPTIONS

usage: ga_printer.py [-h] [-t TEXT] [-p PORT] [-s SIZE] BTMAC

Print an text to a thermal printer

positional arguments:
  BTMAC                 BT MAC address of printer (type FIND to scan BLE devices)

optional arguments:
 - -h, --help :           show this help message and exit
 - -t TEXT, --text TEXT : Text to be printed
 - -p PORT, --port PORT : HTTP port
 - -s SIZE, --size SIZE : Font size

### First find Bluetooth mac address of printer

```
python3 ./GA_Post-it_thermal_printer/ga_printer.py FIND
```
Result
```
name: , address: 73:2D:48:3E:C9:BE
name: GA4, address: 7A:4D:3B:FD:FE:ED
name: , address: 70:C8:63:81:D2:4B
```

### Print text

```
python3 ./GA_Post-it_thermal_printer/ga_printer.py 7A:4D:3B:FD:FE:ED -t "hello world"
```

You can define font size with "-s" option (font size default = 50)

### Start HTTP server

```
python3 ./GA_Post-it_thermal_printer/ga_printer.py 7A:4D:3B:FD:FE:ED -p 8080
```
Start a HTTP server with TCP 8080 listen port.
You can define font size with "-s" option (font size default = 50)

HTTP server print all text receive with POST requete
