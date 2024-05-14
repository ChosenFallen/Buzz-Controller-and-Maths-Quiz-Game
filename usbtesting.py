# import libusb_package # type: ignore

import usb.core

# print([x for x in usb.core.find(find_all=True)])

for usb_device in usb.core.find(find_all=True):
    print("-------------------------------")
    print(usb_device)

# for dev in libusb_package.find(find_all=True):
#     print(dev)

# import os
# os.environ['PYUSB_DEBUG'] = 'debug'
# import libusb_package
# libusb_package.find()

# import usb.backend.libusb1
# backend = usb.backend.libusb1.get_backend(find_library=lambda x: r"C:\Users\curti\AppData\Local\Programs\Python\Python312\Lib\site-packages\libusb\_platform\_windows\x64\libusb-1.0.dll")  # adapt to your path
# usb_devices = usb.core.find(backend=backend, find_all=True)
# for usb_device in usb_devices:
#     print(usb_device)


# import usb.core
# from usb.backend import libusb1

# # it should find libusb-1.0.dll at our path variable
# back = libusb1.get_backend()
# print(type(back))  # return: <class 'usb.backend.libusb1._LibUSB'>

# dev = usb.core.find(backend=back)
# print(type(dev))  # return: <class 'usb.core.Device'>

# # flag 'find_all=True' would return generator
# # reprecent connected usb devices

# dev_list = usb.core.find(find_all=True, backend=back)
# print(type(dev_list)) # return: <class 'generator'>
