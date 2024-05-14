from enum import Enum, auto
from random import choice
from threading import Thread

import usb.backend.libusb1  # type: ignore
import usb.core  # type: ignore
import usb.util  # type: ignore


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
        self.controllers.extend(BuzzController(brain=self, index=i) for i in range(4))
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
        button_masks = [
            (1, 2, 4, 8, 16),
            (32, 64, 128, 1, 2),
            (4, 8, 16, 32, 64),
            (128, 1, 2, 4, 8),
        ]
        data_index_arrays = [
            (2, 2, 2, 2, 2),
            (2, 2, 2, 3, 3),
            (3, 3, 3, 3, 3),
            (3, 4, 4, 4, 4),
        ]
        for i, controller in enumerate(self.controllers):
            mask = button_masks[i]
            data_indexes = data_index_arrays[i]
            controller.Red = bool(data[data_indexes[0]] & mask[0])
            controller.Yellow = bool(data[data_indexes[1]] & mask[1])
            controller.Green = bool(data[data_indexes[2]] & mask[2])
            controller.Orange = bool(data[data_indexes[3]] & mask[3])
            controller.Blue = bool(data[data_indexes[4]] & mask[4])

        # # Controller 1

        # self.controllers[0].Red = True if data[2] & 1 else False
        # self.controllers[0].Yellow = True if data[2] & 2 else False
        # self.controllers[0].Green = True if data[2] & 4 else False
        # self.controllers[0].Orange = True if data[2] & 8 else False
        # self.controllers[0].Blue = True if data[2] & 16 else False

        # # Controller 2

        # self.controllers[1].Red = True if data[2] & 32 else False
        # self.controllers[1].Yellow = True if data[2] & 64 else False
        # self.controllers[1].Green = True if data[2] & 128 else False
        # self.controllers[1].Orange = True if data[3] & 1 else False
        # self.controllers[1].Blue = True if data[3] & 2 else False

        # # Controller 3

        # self.controllers[2].Red = True if data[3] & 4 else False
        # self.controllers[2].Yellow = True if data[3] & 8 else False
        # self.controllers[2].Green = True if data[3] & 16 else False
        # self.controllers[2].Orange = True if data[3] & 32 else False
        # self.controllers[2].Blue = True if data[3] & 64 else False

        # # Controller 4

        # self.controllers[3].Red = True if data[3] & 128 else False
        # self.controllers[3].Yellow = True if data[4] & 1 else False
        # self.controllers[3].Green = True if data[4] & 2 else False
        # self.controllers[3].Orange = True if data[4] & 4 else False
        # self.controllers[3].Blue = True if data[4] & 8 else False

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
        return all(self.is_button_pressed(button) for button in list_of_buttons)

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
        button_state = {
            "red": self.Red,
            "yellow": self.Yellow,
            "green": self.Green,
            "orange": self.Orange,
            "blue": self.Blue,
        }
        return button_state[button.lower()]


class QuizBuzzBrain(BuzzBrain):
    def first_pressed_controller(
        self, in_play_controllers: list[int] | None = None
    ) -> None | int:
        if in_play_controllers is None:
            in_play_controllers = [0, 1, 2, 3]
        pressed = [
            idx
            for idx, controller in enumerate(self.controllers)
            if controller.index in in_play_controllers
            and controller.is_buttons_pressed(["yellow", "green", "orange", "blue"])
        ]
        match len(pressed):
            case 0:
                return None
            case 1:
                return pressed[0]
            case _:
                return choice(pressed)

    def first_pressed_button(self, controller_index: int) -> str:
        pressed = [
            colour
            for colour in ["yellow", "green", "orange", "blue"]
            if self.controllers[controller_index].is_button_pressed(colour)
        ]
        match len(pressed):
            case 1:
                return pressed[0]
            case _:
                return choice(pressed)
