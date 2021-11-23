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

HTTP server print all text receive with POST request

## ADD Google Assistant support

IFTT can send POST HTTP request with voice command.

### Prerequisites

 - Create a account on [IFTTT](https://ifttt.com/login)
 - Link your Google account on IFTTT
 - NAT your RaspberryPI HTTP server on your internet box
 - If necessary configure a dynamic DNS service 

### Configure new APPLET

/!\ Free IFTTT account can use only 5 applets

Create new applet
![image](https://user-images.githubusercontent.com/59627714/143009099-07930b62-6564-45d6-83aa-fdfe7313a093.png)
Click  **IF ADD** button
![image](https://user-images.githubusercontent.com/59627714/143009174-b6b73d97-0cf7-484d-9aa8-cdded6835f84.png)
Search **Google Assistant** service
![image](https://user-images.githubusercontent.com/59627714/143009503-3457a877-5e13-4866-849f-599701ac2e89.png)
Select **Say a phrase with a text ingredient** trigger
![image](https://user-images.githubusercontent.com/59627714/143009651-3b200a3c-6fd2-4728-9730-1ff5320b2737.png)
Configure trigger. Text print is **$**
![image](https://user-images.githubusercontent.com/59627714/143009862-d5a736f6-c676-41a3-87a9-a3f16840eaa4.png)
Click **THEN THAT ADD** button
![image](https://user-images.githubusercontent.com/59627714/143010023-5e7ee820-7cad-44ed-8b8e-57633a9678a5.png)
Search **Webhooks** service
![image](https://user-images.githubusercontent.com/59627714/143010067-5b5fdc3a-4114-4196-9ce1-ee60a44d6a55.png)
Choose **Make a web request** action
![image](https://user-images.githubusercontent.com/59627714/143010271-9db665a4-5b7b-4852-8887-1210668508a7.png)
Configure action. 
 - IP : is public IP addess of RaspberryPi HTTP server (Public IP of internet box)
 - PORT : is NAT port to access RaspberryPi HTTP server
![image](https://user-images.githubusercontent.com/59627714/143010648-f108aa09-a57c-4b4f-a719-b399185d3e9d.png)

Save and test your new feature. 
Say :
 - "OK Google, print memo buy bread"
 - "OK Google, print invoice"

