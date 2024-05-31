#!/usr/bin/python

## @file   keyActions.py
#  @brief  Key-Stroke Action File
#  @date   Feb 25, 2016
#  @author Firesh Bakhda <firesh.bakhda@intel.com>, Wan Arif, Wan Abdul Hakim B <wan.abdul.hakim.b.wan.arif@intel.com>
#  @Modified Chu Wai Kitx <wai.kitx.chu@intel.com>, Teh Wei Loonx <wei.loonx.teh@intel.com>

import os
import string
import time
import datetime

class KeyStrokeError(Exception):
    def __init__(self, message):
        """Custom exception for KeyStroke Activity"""

        self.message = message
        super(KeyStrokeError, self).__init__(message)


class keyActions():

    time_t = 1.5
    _usbKeyMap = { "KEY_A":"0x04","KEY_B":"0x05","KEY_C":"0x06",
                   "KEY_D":"0x07","KEY_E":"0x08","KEY_F":"0x09",
                   "KEY_G":"0x0A","KEY_H":"0x0B","KEY_I":"0x0C",
                   "KEY_J":"0x0D","KEY_K":"0x0E","KEY_L":"0x0F",
                   "KEY_M":"0x10","KEY_N":"0x11","KEY_O":"0x12",
                   "KEY_P":"0x13","KEY_Q":"0x14","KEY_R":"0x15",
                   "KEY_S":"0x16","KEY_T":"0x17","KEY_U":"0x18",
                   "KEY_V":"0x19","KEY_W":"0x1A","KEY_X":"0x1B",
                   "KEY_Y":"0x1C","KEY_Z":"0x1D",

                   "KEY_1":"0x1E","KEY_2":"0x1F","KEY_3":"0x20",
                   "KEY_4":"0x21","KEY_5":"0x22","KEY_6":"0x23",
                   "KEY_7":"0x24","KEY_8":"0x25","KEY_9":"0x26",
                   "KEY_0":"0x27",
               
                   "KEY_ENTER":"0x28","KEY_ESC":"0x29","KEY_BACKSPACE":"0x2A",
                   "KEY_TAB":"0x2B","KEY_SPACE":"0x2C","KEY_MINUS":"0x2D",
                   "KEY_EQUAL":"0x2E","KEY_LEFT_BRACE":"0x2F","KEY_RIGHT_BRACE":"0x30",
                   "KEY_BACKSLASH":"0x31","KEY_NUMBER":"0x32","KEY_SEMICOLON":"0x33",
                   "KEY_QUOTE":"0x34","KEY_TILDE":"0x35","KEY_COMMA":"0x36",
                   "KEY_PERIOD":"0x37","KEY_SLASH":"0x38","KEY_CAPS_LOCK":"0x39",
                   "KEY_PRINTSCREEN":"0x46","KEY_SCROLL_LOCK":"0x47","KEY_PAUSE":"0x48",
                   "KEY_INSERT":"0x49","KEY_HOME":"0x4A","KEY_PAGE_UP":"0x4B",
                   "KEY_DELETE":"0x4C","KEY_END":"0x4D","KEY_PAGE_DOWN":"0x4E",
                   "KEY_RIGHT":"0x4F","KEY_LEFT":"0x50","KEY_DOWN":"0x51",
                   "KEY_UP":"0x52","KEY_NUM_LOCK":"0x53",
                
                   "KEY_F1":"0x3A","KEY_F2":"0x3B","KEY_F3":"0x3C",
                   "KEY_F4":"0x3D","KEY_F5":"0x3E","KEY_F6":"0x3F",
                   "KEY_F7":"0x40","KEY_F8":"0x41","KEY_F9":"0x42",
                   "KEY_F10":"0x43","KEY_F11":"0x44","KEY_F12":"0x45",
               
                 }

    _uartKeyMap = { "KEY_F2":"\x1B\x5B\x31\x32\x7E",
                    "KEY_DOWN":"\x1B\x5B\x42",
                    "KEY_UP":"\x1B\x5B\x41",
                    "KEY_ENTER":"\x0D",
                  }

    def __init__(self,_io_type):
        
        self.io_type = _io_type
        if self.io_type == "usb":
           self._keyMap = self._usbKeyMap
        elif self.io_type == "uart":
           self._keyMap = self._uartKeyMap
        else:
           raise KeyStrokeError("Unknown io type " + self.io_type + ", only [usb|uart] io type is supported")
        

    def log_file(self,message):
        
        with open('/teensy_keystroke.log','a') as write_msg:
            current_datetime = datetime.datetime.now()
            write_msg.write("["+str(current_datetime) +"] : "+ message + "\n")

    ##   @param "{string} num" Integer number of times F2 should be pressed
    ##   @param "{int}{float} t" Integer/Float number seconds to delay
    ##   @note Default t=0.5
    ##   @returns {void}
    ##   @brief Sends F2 key via USB
    def sendKey(self, _key, num=1, t=time_t, shift=False):

        try:
            if shift:
                key = "^" + self._keyMap[_key]
            else:
                key = "~" + self._keyMap[_key]
        except KeyError:
            raise KeyStrokeError("unknown " + _key + " key as argument")
            
        if num > 0:
            for i in range(0, num):
                time.sleep(t)
                if os.system("echo '" + key + "' > /dev/ttyUSB0"):
                    self.log_file("Failed to send " + _key + " key")
                    raise KeyStrokeError("Failed to send " + _key + " key")
                self.log_file(_key + " pressed")
        else:
            self.log_file("Invalid repetition value for " + _key + " key")
            raise KeyStrokeError("Invalid repetition value for " + _key + " key")
    
    ##   @param "{string} str" Any string to be sent via USB
    ##   @param "{int}{float} t" Integer/Float number seconds to delay
    ##   @note Default t=0.5
    ##   @returns {void}
    ##   @brief Sends key-strokes to remote machine via USB
    def customKey(self,data, t=0.5):

        if self.io_type == "uart":
           raise KeyStrokeError("io type " + self.io_type + " is not supported to run this method")

        datalist = list(data)
        lowercase = list(string.ascii_lowercase)
        uppercase = list(string.ascii_uppercase)
        digits = list(string.digits)
        digits.insert(len(digits) - 1,digits.pop(0))
        symbol = list('!@#$%^&*()-.:/_ \\')
        symbolHex = ['^0x1E','^0x1F','^0x20','^0x21','^0x22','^0x23','^0x24','^0x25','^0x26','^0x27','~0x2D','~0x37','^0x33','~0x38','^0x2D','~0x2C','~0x31']

        convertedInput = []

        for char in datalist:
            time.sleep(t)
            if char.isupper():
                if char in uppercase:
                    arrayIndex = uppercase.index(char)
                    hexCode = "^0x" + "{:02x}".format(arrayIndex + 4).upper()
                    os.system("echo '"+ hexCode +"' > /dev/ttyUSB0")
                    convertedInput.append(hexCode)
            elif char.islower(): 
                if char in lowercase:
                    arrayIndex = lowercase.index(char)
                    hexCode = "~0x" + "{:02x}".format(arrayIndex + 4).upper()
                    os.system("echo '"+ hexCode +"' > /dev/ttyUSB0")
                    convertedInput.append(hexCode)
            elif char in digits:
                    arrayIndex = digits.index(char)
                    hexCode = "~0x" + "{:02x}".format(arrayIndex + 4 + 26).upper()
                    os.system("echo '"+ hexCode +"' > /dev/ttyUSB0")
                    convertedInput.append(hexCode)
            elif char in symbol:
                    arrayIndex = symbol.index(char)
                    hexCode = symbolHex[arrayIndex]
                    os.system("echo '"+ hexCode +"' > /dev/ttyUSB0")
                    convertedInput.append(hexCode)
            else:
                self.log_file(str(char) + ' is skipped')

        
        self.log_file('Characters Sent:')
        self.log_file(' '.join(convertedInput))
