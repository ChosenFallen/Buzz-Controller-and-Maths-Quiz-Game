from enum import Enum, auto
from threading import Thread

import usb.backend.libusb1  # type: ignore
import usb.core  # type: ignore
import usb.util  # type: ignore
from random import choice


class Colours(Enum):
    Red = auto()
    Yellow = auto()
    Green = auto()
    Orange = auto()
    Blue = auto()


class BuzzBrain:
    def __init__(self) -> None:
        backend = usb.backend.libusb1.get_backend(
            find_library=lambda x: "libusb-1.0.dll"  # type: ignore
        )
        self.device = usb.core.find(backend=backend, idVendor=0x054C, idProduct=0x1000)
        self.interface = 0

        self.controllers: list[BuzzController] = []
        for i in range(4):
            self.controllers.append(BuzzController(brain=self, index=i))

        self.device.set_configuration()  # type: ignore
        usb.util.claim_interface(self.device, self.interface)
        cfg = self.device.get_active_configuration()  # type: ignore
        self.endpoint = cfg[(0, 0)][0]

        self.lights: list[int] = [0, 0, 0, 0]
        self.thread: None | Thread = None
        self.bits: int = 0
        self.changed: int = 0

    def sendLightState(self) -> None:
        """
        Sends the current state of the lights to the controller
        """
        self.device.ctrl_transfer(  # type: ignore
            0x21,
            0x09,
            0x0200,
            0,
            [0, self.lights[0], self.lights[1], self.lights[2], self.lights[3], 0, 0],
        )

    def read_controller(self) -> None:
        try:
            cfg = self.device.get_active_configuration()  # type: ignore
            self.endpoint = cfg[(0, 0)][0]
            data = self.device.read(  # type: ignore
                self.endpoint.bEndpointAddress,
                self.endpoint.wMaxPacketSize,
                timeout=1000,
            )
            self.parse_controller(data)
        except usb.core.USBError as _:
            data = None

        self.thread = None

    def parse_controller(self, data: bytes) -> None:
        # Controller 1

        self.controllers[0].Red = True if data[2] & 1 else False
        self.controllers[0].Yellow = True if data[2] & 2 else False
        self.controllers[0].Green = True if data[2] & 4 else False
        self.controllers[0].Orange = True if data[2] & 8 else False
        self.controllers[0].Blue = True if data[2] & 16 else False

        # Controller 2

        self.controllers[1].Red = True if data[2] & 32 else False
        self.controllers[1].Yellow = True if data[2] & 64 else False
        self.controllers[1].Green = True if data[2] & 128 else False
        self.controllers[1].Orange = True if data[3] & 1 else False
        self.controllers[1].Blue = True if data[3] & 2 else False

        # Controller 3

        self.controllers[2].Red = True if data[3] & 4 else False
        self.controllers[2].Yellow = True if data[3] & 8 else False
        self.controllers[2].Green = True if data[3] & 16 else False
        self.controllers[2].Orange = True if data[3] & 32 else False
        self.controllers[2].Blue = True if data[3] & 64 else False

        # Controller 4

        self.controllers[3].Red = True if data[3] & 128 else False
        self.controllers[3].Yellow = True if data[4] & 1 else False
        self.controllers[3].Green = True if data[4] & 2 else False
        self.controllers[3].Orange = True if data[4] & 4 else False
        self.controllers[3].Blue = True if data[4] & 8 else False

        oldbits = self.bits
        self.bits = (data[4] << 16) + (data[3] << 8) + data[2]

        self.changed = oldbits | self.bits

    def update(self) -> None:
        # Update controllers with button states
        if self.thread is None:
            self.thread = Thread(target=self.read_controller, args=[])
            self.thread.start()

        # Send light state
        self.sendLightState()


class BuzzController:
    def __init__(self, brain: BuzzBrain, index: int) -> None:
        self.brain: BuzzBrain = brain
        self.index: int = index

        self.Red: bool = False
        self.Yellow: bool = False
        self.Green: bool = False
        self.Orange: bool = False
        self.Blue: bool = False
        self.Light: bool = False

    def is_buttons_pressed(self, list_of_buttons: list[str]) -> bool:
        return all([self.is_button_pressed(button) for button in list_of_buttons])

    def get_buttons_states(self) -> dict[str, bool]:
        return {
            "red": self.Red,
            "yellow": self.Yellow,
            "green": self.Green,
            "orange": self.Orange,
            "blue": self.Blue,
        }

    # def set_button_states(self, buttons: dict[str, bool]) -> None:
    #     self.Red = buttons["red"]
    #     self.Yellow = buttons["yellow"]
    #     self.Green = buttons["green"]
    #     self.Orange = buttons["orange"]
    #     self.Blue = buttons["blue"]

    def is_button_pressed(self, button: str) -> bool:
        return self.__dict__[button.title()]


class QuizBuzzBrain(BuzzBrain):
    def first_pressed_controller(self, in_play_controllers: list[int] = [0, 1, 2, 3]) -> None | int:
        # Return the index of the first pressed controller
        pressed = []
        for controller in self.controllers:
            if controller.index in in_play_controllers and controller.is_buttons_pressed(["yellow", "green", "orange", "blue"]):
                pressed.append(self.controllers.index(controller))
                
        match len(pressed):
            case 0:
                return None
            case 1:
                return pressed[0]
            case _:
                return choice(pressed)

    def first_pressed_button(self, controller_index: int) -> str:
        pressed = []
        for colour in ["yellow", "green", "orange", "blue"]:
            if self.controllers[controller_index].is_button_pressed(colour):
                pressed.append(colour)
        
        match len(pressed):
            case 1:
                return pressed[0]
            case _:
                return choice(pressed)