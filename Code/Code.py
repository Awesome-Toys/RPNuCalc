"""
MIT License

Copyright (c) 2023 Awesome-Toys

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import microcontroller
from jepler_udecimal import Decimal, getcontext, localcontext, utrig
# import jepler_udecimal.utrig
import board
import digitalio
import keypad
import DOGM132
import busio
import analogio

spi = busio.SPI(clock=board.GP10, MOSI=board.GP11)
dc = digitalio.DigitalInOut(board.GP12)
cs = digitalio.DigitalInOut(board.GP14)
reset = digitalio.DigitalInOut(board.GP13)
display = DOGM132.DOGM132(spi, dc, cs, reset)

batt_voltage = analogio.AnalogIn(board.A3)

row_pins = (board.GP26, board.GP27, board.GP28)
column_pins = (board.GP16, board.GP17, board.GP18, board.GP19, board.GP20, board.GP21, board.GP22, board.GP23)
km = keypad.KeyMatrix(row_pins, column_pins)

KEYCODES = [
    "f", "^", "B", "7", "8", "9", "*", "/",
    "r", "Q", "n", "4", "5", "6", "+", "-",
    "R", "~", "0", "1", "2", "3", ".", "\\" ]

KEYCODESalt = [
    "f",    "@",    "PGMC",    "S",    "D",    "T",    "INT",    "Solver",
    "PGM",    "q",    "e",    "s",    "c",    "t",    "sto",    "rcl",
    "R/S",    "N",    "l",    "L",    "X",    "P",    "p",    "B" ]

fcn = run = pgm_mode = False
dsp = True
pgm = []
bat = 0
pi_4 = Decimal("1.0").atan()

display.contrast = 90

display.fill(0)
display.rotation = 0
display.show()

def get_voltage():
    global bat
    raw = batt_voltage.value
    if bat == 0: bat = raw
    bat = bat - (bat / 100) + (raw / 100)
    x = (bat / 48)-256
    if x < 0: x=0
    if x > 100: x=100
    return x

def savepgm():
    global pgm
    microcontroller.nvm[0] = len(pgm)
    if len(pgm) > 0:
        for index in range(len(pgm)):
            microcontroller.nvm[index + 1] = ord(pgm[index])
    pstack(f"{len(pgm)}b saved")


def loadpgm():
    global pgm
    top_mem = microcontroller.nvm[0]
    if top_mem > 0:
        pgm = []
        for index in range(top_mem):
            pgm.append(chr(microcontroller.nvm[index + 1]))
    pstack(f"{len(pgm)}b loaded")


def extraprec(num=0):
    def inner(fn):
        def wrapper(*args, **kw):
            with localcontext() as ctx:
                ctx.prec = ctx.prec + 13 + (ctx.prec * num)
                result = fn(*args, **kw)
            return +result

        return wrapper

    return inner


class AngleConvert:
    def __init__(self):
        self.state = 0

    def next_state(self):
        self.state = (self.state + 1) % 3

    def __str__(self):
        return "degradgrd"[self.state * 3 : (self.state * 3) + 3]

    @property
    def factor(self):
        return [360, None, 400][self.state]

    @extraprec(num=1)
    def from_user(self, x):
        global pi_4
        factor = self.factor
        if factor is None:
            return x
        x = x.remainder_near(factor)
        return x * pi_4 * 8 / factor

    @extraprec(num=1)
    def to_user(self, x):
        global pi_4
        factor = self.factor
        if factor is None:
            return x
        return x * factor / pi_4 / 8

    @extraprec(num=1)
    def cos(self, x):
        return self.from_user(x).cos()

    @extraprec(num=1)
    def sin(self, x):
        return self.from_user(x).sin()

    @extraprec(num=1)
    def tan(self, x):
        return self.from_user(x).tan()

    @extraprec(num=1)
    def acos(self, x):
        return self.to_user(x.acos())

    @extraprec(num=1)
    def asin(self, x):
        return self.to_user(x.asin())

    @extraprec(num=1)
    def atan(self, x):
        return self.to_user(x.atan())


getcontext().prec = 14
getcontext().Emax = 99
getcontext().Emin = -99


def r_s():
    global pgm_mode, fcn, run, pgm, dsp
    if len(pgm) > 0:
        if entry:
            docalc("\\")
        pstack("Running")
        dsp = False
        for index in range(len(pgm)):
            docalc(pgm[index])
        dsp = True
        pstack("Stopped")
    else:
        pstack("No PGM")
    display.show()


def solver():  # Impliments the Newton-Raphson method
    global pgm_mode, fcn, run, pgm, dsp
    if entry:
        docalc("\\")
    if len(pgm) == 0:
        pstack("No PGM")
        return
    if len(stack) < 1:
        pstack("Arguments")
        return
    pstack("Solver")
    dsp = False
    guess = stack.pop()
    prec = Decimal("1E-13")
    lp_cnt = 0
    while lp_cnt < 500:
        stack.append(guess)
        for index in range(len(pgm)):
            docalc(pgm[index])
        fx = stack.pop()
        stack.append(guess + prec)
        for index in range(len(pgm)):
            docalc(pgm[index])
        fxadd = stack.pop()
        if abs(fx) < prec:
            stack.append(guess)
            break
        v1 = prec * fx
        v2 = fxadd - fx
        if v2 == 0:
            v2 = prec
        guess = guess - (v1 / v2)
        lp_cnt = lp_cnt + 1
    dsp = True
    if lp_cnt < 500:
        pstack("Finished")
    else:
        pstack("Not found")


def intergrate():  # Simpson 1/3 Rule
    global pgm_mode, fcn, run, pgm, dsp
    if entry:
        docalc("\\")
    if len(pgm) == 0:
        pstack("No PGM")
        return
    if len(stack) < 2:
        pstack("Arguments")
        return
    pstack("Integrating")
    dsp = False
    upper = stack.pop()
    lower = stack.pop()
    step_size = (upper - lower) / Decimal("8.0")
    stack.append(lower)
    for index in range(len(pgm)):
        docalc(pgm[index])
    stack.append(upper)
    for index in range(len(pgm)):
        docalc(pgm[index])
    docalc("+")
    integration = stack.pop()
    for i in range(1, 8):
        k = lower + (step_size * i)
        stack.append(Decimal(k))
        for index in range(len(pgm)):
            docalc(pgm[index])
        if i % 2 == 0:
            integration = integration + (stack.pop() * Decimal("2.0"))
        else:
            integration = integration + (stack.pop() * Decimal("4.0"))
    integration = integration * (step_size / Decimal("3.0"))
    stack.append(integration)
    dsp = True
    pstack("Stopped")


def getch():
    global pgm_mode, fcn, run, pgm, dsp
    while True:
        event = km.events.get()
        if event:
            if event.pressed:
                key_number = event.key_number
                if key_number == 0:
                    fcn = not fcn
                    display.fill_rect(125, 0, 7, 8, 0)
                    if fcn is True:
                        display.fill_rect(125, 0, 7, 8, 1)
                        display.pixel(125, 0, 0)
                        display.pixel(125, 7, 0)
                        display.pixel(131, 0, 0)
                        display.pixel(131, 7, 0)
                        display.text("f", 125, 0, 0)
                    display.show()
                if key_number > 0:
                    if fcn:
                        c = KEYCODESalt[key_number]
                    else:
                        c = KEYCODES[key_number]
                    fcn = False
                    display.fill_rect(125, 0, 7, 8, 0)
                    display.show()
                    if c == "sto":
                        savepgm()
                    elif c == "rcl":
                        loadpgm()
                    elif c == "PGMC":
                        pgm = []
                        pgm_mode = False
                        pstack("PGM cleared")
                    elif c == "PGM":
                        pgm_mode = not pgm_mode
                        display.fill_rect(118, 0, 7, 8, 0)
                        if pgm_mode:
                            display.fill_rect(118, 0, 7, 8, 1)
                            display.pixel(118, 0, 0)
                            display.pixel(118, 7, 0)
                            display.pixel(124, 0, 0)
                            display.pixel(124, 7, 0)
                            display.text("p", 119, -1, 0)
                        display.show()
                    elif c == "R/S":
                        r_s()
                    elif c == "Solver":
                        solver()
                    elif c == "INT":
                        intergrate()
                    elif pgm_mode:
                        pgm.append(c)
                    return c


stack = []
entry = []


def do_op(arity, fun):
    if arity > len(stack):
        return "underflow"
    res = fun(*stack[-arity:][::-1])
    del stack[-arity:]
    if isinstance(res, list):
        stack.extend(res)
    elif res is not None:
        stack.append(res)
    return None


angleconvert = AngleConvert()


def roll():
    stack[:] = stack[1:] + stack[:1]


def rroll():
    stack[:] = stack[-1:] + stack[:-1]


def swap():
    stack[-2:] = [stack[-1], stack[-2]]


def pi():
    pi_4 = Decimal("1.0").atan() * 4
    stack.append(pi_4)


ops = {
    "#": (2, lambda x, y: y ** (1 / x)),
    "*": (2, lambda x, y: y * x),
    "+": (2, lambda x, y: y + x),
    "-": (2, lambda x, y: y - x),
    "/": (2, lambda x, y: y / x),
    "^": (2, lambda x, y: y ** x),
    "v": (2, lambda x, y: y ** (1 / x)),
    "@": angleconvert.next_state,
    "D": (1, angleconvert.acos),
    "c": (1, angleconvert.cos),
    "L": (1, Decimal.exp),
    "l": (1, Decimal.ln),
    "q": (1, lambda x: x ** Decimal("0.5")),
    "r": roll,
    "R": rroll,
    "S": (1, angleconvert.asin),
    "s": (1, angleconvert.sin),
    "~": swap,
    "T": (1, angleconvert.atan),
    "t": (1, angleconvert.tan),
    "n": (1, lambda x: -x),
    "N": (1, lambda x: 1 / x),
    "Q": (1, lambda x: x * x),
    "p": pi,
    "X": (1, Decimal.log10),
    "P": (1, lambda x: 10 ** x),
}


def pstack(msg):
    if dsp:
        bat_percent = get_voltage()
        display.rotation = 0
        display.fill_rect(21, 0, 96, 8, 0)
        display.fill_rect(0, 0, 20, 8, 1)
        display.pixel(0, 0, 0)
        display.pixel(0, 7, 0)
        display.pixel(19, 0, 0)
        display.pixel(19, 7, 0)
        display.text(f"{angleconvert}", 1, 0, 0)
        display.text(f"{msg}", 23, 0, 1)
        display.text(f"{bat_percent:3.0f}%", 96, 0, 1)
        for i in range(2, 4):
            if len(stack) > 3 - i:
                val = stack[-4 + i]
                if val == Decimal("0"):
                    val = "0"
            else:
                val = ""
            display.fill_rect(0, 9 + ((i - 2) * 8), 132, 8, 0)
            display.text(
                "YX"[i - 2]
                + " "
                + f'{str(val).rstrip("0").rstrip(".") if "." in str(val) else val}',
                0,
                9 + ((i - 2) * 8),
                1,
            )
        display.show()


def docalc(c):
    do_pstack = False
    do_pentry = False
    message = ""
    
    if c in "B":
        if entry:
            entry.pop()
            do_pentry = True
        elif stack:
            stack.pop()
            do_pstack = True
    elif c == "n" and len(entry) > 0:
        if "e" in entry:
            if entry[entry.index("e") + 1] == "-":
                del entry[entry.index("e") + 1]
            else:
                entry.insert(entry.index("e") + 1, "-")
        else:
            if entry[0] == "-":
                del entry[0]
            else:
                entry.insert(0, "-")
        do_pentry = True
    elif c in "0123456789.eE":
        if c == "." and "." in entry:
            c = "e"
        entry.append(c)
        do_pentry = True
    elif c in "\\":
        if entry:
            try:
                stack.append(Decimal("".join(entry)))
            except Exception as e:
                message = str(e)
            del entry[:]
        elif c == "\\" and stack:
            stack.append(stack[-1])
        do_pstack = True
    elif c in ops:
        if entry:
            try:
                stack.append(Decimal("".join(entry)))
            except Exception as e:
                message = str(e)
            del entry[:]
        op = ops.get(c)
        try:
            if callable(op):
                message = op() or ""
            else:
                message = do_op(*op) or ""
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception as e:
            message = str(e)
        do_pstack = True

    if do_pstack:
        pstack(message)
        do_pentry = True

    if do_pentry:
        if dsp:
            display.fill_rect(0, 25, 132, 7, 0)
            display.text("> " + "".join(entry) + "_", 0, 25, 1)
            display.show()


def loop():
    display.fill(0)
    display.rotation = 0
    display.show()
    pstack("RPN" + chr(230) + "Calc")
    display.fill_rect(0, 25, 132, 8, 0)
    display.text("> " + "".join(entry) + "_", 0, 25, 1)
    display.show()
    get_voltage()
    while True:
        docalc(getch())


try:
    loop()
finally:
    pass
