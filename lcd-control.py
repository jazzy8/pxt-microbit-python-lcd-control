from microbit import *
uart.init(9600, tx=pin15, rx=pin14)

display.off()
pin4.write_analog(1023)
pin3.write_analog(767)

# pin connections
rs = pin0
enable = pin1
datapins = [pin8, pin12, pin2, pin13]


# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL = 0x08
LCD_CURSORSHIFT = 0x10
LCD_FUNCTIONSET = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80


# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00


# flags for display on/off control
LCD_DISPLAYON = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON = 0x02
LCD_CURSOROFF = 0x00
LCD_BLINKON = 0x01
LCD_BLINKOFF = 0x00


# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE = 0x00
LCD_MOVERIGHT = 0x04
LCD_MOVELEFT = 0x00


# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE = 0x08
LCD_1LINE = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS = 0x00




def InitDisplay():
    # at least 50ms after power on
    sleep(50)
    # send rs, enable low - rw is tied to GND
    rs.write_digital(0)
    enable.write_digital(0)
    write4bits(0x03)
    sleep(5)
    write4bits(0x03)
    sleep(5)
    write4bits(0x03)
    sleep(2)
    write4bits(0x02)
    send(LCD_FUNCTIONSET | 0x08, 0)
    sleep(5)
    send(LCD_FUNCTIONSET | 0x08, 0)
    sleep(2)
    send(LCD_FUNCTIONSET | 0x08, 0)
    sleep(2)
    send(LCD_FUNCTIONSET | 0x08, 0)
    sleep(2)
    send(LCD_DISPLAYCONTROL | LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF,0)
    clear()
    send(LCD_ENTRYMODESET | LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT,0)
     
# high level commands    
def clear():
    send(LCD_CLEARDISPLAY,0)
    sleep(2)


def home():
    send(LCD_RETURNHOME,0)
    sleep(2)


def setCursor(col, row):
    orpart = col
    if row>0:
        orpart = orpart + 0x40
    send(LCD_SETDDRAMADDR | orpart, 0)


def showText(t):
    for c in t:
        send(ord(c), 1)


# mid and low level commands        
def send(value, mode):
    rs.write_digital(mode)
    write4bits(value>>4)
    write4bits(value)
    
def pulseEnable():
    enable.write_digital(0)
    sleep(1)
    enable.write_digital(1)
    sleep(1)
    enable.write_digital(0)
    sleep(1)


def write4bits(value):
    for i in range(0,4):
        datapins[i].write_digital((value>>i) & 0x01)
    pulseEnable()


# Test    
InitDisplay()



def onebytetofour(nl):
    nl = nl + 1
    nl = int(nl * 4)
    nl = nl - 1
    return nl


def scrollOnDisplay(text, wait):
    clear()
    sleep(2)
    if len(text) > 16:
        p = 0
        for l in text:
            clear()
            sleep(2)
            l16 = p + 17
            showText(text[p:l16])
            sleep(wait)
            p += 1
    else:
        showText(text)



while True:
    if uart.any():
        t = uart.read()
        iic = str(t, "UTF-8")
        '''
        scrollOnDisplay(iic, 500)
        '''
        if iic.startswith("cls::all"):
            clear()
        elif iic.startswith("shw::"):
            showText(iic[5:])
        elif iic.startswith("cur::"):
            setCursor(int(iic[5:7]), int(iic[8]))
        elif iic.startswith("bkl::"):
            bkl = int(iic[5:])
            rbk = onebytetofour(bkl)
            pin4.write_analog(rbk)
        elif iic.startswith("cnt::"):
            cnt = int(iic[5:])
            rct = onebytetofour(cnt)
            pin3.write_analog(rct)
