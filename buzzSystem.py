from __future__ import annotations

from enum import Enum, auto
from random import choice, shuffle
from threading import Thread

import usb.backend.libusb1  # type: ignore
import usb.core  # type: ignore
import usb.util  # type: ignore

from Questions.baseQuestion import BaseQuestionSet
from Questions.utilities import ALL_COLOURS, ANSWER_COLOURS


class Colours(Enum):
    Red = auto()
    Yellow = auto()
    Green = auto()
    Orange = auto()
    Blue = auto()


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
        return any(self.is_button_pressed(button) for button in list_of_buttons)

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


class BuzzBrain:
    def __init__(
        self, question_set: BaseQuestionSet | None = None, num_of_controllers: int = 4
    ) -> None:
        backend = usb.backend.libusb1.get_backend(
            find_library=lambda x: "libusb-1.0.dll"  # type: ignore
        )
        self.device = usb.core.find(backend=backend, idVendor=0x054C, idProduct=0x1000)
        # print(self.device)
        self.interface = 0

        self.controllers: list[BuzzController] = [
            BuzzController(brain=self, index=i) for i in range(4)
        ]
        self.device.set_configuration()  # type: ignore
        usb.util.claim_interface(self.device, self.interface)
        cfg = self.device.get_active_configuration()  # type: ignore
        self.endpoint = cfg[(0, 0)][0]

        self.lights: list[int] = [0, 0, 0, 0]
        self.thread: None | Thread = None
        self.bits: int = 0
        self.changed: int = 0
        self.question_set: BaseQuestionSet = (
            question_set if question_set is not None else BaseQuestionSet()
        )
        self.num_of_controllers = num_of_controllers
        self.reset_all_controllers()
        self.previous_pressed: list[int] = []

    def reset_all_controllers(self) -> None:
        self.valid_controllers: list[int] = list(range(self.num_of_controllers))

    def remove_controller(self, index: int) -> None:
        if index in self.valid_controllers:
            self.valid_controllers.remove(index)

    def sendLightState(self) -> None:
        """
        Sends the current state of the lights to the controller
        """
        # print(f"L{self.lights}")
        self.device.ctrl_transfer(  # type: ignore
            0x21,
            0x09,
            0x0200,
            0,
            [0, self.lights[0], self.lights[1], self.lights[2], self.lights[3], 0, 0],
        )

    def turn_on_all_lights(self) -> None:
        self.lights = [0xFF, 0xFF, 0xFF, 0xFF]

    def turn_off_all_lights(self) -> None:
        self.lights = [0, 0, 0, 0]

    def turn_off_index(self, index: int) -> None:
        self.lights[index] = 0

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
            # self.sendLightState()
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

        oldbits = self.bits
        self.bits = (data[4] << 16) + (data[3] << 8) + data[2]

        self.changed = oldbits | self.bits
        # if self.changed:
        #     print(f"={self.changed}|")

    def update(self) -> None:
        # Update controllers with button states
        if self.thread is None:

            # print(".")
            self.thread = Thread(target=self.read_controller, args=[])
            self.thread.start()

        # Send light state
        self.sendLightState()

    def first_pressed_controller(self) -> None | int:
        # print(
        #     self.controllers[0].Blue,
        #     self.controllers[0].index,
        #     in_play_controllers,
        #     self.controllers[0].index in in_play_controllers,
        #     self.controllers[0].is_buttons_pressed(ANSWER_COLOURS),
        # )
        pressed = [
            controller.index
            for controller in self.controllers
            if controller.index in self.valid_controllers
            and controller.is_buttons_pressed(ANSWER_COLOURS)
        ]
        # print(pressed)
        match len(pressed):
            case 0:
                self.previous_pressed = []
                return None
            case 1:
                if pressed[0] in self.previous_pressed:
                    self.previous_pressed = pressed
                    return None
                self.previous_pressed = pressed
                return pressed[0]
            case _:
                shuffle(pressed)
                for chosen_index in pressed:
                    if chosen_index not in self.previous_pressed:
                        self.previous_pressed = pressed
                        return chosen_index
                return None

    def first_pressed_button(self, controller_index: int) -> str:
        pressed = [
            colour
            for colour in ANSWER_COLOURS
            if self.controllers[controller_index].is_button_pressed(colour)
        ]
        match len(pressed):
            case 1:
                return pressed[0]
            case _:
                return choice(pressed)

    def check_answer(self, colour: str) -> bool:
        if self.question_set is not None:
            return self.question_set.check_answer(colour)
        return False
