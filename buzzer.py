#!/usr/bin/python
# -*- coding: utf-8 -*-

# PS2 Buzz! Controller library

import json
import os
import sys
import time
import traceback

import usb.backend.libusb1
import usb.core
import usb.util


class buzz:

    def __init__(self):

        # ID 054c:1000 Sony Corp. Wireless Buzz! Receiver
        backend = usb.backend.libusb1.get_backend(
            find_library=lambda x: "libusb-1.0.dll"
        )
        self.device = usb.core.find(backend=backend, idVendor=0x054C, idProduct=0x1000)

        self.interface = 0
        self.lights = [0, 0, 0, 0]
        self.buttons = [
            {"red": 0, "yellow": 0, "green": 0, "orange": 0, "blue": 0},
            {"red": 0, "yellow": 0, "green": 0, "orange": 0, "blue": 0},
            {"red": 0, "yellow": 0, "green": 0, "orange": 0, "blue": 0},
            {"red": 0, "yellow": 0, "green": 0, "orange": 0, "blue": 0},
        ]
        self.bits = 0

        self.device.set_configuration()
        usb.util.claim_interface(self.device, self.interface)
        cfg = self.device.get_active_configuration()
        self.endpoint = cfg[(0, 0)][0]

    def devicestatus(self):
        # ID 054c:1000 Sony Corp. Wireless Buzz! Receiver
        backend = usb.backend.libusb1.get_backend(
            find_library=lambda x: "libusb-1.0.dll"
        )
        self.device = usb.core.find(backend=backend, idVendor=0x054C, idProduct=0x1000)

        return self.device

    def setlights(self, control):

        # Sets lights based on binaray
        # 1 = Controller 1
        # 2 = Controller 2
        # 4 = Controller 3
        # 8 = Controller 4

        self.lights[0] = 0xFF if control & 1 else 0
        self.lights[1] = 0xFF if control & 2 else 0
        self.lights[2] = 0xFF if control & 4 else 0
        self.lights[3] = 0xFF if control & 8 else 0
        self.device.ctrl_transfer(
            0x21,
            0x09,
            0x0200,
            0,
            [
                0,
                self.lights[0],
                self.lights[1],
                self.lights[2],
                self.lights[3],
                0,
                0,
            ],
        )

    def setlight(self, controller, state=False):

        # Sets a light on or off for a single controller

        self.lights[controller] = 0xFF if state else 0
        self.device.ctrl_transfer(
            0x21,
            0x09,
            0x0200,
            0,
            [
                0,
                self.lights[0],
                self.lights[1],
                self.lights[2],
                self.lights[3],
                0,
                0,
            ],
        )

    def fliplight(self, controller):

        # Flips the state of a controllers light
        # TODO

        pass

    def readcontroller(self, raw=False, timeout=1000):

        # Reads the controller
        # Returns the result of Parsecontroller (the changed bit) or raw

        try:
            cfg = self.device.get_active_configuration()
            self.endpoint = cfg[(0, 0)][0]
            data = self.device.read(
                self.endpoint.bEndpointAddress,
                self.endpoint.wMaxPacketSize,
                timeout=timeout,
            )
            parsed = self.parsecontroller(data)
        except usb.core.USBError as e:

            # if (e): print ("Laukiama mygtuko")
            data = None
        if data != None and raw == False:
            data = parsed
        return data

    def parsecontroller(self, data):

        # Function to parse the results of readcontroller
        # We break this out incase someone else wants todo something different
        # Returns the changed bits

        # Controller 1

        self.buttons[0]["red"] = True if data[2] & 1 else False
        self.buttons[0]["yellow"] = True if data[2] & 2 else False
        self.buttons[0]["green"] = True if data[2] & 4 else False
        self.buttons[0]["orange"] = True if data[2] & 8 else False
        self.buttons[0]["blue"] = True if data[2] & 16 else False

        # Controller 2

        self.buttons[1]["red"] = True if data[2] & 32 else False
        self.buttons[1]["yellow"] = True if data[2] & 64 else False
        self.buttons[1]["green"] = True if data[2] & 128 else False
        self.buttons[1]["orange"] = True if data[3] & 1 else False
        self.buttons[1]["blue"] = True if data[3] & 2 else False

        # Controller 3

        self.buttons[2]["red"] = True if data[3] & 4 else False
        self.buttons[2]["yellow"] = True if data[3] & 8 else False
        self.buttons[2]["green"] = True if data[3] & 16 else False
        self.buttons[2]["orange"] = True if data[3] & 32 else False
        self.buttons[2]["blue"] = True if data[3] & 64 else False

        # Controller 4

        self.buttons[3]["red"] = True if data[3] & 128 else False
        self.buttons[3]["yellow"] = True if data[4] & 1 else False
        self.buttons[3]["green"] = True if data[4] & 2 else False
        self.buttons[3]["orange"] = True if data[4] & 4 else False
        self.buttons[3]["blue"] = True if data[4] & 8 else False

        oldbits = self.bits
        self.bits = (data[4] << 16) + (data[3] << 8) + data[2]

        changed = oldbits | self.bits

        return changed

    def getbuttons(self):

        # Returns current state of buttons

        return self.buttons

    def getlights(self):

        # Returns the current state of the lights

        return self.lights


if __name__ == "__main__":
    buzzers = buzz()

    #    for x in range(16):
    # ....buzz.setlights(x)
    # ....time.sleep(1)

    for x in range(0, 12):
        buzzers.setlights(8)
        time.sleep(0.05)
        buzzers.setlights(4)
        time.sleep(0.05)
        buzzers.setlights(2)
        time.sleep(0.05)
        buzzers.setlights(1)
        time.sleep(0.05)
    buzzers.setlights(0)
    buzzers.setlights(1|2|4|8)  # type: ignore
    while True:
        r = buzzers.readcontroller(timeout=500)  # type: ignore
        if r != None:
            print(bin(r))
            print(buzzers.getbuttons())
    
