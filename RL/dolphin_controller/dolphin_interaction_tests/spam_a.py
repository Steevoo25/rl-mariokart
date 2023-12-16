from dolphin import controller
from time import sleep
while True:
    controller.set_gc_buttons(0, {"A": True})
    sleep(0.05)
    controller.set_gc_buttons(0, {"A": False})