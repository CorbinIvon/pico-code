# *****************************************************************************
# * | File        :   Pico_ePaper_Organized-2.9.py
# * | Author      :   Corbin Meier
# * | Original    :   Waveshare team
# * | Function    :   Simplified Electronic paper driver
# * | Info        :   I have decided to modify the original driver to be smaller in terms of length.
# * ---------------------------------------------------------------------------
# * | This version:   V1.0
# * | Date        :   2024-03-09
# * | Info        :   Framework
# * | License     :   MIT License
# * | License src :   https://github.com/waveshareteam/Pico_ePaper_Code/blob/main/python/Pico_ePaper-2.9.py
# -----------------------------------------------------------------------------
from machine import Pin, SPI
import framebuf
import utime

RST_PIN     = 12
DC_PIN      = 8
CS_PIN      = 9
BUSY_PIN    = 13

WF_PARTIAL_2IN9 = [0x0,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x80,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x40,0x40,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x80,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0A,0x0,0x0,0x0,0x0,0x0,0x1,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x22,0x22,0x22,0x22,0x22,0x22,0x0,0x0,0x0,0x22,0x17,0x41,0xB0,0x32,0x36,]
WS_20_30 = [0x80,0x66,0x0,0x0,0x0,0x0,0x0,0x0,0x40,0x0,0x0,0x0,0x10,0x66,0x0,0x0,0x0,0x0,0x0,0x0,0x20,0x0,0x0,0x0,0x80,0x66,0x0,0x0,0x0,0x0,0x0,0x0,0x40,0x0,0x0,0x0,0x10,0x66,0x0,0x0,0x0,0x0,0x0,0x0,0x20,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x14,0x8,0x0,0x0,0x0,0x0,0x2,0xA,0xA,0x0,0xA,0xA,0x0,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x14,0x8,0x0,0x1,0x0,0x0,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x1,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x44,0x44,0x44,0x44,0x44,0x44,0x0,0x0,0x0,0x22,0x17,0x41,0x0,0x32,0x36]
Gray4 = [0x00,0x60,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x20,0x60,0x10,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x28,0x60,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x2A,0x60,0x15,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x90,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x02,0x00,0x05,0x14,0x00,0x00,0x1E,0x1E,0x00,0x00,0x00,0x00,0x01,0x00,0x02,0x00,0x05,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x24,0x22,0x22,0x22,0x23,0x32,0x00,0x00,0x00,0x22,0x17,0x41,0xAE,0x32,0x28]

class EPD_2in9(framebuf.FrameBuffer):
  def __init__(self, orientation=0):
    # An orientation of 0 is landscape. 1 is portrait.
    self.black = 0x00
    self.white = 0xff
    self.darkgray = 0xaa
    self.grayish = 0x55

    self.orientation = orientation
    self.reset_pin = Pin(RST_PIN, Pin.OUT)
    self.busy_pin = Pin(BUSY_PIN, Pin.IN, Pin.PULL_UP)
    self.cs_pin = Pin(CS_PIN, Pin.OUT)
    self.width = 128
    self.height = 296
    self.partial_lut = WF_PARTIAL_2IN9
    self.full_lut = WS_20_30
    self.Gray4_lut = Gray4
    self.spi = SPI(1)
    self.spi.init(baudrate=4000_000)
    self.dc_pin = Pin(DC_PIN, Pin.OUT)
    self.buffer = bytearray(self.height * self.width // 8)
    if self.orientation == 0:
      super().__init__(self.buffer, self.height, self.width, framebuf.MONO_VLSB)
    else:
      self.buffer_4Gray = bytearray(self.height * self.width // 4)
      self.image4Gray = framebuf.FrameBuffer(self.buffer_4Gray, self.width, self.height, framebuf.GS2_HMSB)
      super().__init__(self.buffer, self.width, self.height, framebuf.MONO_HLSB)
    self.init()
  def digital_write(self, pin, value):
    pin.value(value)
  def digital_read(self, pin):
    return pin.value()

  def delay_ms(self, delaytime):
    utime.sleep(delaytime / 1000.0)

  def spi_writebyte(self, data):
    self.spi.write(bytearray(data))

  def module_exit(self):
    self.digital_write(self.reset_pin, 0)

  # Hardware reset
  def reset(self):
    self.digital_write(self.reset_pin, 1)
    self.delay_ms(50)
    self.digital_write(self.reset_pin, 0)
    self.delay_ms(2)
    self.digital_write(self.reset_pin, 1)
    self.delay_ms(50)

  def send_command(self, command):
    self.digital_write(self.dc_pin, 0)
    self.digital_write(self.cs_pin, 0)
    self.spi_writebyte([command])
    self.digital_write(self.cs_pin, 1)

  def send_data(self, data):
    self.digital_write(self.dc_pin, 1)
    self.digital_write(self.cs_pin, 0)
    self.spi_writebyte([data])
    self.digital_write(self.cs_pin, 1)

  def send_data1(self, buf):
    self.digital_write(self.dc_pin, 1)
    self.digital_write(self.cs_pin, 0)
    self.spi.write(bytearray(buf))
    self.digital_write(self.cs_pin, 1)

  def ReadBusy(self):
    print("e-Paper busy")
    while(self.digital_read(self.busy_pin) == 1):    #  0: idle, 1: busy
      self.delay_ms(10)
    print("e-Paper busy release")

  def TurnOnDisplay(self):
    self.send_command(0x22) # DISPLAY_UPDATE_CONTROL_2
    self.send_data(0xC7)
    self.send_command(0x20) # MASTER_ACTIVATION
    self.ReadBusy()

  def TurnOnDisplay_Partial(self):
    self.send_command(0x22) # DISPLAY_UPDATE_CONTROL_2
    self.send_data(0x0F)
    self.send_command(0x20) # MASTER_ACTIVATION
    self.ReadBusy()

  def lut(self, lut):
    self.send_command(0x32)
    self.send_data1(lut[0:153])
    self.ReadBusy()

  def SetLut(self, lut):
    self.lut(lut)
    self.send_command(0x3f)
    self.send_data(lut[153])
    self.send_command(0x03)   # gate voltage
    self.send_data(lut[154])
    self.send_command(0x04)   # source voltage
    self.send_data(lut[155])  # VSH
    self.send_data(lut[156])  # VSH2
    self.send_data(lut[157])  # VSL
    self.send_command(0x2c)    # VCOM
    self.send_data(lut[158])

  def SetWindow(self, x_start, y_start, x_end, y_end):
    self.send_command(0x44) # SET_RAM_X_ADDRESS_START_END_POSITION
    # x point must be the multiple of 8 or the last 3 bits will be ignored
    self.send_data((x_start>>3) & 0xFF)
    self.send_data((x_end>>3) & 0xFF)
    self.send_command(0x45) # SET_RAM_Y_ADDRESS_START_END_POSITION
    self.send_data(y_start & 0xFF)
    self.send_data((y_start >> 8) & 0xFF)
    self.send_data(y_end & 0xFF)
    self.send_data((y_end >> 8) & 0xFF)

  def SetCursor(self, x, y):
    self.send_command(0x4E) # SET_RAM_X_ADDRESS_COUNTER
    self.send_data(x & 0xFF)

    self.send_command(0x4F) # SET_RAM_Y_ADDRESS_COUNTER
    self.send_data(y & 0xFF)
    self.send_data((y >> 8) & 0xFF)
    self.ReadBusy()

  def init(self):
    # EPD hardware init start
    self.reset()

    self.ReadBusy()
    self.send_command(0x12)  #SWRESET
    self.ReadBusy()

    self.send_command(0x01) #Driver output control
    self.send_data(0x27)
    self.send_data(0x01)
    self.send_data(0x00)

    self.send_command(0x11) #data entry mode

    if self.orientation == 0:
      self.send_data(0x07)
    else:
      self.send_data(0x03)

    self.SetWindow(0, 0, self.width-1, self.height-1)

    self.send_command(0x21) #  Display update control
    self.send_data(0x00)
    self.send_data(0x80)

    self.SetCursor(0, 0)
    self.ReadBusy()

    self.SetLut(self.full_lut)
    # EPD hardware init end
    return 0
  def init_4Gray(self):
    self.reset()

    self.ReadBusy()
    self.send_command(0x12)  #SWRESET
    self.ReadBusy()

    self.send_command(0x01) #Driver output control
    self.send_data(0x27)
    self.send_data(0x01)
    self.send_data(0x00)

    self.send_command(0x11) #data entry mode
    self.send_data(0x03)

    self.SetWindow(8, 0, self.width, self.height-1)

    self.send_command(0x3C)
    self.send_data(0x04)

    self.SetCursor(1, 0)
    self.ReadBusy()

    self.SetLut(self.Gray4_lut)
    # EPD hardware init end
    return 0
  def display(self, image):
    if (image == None):
      return
    self.send_command(0x24) # WRITE_RAM
    if self.orientation == 0:
      for j in range(int(self.width / 8) - 1, -1, -1):
        for i in range(0, self.height):
          self.send_data(image[i + j * self.height])
    else:
      self.send_data1(image)
    self.TurnOnDisplay()
  def display_Base(self, image):
    if (image == None):
      return
    self.send_command(0x24) # WRITE_RAM
    if self.orientation == 0:
      for j in range(int(self.width / 8) - 1, -1, -1):
        for i in range(0, self.height):
          self.send_data(image[i + j * self.height])
    else:
      self.send_data1(image)

    self.send_command(0x26) # WRITE_RAM
    if self.orientation == 0:
      for j in range(int(self.width / 8) - 1, -1, -1):
        for i in range(0, self.height):
          self.send_data(image[i + j * self.height])
    else:
      self.send_data1(image)
    self.TurnOnDisplay()
  def display_4Gray(self, image):
    self.send_command(0x24)
    for i in range(0, 4736):
      temp3=0
      for j in range(0, 2):
        temp1 = image[i*2+j]
        for k in range(0, 2):
          temp2 = temp1&0x03
          if(temp2 == 0x03):
            temp3 |= 0x00   # white
          elif(temp2 == 0x00):
            temp3 |= 0x01   # black
          elif(temp2 == 0x02):
            temp3 |= 0x00   # gray1
          else:   # 0x01
            temp3 |= 0x01   # gray2
          temp3 <<= 1

          temp1 >>= 2
          temp2 = temp1&0x03
          if(temp2 == 0x03):   # white
            temp3 |= 0x00
          elif(temp2 == 0x00):   # black
            temp3 |= 0x01
          elif(temp2 == 0x02):
            temp3 |= 0x00   # gray1
          else:   # 0x01
            temp3 |= 0x01   # gray2

          if (( j!=1 ) | ( k!=1 )):
            temp3 <<= 1
          temp1 >>= 2
      self.send_data(temp3)

    self.send_command(0x26)
    for i in range(0, 4736):
      temp3=0
      for j in range(0, 2):
        temp1 = image[i*2+j]
        for k in range(0, 2):
          temp2 = temp1&0x03
          if(temp2 == 0x03):
            temp3 |= 0x00   # white
          elif(temp2 == 0x00):
            temp3 |= 0x01   # black
          elif(temp2 == 0x02):
            temp3 |= 0x01   # gray1
          else:   # 0x01
            temp3 |= 0x00   # gray2
          temp3 <<= 1

          temp1 >>= 2
          temp2 = temp1&0x03
          if(temp2 == 0x03):   # white
            temp3 |= 0x00
          elif(temp2 == 0x00):   # black
            temp3 |= 0x01
          elif(temp2 == 0x02):
            temp3 |= 0x01   # gray1
          else:   # 0x01
            temp3 |= 0x00   # gray2
          if(j!=1 or k!=1):
            temp3 <<= 1
          temp1 >>= 2
      self.send_data(temp3)
    self.TurnOnDisplay()
  def display_Partial(self, image):
    if (image == None):
      return

    self.digital_write(self.reset_pin, 0)
    self.delay_ms(2)
    self.digital_write(self.reset_pin, 1)
    self.delay_ms(2)

    self.SetLut(self.partial_lut)
    self.send_command(0x37)
    self.send_data(0x00)
    self.send_data(0x00)
    self.send_data(0x00)
    self.send_data(0x00)
    self.send_data(0x00)
    self.send_data(0x40)
    self.send_data(0x00)
    self.send_data(0x00)
    self.send_data(0x00)
    self.send_data(0x00)

    self.send_command(0x3C) #BorderWaveform
    self.send_data(0x80)

    self.send_command(0x22)
    self.send_data(0xC0)
    self.send_command(0x20)
    self.ReadBusy()

    self.SetWindow(0, 0, self.width - 1, self.height - 1)
    self.SetCursor(0, 0)

    self.send_command(0x24) # WRITE_RAM
    if self.orientation == 0:
      for j in range(int(self.width / 8) - 1, -1, -1):
        for i in range(0, self.height):
          self.send_data(image[i + j * self.height])
    else:
      self.send_data1(image)
    self.TurnOnDisplay_Partial()

  def Clear(self, color):
    self.send_command(0x24) # WRITE_RAM
    self.send_data1([color] * self.height * int(self.width / 8))
    self.send_command(0x26) # WRITE_RAM
    self.send_data1([color] * self.height * int(self.width / 8))
    self.TurnOnDisplay()

  def sleep(self):
    self.send_command(0x10) # DEEP_SLEEP_MODE
    self.send_data(0x01)

    self.delay_ms(2000)
    self.module_exit()

########################################################################################
# MAIN
if __name__=='__main__':
  # Changing the parameter to 1 will make the display portrait. 0 (default) is landscape.
  epd = EPD_2in9(0)
  epd.Clear(0xff)
  epd.fill(0xff)
  epd.text("Waveshare & Corbin", 5, 10, 0x00)
  epd.text("Pico_ePaper-2.9", 5, 20, 0x00)
  epd.text("Raspberry Pico", 5, 30, 0x00)
  epd.display(epd.buffer)
  epd.delay_ms(2000)

  epd.vline(10, 40, 60, 0x00)
  epd.vline(120, 40, 60, 0x00)
  epd.hline(10, 40, 110, 0x00)
  epd.hline(10, 100, 110, 0x00)
  epd.line(10, 40, 120, 100, 0x00)
  epd.line(120, 40, 10, 100, 0x00)
  epd.display(epd.buffer)
  epd.delay_ms(2000)

  epd.rect(150, 5, 50, 55, 0x00)
  epd.fill_rect(150, 65, 50, 115, 0x00)
  epd.display_Base(epd.buffer)
  epd.delay_ms(2000)

  epd.init()
  epd.Clear(0xff)
  epd.delay_ms(2000)
  print("sleep")
  epd.sleep()