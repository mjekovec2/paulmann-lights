"""Asynchronous Python client for Paulmann Key Lights."""

import attr
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



@attr.s(auto_attribs=True, frozen=True)
class State:
    """Object holding the Paulmann Key Light state."""
    system_time: int
    on: bool
    brightness: int
    color: int
    timer: int
    working_mode: []
    controller_enable: []
    name: str

    @staticmethod
    def from_dict(data):

        """Return a State object from a Paulmann Key Light API response."""
        return State(
            system_time=data[UUID_SYSTEM_TIME],
            on=data[UUID_ONOFF],
            brightness=data[UUID_BRIGHTNESS],
            color=data[UUID_COLOR],
            timer=data[UUID_TIMER],
            working_mode=data[UUID_WORKING_MODE],
            controller_enable=data[UUID_CONTROLLER_ENABLE],
            name=data[UUID_NAME],
        )

@attr.s(auto_attribs=True, frozen=True)
class Info:
    """Object holding the Paulmann Key Light device information."""

    system_id: str
    model: str
    serial_number: str
    firmware_revision: str
    hardware_revision: str
    software_revision: str
    manufacturer: str
    ieee_cert: str
    pnp_id: str


    @staticmethod
    def from_dict(data):
        """Return a Info object from a Paulmann Key Light API response."""
        return Info(
            system_id=data[UUID_INFO_SYSTEM_ID],
            model=data[UUID_INFO_MODEL],
            serial_number=data[UUID_INFO_SERIAL_NUMBER],
            firmware_revision=data[UUID_INFO_FIRMWARE_REVISION],
            hardware_revision=data[UUID_INFO_HARDWARE_REVISION],
            software_revision=data[UUID_INFO_SOFTWARE_REVISION],
            manufacturer=data[UUID_INFO_MANUFACTURER],
            ieee_cert=data[UUID_INFO_IEEE_CERT],
            pnp_id=data[UUID_INFO_PNP_ID],
        )
