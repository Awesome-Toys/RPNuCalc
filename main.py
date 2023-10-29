# Initialize 
# Representing the node for the stack.
# The node class defines a constructor and the required getter and setter methods.
# rp2040 simulator https://wokwi.com/projects/new/micropython-pi-pico
# https://www.codeproject.com/Articles/5346603/Reverse-Polish-Notation-RPN-Calculator-in-Python


from machine import Pin, ADC, SoftSPI
import utime
import framebuf
from math import *
import math
import re

entry_mode = "Run"

entry_chr = ""

expr_offset = 0

usbled = Pin(25, Pin.OUT)
adc = ADC(Pin(29))

font58=[]
font58.append([0,0,0,0,0])
font58.append([62,91,79,91,62])
font58.append([62,107,79,107,62])
font58.append([28,62,124,62,28])
font58.append([24,60,126,60,24])
font58.append([28,87,125,87,28])
font58.append([28,94,127,94,28])
font58.append([0,24,60,24,0])
font58.append([255,231,195,231,255])
font58.append([0,24,36,24,0])
font58.append([255,231,219,231,255])
font58.append([48,72,58,6,14])
font58.append([38,41,121,41,38])
font58.append([64,127,5,5,7])
font58.append([64,127,5,37,63])
font58.append([90,60,231,60,90])
font58.append([127,62,28,28,8])
font58.append([8,28,28,62,127])
font58.append([20,34,127,34,20])
font58.append([95,95,0,95,95])
font58.append([6,9,127,1,127])
font58.append([0,102,137,149,106])
font58.append([96,96,96,96,96])
font58.append([148,162,255,162,148])
font58.append([8,4,126,4,8])
font58.append([16,32,126,32,16])
font58.append([8,8,42,28,8])
font58.append([8,28,42,8,8])
font58.append([30,16,16,16,16])
font58.append([12,30,12,30,12])
font58.append([48,56,62,56,48])
font58.append([6,14,62,14,6])
font58.append([0,0,0,0,0])
font58.append([0,0,95,0,0])
font58.append([0,7,0,7,0])
font58.append([20,127,20,127,20])
font58.append([36,42,127,42,18])
font58.append([35,19,8,100,98])
font58.append([54,73,86,32,80])
font58.append([0,8,7,3,0])
font58.append([0,28,34,65,0])
font58.append([0,65,34,28,0])
font58.append([42,28,127,28,42])
font58.append([8,8,62,8,8])
font58.append([0,128,112,48,0])
font58.append([8,8,8,8,8])
font58.append([0,0,96,96,0])
font58.append([32,16,8,4,2])
font58.append([62,81,73,69,62])
font58.append([0,66,127,64,0])
font58.append([114,73,73,73,70])
font58.append([33,65,73,77,51])
font58.append([24,20,18,127,16])
font58.append([39,69,69,69,57])
font58.append([60,74,73,73,49])
font58.append([65,33,17,9,7])
font58.append([54,73,73,73,54])
font58.append([70,73,73,41,30])
font58.append([0,0,20,0,0])
font58.append([0,64,52,0,0])
font58.append([0,8,20,34,65])
font58.append([20,20,20,20,20])
font58.append([0,65,34,20,8])
font58.append([2,1,89,9,6])
font58.append([62,65,93,89,78])
font58.append([124,18,17,18,124])
font58.append([127,73,73,73,54])
font58.append([62,65,65,65,34])
font58.append([127,65,65,65,62])
font58.append([127,73,73,73,65])
font58.append([127,9,9,9,1])
font58.append([62,65,65,81,115])
font58.append([127,8,8,8,127])
font58.append([0,65,127,65,0])
font58.append([32,64,65,63,1])
font58.append([127,8,20,34,65])
font58.append([127,64,64,64,64])
font58.append([127,2,28,2,127])
font58.append([127,4,8,16,127])
font58.append([62,65,65,65,62])
font58.append([127,9,9,9,6])
font58.append([62,65,81,33,94])
font58.append([127,9,25,41,70])
font58.append([38,73,73,73,50])
font58.append([3,1,127,1,3])
font58.append([63,64,64,64,63])
font58.append([31,32,64,32,31])
font58.append([63,64,56,64,63])
font58.append([99,20,8,20,99])
font58.append([3,4,120,4,3])
font58.append([97,89,73,77,67])
font58.append([0,127,65,65,65])
font58.append([2,4,8,16,32])
font58.append([0,65,65,65,127])
font58.append([4,2,1,2,4])
font58.append([64,64,64,64,64])
font58.append([0,3,7,8,0])
font58.append([32,84,84,120,64])
font58.append([127,40,68,68,56])
font58.append([56,68,68,68,40])
font58.append([56,68,68,40,127])
font58.append([56,84,84,84,24])
font58.append([0,8,126,9,2])
font58.append([24,164,164,156,120])
font58.append([127,8,4,4,120])
font58.append([0,68,125,64,0])
font58.append([32,64,64,61,0])
font58.append([127,16,40,68,0])
font58.append([0,65,127,64,0])
font58.append([124,4,120,4,120])
font58.append([124,8,4,4,120])
font58.append([56,68,68,68,56])
font58.append([252,24,36,36,24])
font58.append([24,36,36,24,252])
font58.append([124,8,4,4,8])
font58.append([72,84,84,84,36])
font58.append([4,4,63,68,36])
font58.append([60,64,64,32,124])
font58.append([28,32,64,32,28])
font58.append([60,64,48,64,60])
font58.append([68,40,16,40,68])
font58.append([76,144,144,144,124])
font58.append([68,100,84,76,68])
font58.append([0,8,54,65,0])
font58.append([0,0,119,0,0])
font58.append([0,65,54,8,0])
font58.append([2,1,2,4,2])
font58.append([60,38,35,38,60])
font58.append([30,161,161,97,18])
font58.append([58,64,64,32,122])
font58.append([56,84,84,85,89])
font58.append([33,85,85,121,65])
font58.append([34,84,84,120,66])
font58.append([33,85,84,120,64])
font58.append([32,84,85,121,64])
font58.append([12,30,82,114,18])
font58.append([57,85,85,85,89])
font58.append([57,84,84,84,89])
font58.append([57,85,84,84,88])
font58.append([0,0,69,124,65])
font58.append([0,2,69,125,66])
font58.append([0,1,69,124,64])
font58.append([125,18,17,18,125])
font58.append([240,40,37,40,240])
font58.append([124,84,85,69,0])
font58.append([32,84,84,124,84])
font58.append([124,10,9,127,73])
font58.append([50,73,73,73,50])
font58.append([58,68,68,68,58])
font58.append([50,74,72,72,48])
font58.append([58,65,65,33,122])
font58.append([58,66,64,32,120])
font58.append([0,157,160,160,125])
font58.append([61,66,66,66,61])
font58.append([61,64,64,64,61])
font58.append([60,36,255,36,36])
font58.append([72,126,73,67,102])
font58.append([43,47,252,47,43])
font58.append([255,9,41,246,32])
font58.append([192,136,126,9,3])
font58.append([32,84,84,121,65])
font58.append([0,0,68,125,65])
font58.append([48,72,72,74,50])
font58.append([56,64,64,34,122])
font58.append([0,122,10,10,114])
font58.append([125,13,25,49,125])
font58.append([38,41,41,47,40])
font58.append([38,41,41,41,38])
font58.append([48,72,77,64,32])
font58.append([56,8,8,8,8])
font58.append([8,8,8,8,56])
font58.append([47,16,200,172,186])
font58.append([47,16,40,52,250])
font58.append([0,0,123,0,0])
font58.append([8,20,42,20,34])
font58.append([34,20,42,20,8])
font58.append([85,0,85,0,85])
font58.append([170,85,170,85,170])
font58.append([255,85,255,85,255])
font58.append([0,0,0,255,0])
font58.append([16,16,16,255,0])
font58.append([20,20,20,255,0])
font58.append([16,16,255,0,255])
font58.append([16,16,240,16,240])
font58.append([20,20,20,252,0])
font58.append([20,20,247,0,255])
font58.append([0,0,255,0,255])
font58.append([20,20,244,4,252])
font58.append([20,20,23,16,31])
font58.append([16,16,31,16,31])
font58.append([20,20,20,31,0])
font58.append([16,16,16,240,0])
font58.append([0,0,0,31,16])
font58.append([16,16,16,31,16])
font58.append([16,16,16,240,16])
font58.append([0,0,0,255,16])
font58.append([16,16,16,16,16])
font58.append([16,16,16,255,16])
font58.append([0,0,0,255,20])
font58.append([0,0,255,0,255])
font58.append([0,0,31,16,23])
font58.append([0,0,252,4,244])
font58.append([20,20,23,16,23])
font58.append([20,20,244,4,244])
font58.append([0,0,255,0,247])
font58.append([20,20,20,20,20])
font58.append([20,20,247,0,247])
font58.append([20,20,20,23,20])
font58.append([16,16,31,16,31])
font58.append([20,20,20,244,20])
font58.append([16,16,240,16,240])
font58.append([0,0,31,16,31])
font58.append([0,0,0,31,20])
font58.append([0,0,0,252,20])
font58.append([0,0,240,16,240])
font58.append([16,16,255,16,255])
font58.append([20,20,20,255,20])
font58.append([16,16,16,31,0])
font58.append([0,0,0,240,16])
font58.append([255,255,255,255,255])
font58.append([240,240,240,240,240])
font58.append([255,255,255,0,0])
font58.append([0,0,0,255,255])
font58.append([15,15,15,15,15])
font58.append([56,68,68,56,68])
font58.append([252,74,74,74,52])
font58.append([126,2,2,6,6])
font58.append([2,126,2,126,2])
font58.append([99,85,73,65,99])
font58.append([56,68,68,60,4])
font58.append([64,126,32,30,32])
font58.append([6,2,126,2,2])
font58.append([153,165,231,165,153])
font58.append([28,42,73,42,28])
font58.append([76,114,1,114,76])
font58.append([48,74,77,77,48])
font58.append([48,72,120,72,48])
font58.append([188,98,90,70,61])
font58.append([62,73,73,73,0])
font58.append([126,1,1,1,126])
font58.append([42,42,42,42,42])
font58.append([68,68,95,68,68])
font58.append([64,81,74,68,64])
font58.append([64,68,74,81,64])
font58.append([0,0,255,1,3])
font58.append([224,128,255,0,0])
font58.append([8,8,107,107,8])
font58.append([54,18,54,36,54])
font58.append([6,15,9,15,6])
font58.append([0,0,24,24,0])
font58.append([0,0,16,16,0])
font58.append([48,64,255,1,1])
font58.append([0,31,1,1,30])
font58.append([0,25,29,23,18])
font58.append([0,60,60,60,60])
font58.append([23,29,4,124,4])

keyTimeOut = 0

keyName = [["f","y^x","C","7","8","9","*","/"],
           ["<<","x2","neg","4","5","6","+","-"],
           [">>","swap","0","1","2","3",".","ENTR"]]

keyNameAlt = [["f","Menu","ClrST","aSin","aCos","aTan","{f(x)dx","Solver"],
              ["rot","sqrt","E","Sin","Cos","Tan","Sto","Rcl"],
              ["d.r.g","1/x","ln","e^x","log","10^x","pi","LASTx"]]

angle_mode = "deg"

keypadRowPins = [4,3,2]
keypadColPins = [8,9,10,11,12,13,14,15]

spi_sck = machine.Pin(17, Pin.OUT)
spi_mosi = machine.Pin(16, Pin.OUT)
spi_miso = machine.Pin(21, Pin.IN)
spi_cs = machine.Pin(20, Pin.OUT)
spi_dc = machine.Pin(18, Pin.OUT)
spi_rst = machine.Pin(19, Pin.OUT)

#softSPI because when the processor is slowed to save power the hardware SPI stops working argh :(
spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=spi_sck, mosi=spi_mosi, miso=spi_miso)

LCDWIDTH = const(136)
LCDHEIGHT = const(32)

screenmem= bytearray((LCDWIDTH * LCDHEIGHT) // 8)

fbuf = framebuf.FrameBuffer(screenmem, LCDWIDTH, LCDHEIGHT, framebuf.MONO_VLSB)

lastx = float(0)

def init_lcd():
    CMD_DISPLAY_OFF = const(0xAE)
    CMD_DISPLAY_ON = const(0xAF)
    CMD_SET_DISP_START_LINE = const(0x40)
    CMD_SET_PAGE = const(0xB0)
    CMD_SET_COLUMN_UPPER = const(0x10)
    CMD_SET_COLUMN_LOWER = const(0x00)
    CMD_SET_ADC_NORMAL = const(0xA0)
    CMD_SET_ADC_REVERSE = const(0xA1)
    CMD_SET_DISP_NORMAL = const(0xA6)
    CMD_SET_DISP_REVERSE = const(0xA7)
    CMD_SET_ALLPTS_NORMAL = const(0xA4)
    CMD_SET_ALLPTS_ON = const(0xA5)
    CMD_SET_BIAS_9 = const(0xA2)
    CMD_SET_BIAS_7 = const(0xA3)
    CMD_INTERNAL_RESET = const(0xE2)
    CMD_SET_COM_NORMAL = const(0xC0)
    CMD_SET_COM_REVERSE = const(0xC8)
    CMD_SET_POWER_CONTROL = const(0x28)
    CMD_SET_RESISTOR_RATIO = const(0x20)
    CMD_SET_VOLUME_FIRST = const(0x81)
    CMD_SET_VOLUME_SECOND = const(0x00)
    CMD_SET_STATIC_OFF = const(0xAC)
    CMD_SET_STATIC_ON = const(0xAD)
    CMD_SET_STATIC_REG = const(0x00)
    spi_cs(False)
    spi_dc(False)
    spi_rst(True)
    reset_lcd()
    # Display start line select
    write_lcd_cmd(CMD_SET_DISP_START_LINE)
    # ADC set
    write_lcd_cmd(CMD_SET_ADC_NORMAL)
    # Common output mode select
    write_lcd_cmd(CMD_SET_COM_REVERSE)
    # Display normal/reverse
    write_lcd_cmd(CMD_SET_DISP_NORMAL)
    # LCD bias set
    write_lcd_cmd(CMD_SET_BIAS_9)
    # Power control set
    write_lcd_cmd(0x2f)
    # Booster ratio set
    write_lcd_cmd(0xf8)
    write_lcd_cmd(0x00)
    # V0 voltage regulator set
    write_lcd_cmd(0x23)
    # Electronic volume mode set contrast
    write_lcd_cmd(CMD_SET_VOLUME_FIRST)  
    write_lcd_cmd(0x5a) #5a #1f #1d
    # Satic indicator set
    write_lcd_cmd(0xac)
    write_lcd_cmd(0x00)
    # Display ON/OFF
    write_lcd_cmd(CMD_DISPLAY_ON)

def reset_lcd():
    # Toggle RST low to reset.
    spi_rst(True)
    spi_rst(False)
    spi_rst(True)

def write_lcd_cmd(cmd: int):
    #Send a command to the SPI device
    spi_dc(False)
    spi.write(bytearray([cmd]))  

def lcd_text(text, x, y):
    y=y*136
    for chra in text:
        ch=ord(chra)
        for xx in range(0,5):
            screenmem[y+x+xx]= screenmem[y+x+xx] ^ font58[ch][xx]
        x=x+6

def lcd_text_big(text, y):
    y=y*8
    x = 132-len(text)*8
    fbuf.text(text,x,y,1)

def lcd_show():
    write_lcd_cmd(CMD_SET_PAGE | 0)
    write_lcd_cmd(CMD_SET_COLUMN_LOWER)
    write_lcd_cmd(CMD_SET_COLUMN_UPPER)
    spi_dc(True)
    spi.write(screenmem[0:135])
    write_lcd_cmd(CMD_SET_PAGE | 1)
    write_lcd_cmd(CMD_SET_COLUMN_LOWER)
    write_lcd_cmd(CMD_SET_COLUMN_UPPER)
    spi_dc(True)
    spi.write(screenmem[136:271])
    write_lcd_cmd(CMD_SET_PAGE | 2)
    write_lcd_cmd(CMD_SET_COLUMN_LOWER)
    write_lcd_cmd(CMD_SET_COLUMN_UPPER)
    spi_dc(True)
    spi.write(screenmem[272:407])
    write_lcd_cmd(CMD_SET_PAGE | 3)
    write_lcd_cmd(CMD_SET_COLUMN_LOWER)
    write_lcd_cmd(CMD_SET_COLUMN_UPPER)
    spi_dc(True)
    spi.write(screenmem[408:543])
    
fcn = False
    
row = []
col = []
keypadState = [];
low_speed = False

for i in keypadRowPins:
    row.append(Pin(i,Pin.IN,Pin.PULL_UP))
    keypadState.append([0,0,0,0,0,0,0,0])
for i in keypadColPins:
    col.append(Pin(i,Pin.OUT))


def invert_mode():
    pass
#     for x in range(94, 112):
#         fbuf.pixel(x,0,not fbuf.pixel(x,0))
#         fbuf.pixel(x,7,not fbuf.pixel(x,7))
#     for y in range(1,7):
#         for x in range(93, 113):
#             fbuf.pixel(x,y,not fbuf.pixel(x,y))

vbat = adc.read_u16()/65535*4.4
def draw_bat():
    global vbat
    vbat = vbat *.9  + (adc.read_u16()/65535*4.4)/10
    if vbat > 3.05:
        lcd_text("USB", 115, 0)
    else:
        fbuf.rect(117,0,12,6,1)
        fbuf.rect(128,1,3,4,1)
        fbuf.vline(128,2,2,0)
        bat = float(vbat - 2)
        if bat < 0.0:
            bat = 0.0
        bat = bat * 14
        bat = int(bat)
        fbuf.fill_rect(117,1, bat, 4, 1)

def get_bat():
    global vbat
    vbat = vbat *.9  + (adc.read_u16()/65535*4.4)/10
    return round(float(vbat),2)

def setspeed():
    #check for the function key at startup if pressed then no power savings and USB enabled
    #if vbat is greater than 3.1 volts then assume USB powered
    global low_speed
    col[0].low()
    utime.sleep(0.005) #settling time
    pressed = not row[0].value()
    vbat = adc.read_u16()/65535*4.4
    if(vbat > 3.1):
        pressed = True
    if(not pressed):
        low_speed = True
        usbled.value(False)
    if(pressed):
        usbled.value(True)

def keypadRead():
    global row
    global fcn
    j_ifPressed = -1
    i_ifPressed = -1
    for i in range(0,len(col)):
        col[i].low()
        utime.sleep(0.005) #settling time
        for j in range(0,len(row)):
            if((j==0) and (i==0)):
                pressed = (not row[j].value())
            else:
                pressed = not row[j].value()
            if(pressed and (keypadState[j][i] != pressed)): #state changed to high
                keypadState[j][i] = pressed
            elif(not pressed and (keypadState[j][i] != pressed)): # state changed to low
                keypadState[j][i] = pressed
                j_ifPressed = j
                i_ifPressed = i
        col[i].high()
    if(j_ifPressed != -1 and i_ifPressed != -1):
        if(keyName[j_ifPressed][i_ifPressed] == "f"):
            fcn = not fcn
            if(fcn):
                return "f"
            else:
                return " "
        if(fcn):
            fcn = False
            return keyNameAlt[j_ifPressed][i_ifPressed]
        else:
            return keyName[j_ifPressed][i_ifPressed]
    else:
        return -1

setspeed()
init_lcd()

class Node:
   def __init__(self,d):
       self.data = d

   def setnext(self,n):
       self.next = n

   def getdata(self):
       return self.data

   def getnext(self):
       return self.next
       
# Representing the stack class.
# The stack class defines a constructor and the implementations for the
# push and pop operations. It also contains a method to check if the stack is empty.

class Stack:
    def __init__(self):
       self.top = None

    def push(self,d):
       self.newnode = Node(d)
       self.newnode.setnext(self.top)
       self.top = self.newnode

    def pop(self):
       temp = self.top
       self.top = self.top.getnext()
       n = temp.getdata()
       del temp
       return n

    def isempty(self):
       return self.top == None

    def display(self):
        if(self.top == None):
            return
        self.display_helper(self.top)

    def display_helper(self, current):
        if current is None:
            return
        print(f"ST:{str(current.data)}")
        self.display_helper(current.next)

    def countNode(self):
        temp = self.top
        cnt = 0
        while temp:
            cnt += 1
            temp = temp.next
        return cnt

    def rotate(self, k):
        if k == 0: 
            return 
        current = self.top
        count = 1 
        while(count <k and 
              current is not None):
            current = current.next
            count += 1
        if current is None:
            return
        kthNode = current 
        while(current.next is not None):
            current = current.next
        current.next = self.top
        self.top = kthNode.next
        kthNode.next = None

def gradFromRad(rad):
    return 200*rad/math.pi
def radFromGrad(grad):
    return math.pi*grad/200

def do_calc(expr): #main calculator functions
    global errstr, angle_mode, lastx
    try:
        elements = expr.split()
        for x in elements:
            if x == "+":
                n1 = mystack.pop()
                n2 = mystack.pop()
                n3 = n2 + n1
                mystack.push(n3)
            elif x == "pi":
                mystack.push(math.pi)
            elif x == "vbat":
                mystack.push(get_bat())
            elif x == "LASTx":
                mystack.push(lastx)
            elif x == "y^x":
                n1 = mystack.pop()
                n2 = mystack.pop()
                n3 = pow(n2, n1)
                mystack.push(n3)
            elif x == "-":
                n1 = mystack.pop()
                n2 = mystack.pop()
                n3 = n2 - n1
                mystack.push(n3)
            elif x == "*":
                n1 = mystack.pop()
                n2 = mystack.pop()
                n3 = n2 * n1
                mystack.push(n3)
            elif x == "/":
                n1 = mystack.pop()
                n2 = mystack.pop()
                n3 = n2 / n1
                mystack.push(n3)
            elif x == "swap":
                n1 = mystack.pop()
                n2 = mystack.pop()
                mystack.push(n1)
                mystack.push(n2)
            elif x == "x2":
                n1 = mystack.pop()
                n3 = n1 * n1
                mystack.push(n3)
            elif x == "10^x":
                n1 = mystack.pop()
                n3 = pow(10, n1)
                mystack.push(n3)
            elif x == "log":
                n1 = mystack.pop()
                n3 = log10(n1)
                mystack.push(n3)
            elif x == "ln":
                n1 = mystack.pop()
                n3 = log(n1)
                mystack.push(n3)
            elif x == "e^x":
                n1 = mystack.pop()
                n3 = pow(math.e , n1)
                mystack.push(n3)
            elif x == "sqrt":
                n1 = mystack.pop()
                n3 = sqrt(n1)
                mystack.push(n3)
            elif x == "1/x":
                n1 = mystack.pop()
                n3 = float('1') / n1
                mystack.push(n3)
            elif x == "Sin":
                n1 = mystack.pop()
                if angle_mode=="deg":  #d
                    n3 = sin(radians(n1))
                elif angle_mode=="grd": #g
                    n3 = sin(radFromGrad(n1))
                else:
                    n3 = sin(n1)
                mystack.push(n3)
            elif x == "Cos":
                n1 = mystack.pop()
                if angle_mode=="deg":  #d
                    n3 = cos(radians(n1))
                elif angle_mode=="grd": #g
                    n3 = cos(radFromGrad(n1))
                else:
                    n3 = cos(n1)
                mystack.push(n3)
            elif x == "Tan":
                n1 = mystack.pop()
                if angle_mode=="deg":  #d
                    n3 = tan(radians(n1))
                elif angle_mode=="grd": #g
                    n3 = tan(radFromGrad(n1))
                else:
                    n3 = tan(n1)
                mystack.push(n3)
            elif x == "aSin":
                n1 = mystack.pop()
                if angle_mode=="deg":  #d
                    n3 = degrees(asin(n1))
                elif angle_mode=="grd": #g 
                    n3 = gradFromRad(asin(n1))
                else:
                    n3 = asin(n1)
                mystack.push(n3)
            elif x == "aCos":
                n1 = mystack.pop()
                if angle_mode=="deg":  #d
                    n3 = degrees(acos(n1))
                elif angle_mode=="grd": #g 
                    n3 = gradFromRad(acos(n1))
                else:
                    n3 = acos(n1)
                mystack.push(n3)
            elif x == "aTan":
                n1 = mystack.pop()
                if angle_mode=="deg":  #d
                    n3 = degrees(atan(n1))
                elif angle_mode=="grd": #g
                    n3 = gradFromRad(atan(n1))
                else:
                    n3 = atan(n1)
                mystack.push(n3)
            elif x == "dup":
                if(not mystack.isempty()):
                    n1 = mystack.pop()
                    mystack.push(n1)
                    mystack.push(n1)
            elif x == "rot":
                if(not mystack.isempty()):
                    mystack.rotate(1)
            else:
                mystack.push(float(x))
                lastx = float(x)
    except:
        errstr = "Invalid Expression"

errstr = ""
displayWindowStart = 0
mystack = Stack()
expr = ""
dispstr = entry_chr

enter = False
fbuf.fill(0)
lcd_text_big('0.',1)
lcd_text(f"{chr(230)}Calc {entry_mode}",0,0)
tmp = f"{chr(255)}{mystack.countNode()} {angle_mode}"
lcd_text(tmp,112-6*len(tmp),0)
invert_mode()
draw_bat()
dispstr = " " * 48 + dispstr
lcd_text(dispstr[len(dispstr)-44:len(dispstr)-22],0,2)
lcd_text(dispstr[len(dispstr)-22:len(dispstr)-0],0,3)
lcd_show()

while True:       
    if(low_speed):
        machine.freq(10000000)

    key = -1
    
    while key == -1:
        key = keypadRead()

    if(low_speed):
        machine.freq(125000000)
   
    usbled.toggle()

    dispstr = entry_chr
    errstr = ""

#----------------------------------------------
#     print(f"START >{expr}<")
#     mystack.display()
#     print("-------------------------------")
#----------------------------------------------

    if(key == "ENTR") and (entry_mode == "Run"):
        if expr == "":
            enter = False
            do_calc("dup")
            expr = ""
            dispstr = entry_chr  
        else:
            enter = False
            do_calc(expr)
            expr = ""
            dispstr = entry_chr            

    elif(key == "ENTR") and (entry_mode == "PRG"):
        if(expr==""):
            expr = "dup "
        else:
            if(expr[len(expr)-1] != " "):
                expr =expr + " "
            else:
                expr = expr + "dup "
        dispstr = expr+entry_chr

    elif key == "<<":
        if expr_offset > 0:
            expr_offset = expr_offset - 1
        dispstr = expr+entry_chr
        
    elif key == ">>":
        if expr_offset <= len(expr)-44:
            expr_offset = expr_offset + 1
        dispstr = expr+entry_chr

    elif(key == "C"):
        enter = False
        if len(expr) > 0:
            expr = expr[0:len(expr)-1]
        else:
            if not mystack.isempty():
                result=mystack.pop()
        dispstr = expr+entry_chr

    elif(key == "ClrST"):
        dispstr = expr+entry_chr
        enter = False
        while(not mystack.isempty()):
             mystack.pop()
             
    elif(key == "d.r.g"):
        if angle_mode=="deg": 
            angle_mode="rad"
        elif angle_mode=="rad":
            angle_mode="grd"
        else:
            angle_mode="deg"
        dispstr = expr+entry_chr
        
    elif(key == "Menu"):
        if entry_mode=="Run":
            entry_mode="PRG"
        else:
            entry_mode="Run"
        dispstr = expr+entry_chr
        
    elif(key == "Rcl"):
        lst = expr.split()
        if len(lst) != 0:
            rcl = expr.split()[len(expr.split())-1]        
            try:
                elements = expr.split()
                expr = ""
                for x in range(0,len(elements)-1):
                    expr = expr + elements[x] + " "
                rcl = int(rcl)
                with open(f"SAVE{rcl}.TXT", "r") as f:
                    expr = expr + f.read() 
                    expr = expr + "" #no space after program
                f.close()
                dispstr = expr+entry_chr
            except:
                errstr = "NOT FOUND"
            enter = True
        else:
            errstr = "NO_ADDRESS"
    
    elif(key == "Solver"): # Impliments the Newton-Raphson method
        try:
            guess = mystack.pop()
            #here we do the actual solve
            lp_cnt = 0
            prec = float("1E-13")
            while lp_cnt < 500:
                mystack.push(guess) # add the guess to the stack
                do_calc(expr)# do the calculation with the guess
                fx = mystack.pop()
                mystack.push(guess + prec)
                do_calc(expr)# do the calculation with the guess + prec
                fxadd = mystack.pop()
                if abs(fx) < prec:
                    mystack.push(guess)
                    break
                v1 = prec * fx
                v2 = fxadd - fx
                if v2 == 0:
                    v2 = prec
                guess = guess - (v1 / v2)
                lp_cnt = lp_cnt + 1
            if lp_cnt >= 500:
                errstr = "No root found"
            #now cleanup after
            expr = ""
            dispstr = expr+entry_chr
        except:
            expr = ""
            errstr = "Invalid Expression"
            dispstr = expr+entry_chr

    elif(key == "{f(x)dx"): # Impliments the Simpson 1/3 Rule
        try:
            upper = float(mystack.pop())
            lower = float(mystack.pop())
            step_size = (upper - lower) / 8.0
            mystack.push(float(lower))
            do_calc(expr)
            mystack.push(float(upper))
            do_calc(expr)
            do_calc("+")
            integration = float(mystack.pop())
            for i in range(1, 8):
                k = lower + (step_size * i)
                mystack.push(float(k))
                do_calc(expr)
                if((i % 2) == 0):
                    integration = integration + (float(mystack.pop()) * 2.0)
                else:
                    integration = integration + (float(mystack.pop()) * 4.0)
            integration = integration * (step_size / 3.0)
            mystack.push(float(integration))
            #now cleanup after
            expr = ""
            dispstr = expr+entry_chr
        except:
            expr = ""
            errstr = "Invalid Expression"
            dispstr = expr+entry_chr
            
    elif(key == "Sto"):
        lst = expr.split()
        tmp = expr
        if len(lst) != 0:
            rcl = expr.split()[len(expr.split())-1]        
        try:
            elements = expr.split()
            expr = ""
            for x in range(0,len(elements)-1):
                expr = expr + elements[x] + " "
            
            rcl = int(rcl)
            with open(f"SAVE{rcl}.TXT", "w") as f:
                f.write(expr)
            f.close()
            dispstr = expr+entry_chr
        except:
            expr = tmp
            errstr = "NO_ADDRESS"
        enter = True
        
    elif(key == "f"):
        enter = False
        dispstr = expr+' FCN'
    
    elif(key in ['0','1','2','3','4','5','6','7','8','9',".","neg","E"]):
        if(key == "neg"):
            key = "-"
        expr =expr + key
        dispstr = expr+entry_chr
        enter = False
        
    else:
        expr =expr + " " + key    
        expr = re.sub(' +',' ',expr)
        expr =expr + " "
        dispstr = expr+entry_chr
        enter = True
        if entry_mode == "Run":
            enter = False
            do_calc(expr)
            expr = ""
            dispstr = expr+entry_chr

    if (key != "<<") and (key != ">>"):
        expr_offset = 0

    if not mystack.isempty():
        result=mystack.pop()
        mystack.push(result)
    else:
        result=float("0.0")
    
    if len(expr)< 44:
        expr_offset=0
        
    fbuf.fill(0)
    if(result==float("0.0")):
        lcd_text_big('0.',1)
    elif((fabs(result)<=float('0.00001')) or (fabs(result)>=float('1000000'))):
        txt=f"{result:9.9E}"
        lcd_text_big(txt,1)
    else:
        tmp_result = f"{result:14.15}"[0:16]
        print(f"{result}")
        #tmp_result=tmp_result.rstrip('0').rstrip('.') if '.' in tmp_result else tmp_result
        lcd_text_big(tmp_result,1)
    if errstr != "":
        lcd_text(errstr,0,0)
    else:    
        lcd_text(f"{chr(230)}Calc {entry_mode}",0,0)
        tmp = f"{chr(255)}{mystack.countNode()} {angle_mode}"
        lcd_text(tmp,112-6*len(tmp),0)
        invert_mode()
        draw_bat()
    dispstr = " " * 48 + dispstr
    lcd_text(dispstr[len(dispstr)-44-expr_offset:len(dispstr)-22-expr_offset],0,2)
    lcd_text(dispstr[len(dispstr)-22-expr_offset:len(dispstr)-0-expr_offset],0,3)
    lcd_show()
    usbled.toggle()

#----------------------------------------------
#     print(f"STOP >{expr}<")
#     mystack.display()
#     ccnntt = mystack.countNode()
#     print(f"cnt={ccnntt}")
#     print("-------------------------------")
#----------------------------------------------
