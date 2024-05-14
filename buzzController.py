import usb.backend.libusb1  # type: ignore
import usb.core  # type: ignore
import usb.util  # type: ignore


class BuzzControllers:
    def __init__(self) -> None:
        backend = usb.backend.libusb1.get_backend(
            find_library=lambda x: "libusb-1.0.dll" # type: ignore
        )
        self.device = usb.core.find(backend=backend, idVendor=0x054C, idProduct=0x1000)

        self.interface = 0
        self.lights = [0, 0, 0, 0]
        self.buttons = [
            {"red": False, "yellow": False, "green": False, "orange": False, "blue": False},
            {"red": False, "yellow": False, "green": False, "orange": False, "blue": False},
            {"red": False, "yellow": False, "green": False, "orange": False, "blue": False},
            {"red": False, "yellow": False, "green": False, "orange": False, "blue": False},
        ]

        self.bits = 0

        self.device.set_configuration()  # type: ignore
        usb.util.claim_interface(self.device, self.interface)
        cfg = self.device.get_active_configuration()  # type: ignore
        self.endpoint = cfg[(0, 0)][0]

    def is_button_pressed(self, controller: int, button: str):
        return self.buttons[controller][button]

    def devicestatus(self):
        # ID 054c:1000 Sony Corp. Wireless Buzz! Receiver
        backend = usb.backend.libusb1.get_backend(
            find_library=lambda x: "libusb-1.0.dll"
        )
        self.device = usb.core.find(backend=backend, idVendor=0x054C, idProduct=0x1000)
        return self.device

    def get_pressed_controllers(self) -> list[bool]:
        pressed = []
        for controller in self.buttons:
            if any(controller.values()):
                pressed.append(True)
            else:
                pressed.append(False)
        return pressed

    def get_button_state(self, controller):
        return self.buttons[controller]
    
    def get_buttons_state(self) -> list[dict[str, bool]]:
        return self.buttons
    
    def get_lights(self) -> list[int]:
        return self.lights
    
    def set_light(self, controller, state=False):
        self.lights[controller] = 0xFF if state else 0
        self.sendLightState()      

    def set_lights(self, *args):
        for idx, light in enumerate(args):
            self.lights[idx] = 0xFF if light else 0
        self.sendLightState()

    def sendLightState(self):
        self.device.ctrl_transfer(  # type: ignore
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

    def all_lights_off(self):
        self.set_lights(False, False, False, False)

    def all_lights_on(self):
        self.set_lights(True, True, True, True)


    def flip_light(self, controller):
        self.set_light(controller, not self.is_button_pressed(controller, "green"))

    def read_controller(self, raw=False, timeout=1000):

        # Reads the controller
        # Returns the result of Parsecontroller (the changed bit) or raw

        try:
            cfg = self.device.get_active_configuration() # type: ignore
            self.endpoint = cfg[(0, 0)][0]
            data = self.device.read( # type: ignore
                self.endpoint.bEndpointAddress,
                self.endpoint.wMaxPacketSize,
                timeout=timeout,
            )
            parsed = self.parse_controller(data)
        except usb.core.USBError as _:
            data = None
        if data != None and raw == False:
            data = parsed
        return data

    def parse_controller(self, data):

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



if __name__ == "__main__":
    buzz = BuzzControllers()

    buzz.all_lights_on()

    while True:
        r = buzz.read_controller(timeout=500)  # type: ignore
        if r != None:
            pressed = buzz.get_pressed_controllers()
            print(pressed)
            for idx, val in enumerate(pressed):
                if val and buzz.get_buttons_state()[idx]["red"]:
                    buzz.set_light(idx, False)
            # buzz.turnOffControllerLights(pressed)
            if not any(buzz.get_lights()):
                buzz.all_lights_on()

