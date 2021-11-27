#Composition de la trame 
# |   Header    | Longueur de données | ?? |       DATA     | CRC8 | Fin de ligne |
# | 51:78:XX:00 |     05              | 00 | 82:7f:7f:7e:82 | 60   |       ff     |
# Header XX :
#     - bf ou a3 : Ecriture de 384 points en RAW
#     - a1 : Avancer le papier de DATA (ex: 01:00 avance de 1dp, 10:00 avance de 10dp)
# Data (eg 82 -> 1000 0010) :
#     - bit[0] : 1 = Black, 0 = White
#     - bit[2-7] : Nombre de points 


from gattlib import GATTRequester, DiscoveryService
from PIL import Image, ImageOps, ImageFont, ImageDraw
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import crc8
import sys
import argparse
import textwrap

parser = argparse.ArgumentParser(description="Print an text to a thermal printer")
parser.add_argument("BTMAC", help="BT MAC address of printer (type FIND to scan BLE devices)")
parser.add_argument("-t", "--text", type=str, help="Text to be printed")
parser.add_argument("-p", "--port", type=str, help="HTTP port")
parser.add_argument("-s", "--size", type=str, help="Font size")
parser.add_argument("-d", "--device", type=str, help="Bluetooth Device (by default hci0)")
args = parser.parse_args()

# ------------------------------------------------------------------------------
# printer : Print text from command line or http post request
# ------------------------------------------------------------------------------
def printer(text,size=50):
    req = bleConnect(args.BTMAC)
    print(text)
    if (req.is_connected()):
        printText(text, size,req)
        print ("Print end")
        req.disconnect()
    else:
        print("BLE connect error")
    return

# ------------------------------------------------------------------------------
# imgFromString : Convert string to binary image
# ------------------------------------------------------------------------------
def imgFromString(s, fontSize):
    # Font choice
    font = ImageFont.truetype("dejavu/DejaVuSansMono.ttf", fontSize)
    # Convert inline text to multiline
    s = textwrap.fill (s, width = int(384/font.getsize("1")[0])) 
    # Get size of text
    size = font.getsize_multiline(s)
    # Fix height and width
    size_x = 384 if size[0] > 384 else size[0]
    size_y = font.getsize_multiline(s)[1]#font.getsize(s)[1]*(s.count('\n')+1)
    # Create image
    img = Image.new("RGB", size=(size_x, size_y+10), color="white")
    # Draw text in image
    draw = ImageDraw.Draw(img)
    draw.text((0, 0), s, (0, 0, 0), font=font)
    # Convert RGB image to binary image
    img = ImageOps.invert(img.convert('L'))
    img = img.convert('1')
    # Save image to file
    #img.save('img.png')
    return img

# ------------------------------------------------------------------------------
# binFromImg : Convert binary image to array
# ------------------------------------------------------------------------------
def binFromImg(img):
    binImg=[]
    for line in range (0,img.size[1]):
        binImg.append(''.join(format(byte, '08b') for byte in img.tobytes()[int(line*(img.size[0]/8)):int((line*(img.size[0]/8))+img.size[0]/8)]))
    return binImg

# ------------------------------------------------------------------------------
# dataCrc : Calcul hex CRC-8
# ------------------------------------------------------------------------------
def dataCrc(data):
    hash = crc8.crc8()
    hash.update(bytes.fromhex(data))
    return str(hash.hexdigest())

# ------------------------------------------------------------------------------
# binCount : Convert binary image to array of '0' and '1'
# ------------------------------------------------------------------------------
def binCount (binImg):
    trame=[]
    i=0
    #read Image line by line
    for line in binImg:
        nb_zero=0
        nb_one=0
        trame.append('')
        # Read line char by char
        for char in line:
            # Bit '0' process
            if char == '0':
                # Bit '1' before
                if nb_one!=0:
                    # Format '1' number to hex + 128 (First bit to print black)
                    trame[i]+='{:02x}'.format(128+nb_one)
                    nb_one=0
                # Max number is 127 (First bit color + 127 max  number = '0x7f')
                if nb_zero>126:
                    trame[i]+='{:02x}'.format(nb_zero)
                    nb_zero=0
                nb_zero += 1
            # Bit '1' process
            if char == '1':
                # Bit '0' before
                if nb_zero!=0:
                    # Format '0' number to hex
                    trame[i]+='{:02x}'.format(nb_zero)
                    nb_zero=0
                # Max number is 127 (First bit color + 127 max  number = '0xff')
                if nb_one>126:
                    trame[i]+='{:02x}'.format(128+nb_one)
                    nb_one=0
                nb_one += 1
        # End of trame. If '1' or '0' before process
        if nb_zero!=0:
            trame[i]+='{:02x}'.format(nb_zero)
        elif nb_one!=0:
            trame[i]+='{:02x}'.format(128+nb_one)
        i+=1
    return trame

# ------------------------------------------------------------------------------
# bleConnect : Connect to printer mac
# ------------------------------------------------------------------------------
def bleConnect(mac, device='hci0'):
    host = mac
    req = GATTRequester(host, False, device)
    req.connect(True)
    # Some config trame
    req.write_by_handle(0x09, bytes([1, 0]))
    time.sleep(0.02)
    req.write_by_handle(0x000e, bytes([1, 0]))
    time.sleep(0.02)
    req.write_by_handle(0x0011, bytes([2, 0]))
    time.sleep(0.02)
    req.exchange_mtu(83)
    time.sleep(0.02)
    req.write_cmd(0x0006, bytes([18, 81, 120, 168, 0, 1, 0, 0, 0, 255, 18, 81, 120, 163, 0, 1, 0, 0, 0, 255]))
    time.sleep(0.02)
    req.write_cmd(0x0006, bytes([18, 81, 120, 187, 0, 1, 0, 1, 7, 255]))
    time.sleep(0.02)
    req.write_cmd(0x0006, bytes([18, 81, 120, 163, 0, 1, 0, 0, 0, 255]))
    time.sleep(0.2)
    return req

# ------------------------------------------------------------------------------
# printData : Print text
# ------------------------------------------------------------------------------
def printText(text, size, req):
    data = binCount(binFromImg(imgFromString(text,size)))
    for dat in data:
        # Header of trame
        head = "5178bf00"
        # Format BT trame
        trame=head + '{:02x}'.format(len(bytes.fromhex(dat)),'x') + "00" + dat + dataCrc(dat) + "ff"
        print(trame)
        i = len(trame)
        # Pull 40 bytes trames
        while i > 0:
            if i > 40:
                req.write_cmd(0x06, bytes.fromhex(trame[len(trame)-i:len(trame)-i+40]))
                i -= 40
            else:
                req.write_cmd(0x06, bytes.fromhex(trame[len(trame)-i:len(trame)]))
                i -= 40
            time.sleep(0.01)
    # 90 dp moving forward paper
    forwardPaper(90,req)
    return

# ------------------------------------------------------------------------------
# forwardPaper : Moving forward
# ------------------------------------------------------------------------------
def forwardPaper(dp,req):
    head = "5178a100"
    data = '{:02x}'.format(dp) + '00'
    # Format BT trame
    trame=head + '{:02x}'.format(len(bytes.fromhex(data)),'x') + "00" + data + dataCrc(data) + "ff"
    req.write_cmd(0x06, bytes.fromhex(trame))
    time.sleep(0.01)
    return

# ------------------------------------------------------------------------------
# httpserver : Start HTTP server
# ------------------------------------------------------------------------------
class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_response()
        printer(post_data.decode('utf-8'),50 if not args.size else args.size)

def httpserver(server_class=HTTPServer, handler_class=S, port=8080,):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

# ------------------------------------------------------------------------------
# bleScan : Scan Bluetooth Low Energy devices
# ------------------------------------------------------------------------------
def bleScan(device="hci0"):
    service = DiscoveryService(device)
    devices = service.discover(2)
    for address, name in devices.items():
        print("name: {}, address: {}".format(name, address))

if __name__ == '__main__':
    if (args.BTMAC=="FIND"):
        bleScan(args.device if args.device else bleScan())
        sys.exit()
    if not (args.text or args.port):
        print("ERROR: Please specfiy text with -t or http port server with -p argument")
        sys.exit(1)
    if args.text:
        printer(args.text, 50 if not args.size else args.size)
    if args.port:
        httpserver(port=int(args.port))
