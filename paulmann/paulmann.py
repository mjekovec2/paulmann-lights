"""Main class for communicating with Paulmann BLE lights ."""

import sys
from typing import Optional

import pygatt
import logging
from pygatt import BLEAddressType
from pygatt.device import BLEDevice
from pygatt.backends import BLEBackend
from pygatt.exceptions import BLEError, NotConnectedError, NotificationTimeout

from .exceptions import PaulmannConnectionError, PaulmannAuthenticationError,PaulmannError
from .models import Info, State
from .const import *


class Paulmann:
    """Main class for communicating with Paulmann BLE lights ."""

    _device = None

    _adapter: BLEBackend = None

    def __init__(
            self,
            mac: str,
            pwd: str = "1234",
            request_timeout: int = 8,
            adapter: BLEBackend = None
    ) -> None:
        """Initialize connection with the Paulman BLE light."""
        self.mac: str = mac
        self.request_timeout: int = request_timeout
        self._adapter: BLEBackend = pygatt.backends.GATTToolBackend() if adapter is None else adapter
        self._authenticated = False
        self._pwd: str = pwd


    def _connect(self, adapter: BLEBackend, mac: str, retry_count=5, force_restart=False)->BLEDevice:
        """ Connect to the devices and save the connection in _device """
        adapter.start(reset_on_start=force_restart)

        i = 0
        while i < retry_count:
            try:
                device = self._adapter.connect(mac)
                logging.info("Successfully connected to " + mac)
                break
            except:
                logging.info("Attempted connecting to " + self.mac + " and failed, retrying "
                      + str(i+1) + " time")
            i += 1

        if device is None:
            raise PaulmannConnectionError("Could not connect to the light " + self.mac)        
        return device

    def _disconnect(self, adapter: BLEBackend, device: BLEDevice):
        """ disconnect from device """
        adapter.disconnect(device)
        adapter.stop()

    def _authenticate (self, device: BLEDevice, pwd: str):
        """ authenticate with the device, does not alter state of self """
        
        logging.info("Sending password " + pwd)
        try:
            device.char_write (UUID_PWD, bytearray(pwd, "ascii"))
            return True
        except:
            raise PaulmannAuthenticationError("Could not authenticate to the light " + self.mac + " using password")
        logging.info("Password successfully sent!")

    def disconnect(self):
        self._disconnect(self._adapter, self._device)
        self._device = None

    def get_device(self):
        if self._device is not None:
            return self._device

        try:
            device = self._connect(self._adapter, self.mac)
            self._authenticate(device, self._pwd)
            self._device = device
            return device
        except:
            raise

    def switch(self, on: bool):
        """ switch the light on or off according to parareter on """
        self.set_state(on=on)

    def toggle (self):
        """ flip the switch regardless of current state """
        state:State = self.get_state()
        self.set_state(on=not state.on)
        
    def color (self, value: int):
        """ color between 153 and 370 - in milireds """
        self.set_state(color=value)

    def brightness (self, value: int):
        """ brightness between 0 and 100 """
        self.set_state(brightness=value)

    def is_on(self)->bool:
        """ return current state of light = on or off """
        state = self.get_state()
        return state.on

    def get_brightness(self)->int:
        """ return current brightness level """
        state = self.get_state()
        return state.brightness

    def get_color(self)->bool:
        """ return current color of light """
        state = self.get_state()
        return state.color

    def set_state(self, on:bool = None, brightness:int = None, color:int = None):
        """ set state of the Paulmann lights
        Parameters
        ----------
        on : bool
            whether the light is on or off
        brightness : int
            brigtness in range of 0 to 100, where 0 is least bright
        color : int
            color in milireds in the range of 154 to 370, 370 being most "warm" or yellow light
        """
        device = self.get_device()

        if on is not None:
            if on:
                logging.info("Toggle on")
                device.char_write (UUID_ONOFF, bytearray([0x01]))
            else:
                logging.info("Toggle off")
                device.char_write (UUID_ONOFF, bytearray([0x00]))
                
        if brightness is not None:
            if brightness > 100:
                brightness = 100
            elif brightness < 0:
                brightness = 0
            logging.info("Brightness to " + str(brightness))
            device.char_write(UUID_BRIGHTNESS, brightness.to_bytes(1, "little"))

        if color is not None:
            if color > 370:
                color = 370
            elif color < 153:
                color = 153

            logging.info("Color to " + str(color))
            device.char_write(UUID_COLOR, color.to_bytes(2, "little"))

    def get_state(self)-> State:
        """ return full state of the light """
        device = self.get_device()

        logging.info("Retrieving state")
        data = {
            UUID_SYSTEM_TIME: device.char_read(UUID_SYSTEM_TIME),
            UUID_ONOFF: int.from_bytes(device.char_read(UUID_ONOFF), 'little') == 1,
            UUID_BRIGHTNESS: int.from_bytes(device.char_read(UUID_BRIGHTNESS), 'little'),
            UUID_NAME: device.char_read(UUID_NAME).decode('ascii').rstrip("\x00"),
            UUID_COLOR: int.from_bytes(device.char_read(UUID_COLOR), 'little'),
            UUID_TIMER: device.char_read(UUID_TIMER),
            UUID_WORKING_MODE: device.char_read(UUID_WORKING_MODE),
            UUID_CONTROLLER_ENABLE: bool(device.char_read(UUID_CONTROLLER_ENABLE)),
        }

        state = State.from_dict(data)
        logging.info(state)
        return state

    def get_info(self)-> Info:
        """ return full info of the light """
        device = self.get_device()

        logging.info("Retrieving info")
        data = {
            UUID_INFO_SYSTEM_ID:
                device.char_read(UUID_INFO_SYSTEM_ID),
            UUID_INFO_MODEL:
                device.char_read(UUID_INFO_MODEL).decode('ascii').rstrip("\x00"),
            UUID_INFO_SERIAL_NUMBER:
                device.char_read(UUID_INFO_SERIAL_NUMBER).decode('ascii').rstrip("\x00"),
            UUID_INFO_FIRMWARE_REVISION:
                device.char_read(UUID_INFO_FIRMWARE_REVISION).decode('ascii')
                .rstrip("\x00"),
            UUID_INFO_HARDWARE_REVISION:
                device.char_read(UUID_INFO_HARDWARE_REVISION).decode('ascii')
                .rstrip("\x00"),
            UUID_INFO_SOFTWARE_REVISION:
                device.char_read(UUID_INFO_SOFTWARE_REVISION).decode('ascii')
                .rstrip("\x00"),
            UUID_INFO_MANUFACTURER:
                device.char_read(UUID_INFO_MANUFACTURER).decode('ascii').rstrip("\x00"),
            UUID_INFO_IEEE_CERT:
                device.char_read(UUID_INFO_IEEE_CERT),
            UUID_INFO_PNP_ID:
                device.char_read(UUID_INFO_PNP_ID).decode('ascii').rstrip("\x00"),
        }

        info = Info.from_dict(data)
        logging.info(info)
        return info
