from paulmann.const import (
    UUID_SYSTEM_TIME,
    UUID_PWD,
    UUID_ONOFF,
    UUID_BRIGHTNESS,
    UUID_NAME,
    UUID_COLOR,
    UUID_TIMER,
    UUID_WORKING_MODE,
    UUID_CONTROLLER_ENABLE,
    UUID_INFO_SYSTEM_ID,
    UUID_INFO_MODEL,
    UUID_INFO_SERIAL_NUMBER,
    UUID_INFO_FIRMWARE_REVISION,
    UUID_INFO_HARDWARE_REVISION,
    UUID_INFO_SOFTWARE_REVISION,
    UUID_INFO_MANUFACTURER,
    UUID_INFO_IEEE_CERT,
    UUID_INFO_PNP_ID
)

import logging
from typing import Optional

class MockAdapter:
    __instance = None
    mac = None
    _device = None

    def __init__(self):
        raise Exception("use get_instance() instead")
        
    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls.__new__(cls)
            cls.__instance._device: Optional[MockDevice] = None
            cls.__instance.mac = ""
        return cls.__instance

    def start(self, **kwargs):
        return True

    def stop(self):
        return True

    def connect(self, mac:str):
        self._mac = mac
        if self._device is None:
            self._device = MockDevice(self)
        return self._device

    def disconnect(self, device):
        #self._device = None
        #self._mac = ""
        return


class MockDevice:
    def __init__(self, adapter):
        self._adapter = adapter
        self._on = False
        self._color = 2700
        self._brightness = 50

    def char_write(self, uuid: str, value: bytearray):
        #print("Write:",uuid, value)
        if uuid == UUID_BRIGHTNESS:
            self._brightness = int.from_bytes(value, 'little')
            #logging.info(self._brightness)     
        elif uuid == UUID_COLOR:
            self._color = int.from_bytes(value, 'little')
            #logging.info(self._color)
        elif uuid == UUID_ONOFF:
            self._on = int.from_bytes(value, 'little') == 1
            #logging.info(self._on)

        #print(self._on, self._color, self._brightness)
        return True

    def char_read(self, uuid: str) -> bytearray:
        
        if uuid == UUID_BRIGHTNESS:
            result = self._brightness.to_bytes(1, 'little')  
        elif uuid == UUID_COLOR:
            result = self._color.to_bytes(2, 'little')
        elif uuid == UUID_ONOFF:
            logging.info("Read onoff:" + str(self._on))
            result = self._on.to_bytes(int(self._on == True), 'little')  
        elif uuid == UUID_CONTROLLER_ENABLE:
            result = bytearray("1", "ascii")
        elif uuid == UUID_INFO_FIRMWARE_REVISION:
            result = bytearray("v1.fw.mock", "ascii")  
        elif uuid == UUID_INFO_HARDWARE_REVISION:
            result = bytearray("v1.hw.mock", "ascii")
        elif uuid == UUID_INFO_IEEE_CERT:
            result = bytearray("ieee cert", "ascii")
        elif uuid == UUID_INFO_MODEL:
            result = bytearray("Model name mock", "ascii")
        elif uuid == UUID_INFO_PNP_ID:
            result = bytearray("abc.mock", "ascii")
        elif uuid == UUID_INFO_SERIAL_NUMBER:
            result = bytearray("Serial number mock", "ascii")
        elif uuid == UUID_INFO_SOFTWARE_REVISION:
            result = bytearray("v1.sw.mock", "ascii")
        elif uuid == UUID_INFO_SYSTEM_ID:
            result = bytearray("1234.mock", "ascii")
        elif uuid == UUID_NAME:
            result = bytearray("Lamp WC Mock", "ascii")        
        elif uuid == UUID_SYSTEM_TIME:
            result = bytearray("today", "ascii")
        elif uuid == UUID_TIMER:
            result = bytearray("tomorrow", "ascii")
        elif uuid == UUID_WORKING_MODE:
            result = bytearray("aaaa", "ascii")
        elif uuid == UUID_INFO_MANUFACTURER:
            result = bytearray("Paulman lichts mock", "ascii")

        #print("Read:",uuid, result)
        return result