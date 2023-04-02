"""
`DOGM132`
====================================================

A display control library for DOGM132 graphic displays

Implementation Notes
--------------------

**Hardware:**

* `DOGM132 graphic display

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

import time
from micropython import const
from adafruit_bus_device import spi_device

try:
    from typing import Optional
    from digitalio import DigitalInOut
    from busio import SPI
except ImportError:
    pass

try:
    import framebuf
except ImportError:
    import adafruit_framebuf as framebuf

__version__ = "0.0.0+auto.0"
__repo__ = "DOGM132"


class DOGM132(framebuf.FrameBuffer):
    """DOGM132 LCD display."""

    # pylint: disable=too-many-instance-attributes

    LCDWIDTH = const(136)
    LCDHEIGHT = const(32)

    # LCD Start Bytes
    start_bytes = 0

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

    def __init__(
        self,
        spi: SPI,
        dc_pin: DigitalInOut,
        cs_pin: DigitalInOut,
        reset_pin: Optional[DigitalInOut] = None,
        *,
        contrast: int = 0,
        baudrate: int = 1000000
    ) -> None:
        self._dc_pin = dc_pin
        dc_pin.switch_to_output(value=False)

        self.spi_device = spi_device.SPIDevice(spi, cs_pin, baudrate=baudrate)

        self._reset_pin = reset_pin
        if reset_pin:
            reset_pin.switch_to_output(value=True)

        self.buffer = bytearray(self.LCDHEIGHT * self.LCDWIDTH)
        super().__init__(self.buffer, self.LCDWIDTH, self.LCDHEIGHT)

        self._contrast = None
        self._invert = False

        self.reset()
        
        # Display start line select
        self.write_cmd(self.CMD_SET_DISP_START_LINE)
        # ADC set
        self.write_cmd(self.CMD_SET_ADC_REVERSE)
        # Common output mode select
        self.write_cmd(self.CMD_SET_COM_NORMAL)
        # Display normal/reverse
        self.write_cmd(self.CMD_SET_DISP_NORMAL)
        # LCD bias set
        self.write_cmd(self.CMD_SET_BIAS_9)
        # Power control set
        self.write_cmd(0x2f)
        # Booster ratio set
        self.write_cmd(0xf8)
        self.write_cmd(0x00)
        # V0 voltage regulator set
        self.write_cmd(0x23)
        # Electronic volume mode set contrast
        self.write_cmd(0x81)
        self.write_cmd(0x1f)
        # Satic indicator set
        self.write_cmd(0xac)
        self.write_cmd(0x00)
        # Display ON/OFF
        self.write_cmd(self.CMD_DISPLAY_ON)
        
    def reset(self) -> None:
        """Reset the display"""
        if self._reset_pin:
            # Toggle RST low to reset.
            self._reset_pin.value = False
            time.sleep(0.1)
            self._reset_pin.value = True
            time.sleep(0.1)

    def write_cmd(self, cmd: int) -> None:
        """Send a command to the SPI device"""
        self._dc_pin.value = False
        with self.spi_device as spi:
            spi.write(bytearray([cmd]))  # pylint: disable=no-member

# Ascii printer for very small framebufs!
    def print_buffer(self):
        print(self.buffer[0:4224])
        
    def show(self) -> None:
        page = 0
        self.write_cmd(self.CMD_SET_PAGE | 0)
        self.write_cmd(self.CMD_SET_COLUMN_LOWER)
        self.write_cmd(self.CMD_SET_COLUMN_UPPER)
        self._dc_pin.value = True
        with self.spi_device as spi:
            spi.write(self.buffer[0:132])
        page = 1
        self.write_cmd(self.CMD_SET_PAGE | 1)
        self.write_cmd(self.CMD_SET_COLUMN_LOWER)
        self.write_cmd(self.CMD_SET_COLUMN_UPPER)
        self._dc_pin.value = True
        with self.spi_device as spi:
            spi.write(self.buffer[136:268])
        page = 2
        self.write_cmd(self.CMD_SET_PAGE | 2)
        self.write_cmd(self.CMD_SET_COLUMN_LOWER)
        self.write_cmd(self.CMD_SET_COLUMN_UPPER)
        self._dc_pin.value = True
        with self.spi_device as spi:
            spi.write(self.buffer[272:404])
        page = 3
        self.write_cmd(self.CMD_SET_PAGE | 3)
        self.write_cmd(self.CMD_SET_COLUMN_LOWER)
        self.write_cmd(self.CMD_SET_COLUMN_UPPER)
        self._dc_pin.value = True
        with self.spi_device as spi:
            spi.write(self.buffer[408:540])
           
    @property
    def invert(self) -> bool:
        """Whether the display is inverted, cached value"""
        return self._invert

    @invert.setter
    def invert(self, val: bool) -> None:
        """Set invert on or normal display on"""
        self._invert = val
        if val:
            self.write_cmd(self.CMD_SET_DISP_REVERSE)
        else:
            self.write_cmd(self.CMD_SET_DISP_NORMAL)

    @property
    def contrast(self) -> int:
        """The cached contrast value"""
        return self._contrast

    @contrast.setter
    def contrast(self, val: int) -> None:
        """Set contrast to specified value (should be 0-127)."""
        self._contrast = max(0, min(val, 0x7F))  # Clamp to values 0-0x7f
        self.write_cmd(self.CMD_SET_VOLUME_FIRST)
        self.write_cmd(self.CMD_SET_VOLUME_SECOND | (self._contrast & 0x3F))
