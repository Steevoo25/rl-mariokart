## A short script to help understand how to use the Dolphin Controller API
# Mpre specifically setting multiple buttons at once
from dolphin import event
from press_button import press_button as set_controller


def press_2_buttons():
    set_controller({"A": True, "B": True})

def set_stick():
    set_controller({"StickX": 128})

event.on_frameadvance(press_2_buttons)