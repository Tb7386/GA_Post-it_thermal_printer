# Google Assistant memo thermal printer
Add a post-it printer feature for Google Home with Raspberry, a chines 200dpi thermal printer and IFTTT.

![GA_Printer](https://user-images.githubusercontent.com/59627714/142870722-ee2301b1-b301-4a24-92b4-a5bf1afc9e40.png)

**This scripts enables printing on chiness copy of Peripage A6. Due to the use of Python this script should be portable to any environment supported by [PyBluez](https://github.com/pybluez/pybluez)**

## Introduction
Projet provide a low-cast post'it printing solution.
Hardware needed :
 - RaspberryPi or all others product with network, Bluetooth Low Energy communication and support Python 3 and Bluez.
 - Chiness thermal printer BLE 200dpi ~20$ (https://fr.aliexpress.com/item/1005003351851277.html)
 - Google Home (or all device with Google Assistant)

Software used :
 - Raspberry Pi OS (if Raspberry Pi is used)
 - Python 3.7
 - PyBluez
 - IFTT

### Thermal printer communication
Chiness copy of Peripage A6 (buy on Aliexpress https://fr.aliexpress.com/item/1005003351851277.html?spm=a2g0s.9042311.0.0.2b904c4dRWJyPA) is an inexpensive portable thermo printer. It provides by Bluetooth Low Energy. This script only print text.

Trame is composed by

|   Header    | data lenght | ?? |       DATA     | CRC8 | end of line 

| 51:78:XX:00 |     05      | 00 | 82:7f:7f:7e:82 | 60   |     ff     


Header XX :
   - bf : Print 384 dot
   - a1 : move forward paper (eg: data=01:00 => 1 dot forward)

Print data (eg 82 -> 1000 0010) :
  - bit[0] : 1 = Black, 0 = White
  - bit[2-7] : number of do

## Installation
