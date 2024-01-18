from dolphin import controller
from time import sleep

from typing import TypedDict

# Define my subset of controller inputs
class myGCInputs(TypedDict, total=False):
    # A button
    A:bool
    # B button
    B: bool
    # D-Pad Up
    Up: bool
    # Control stick Horizontal Axis
    StickX: float

def press_button(buttons : myGCInputs):

    print(f"Controller State: {buttons}")
    
    controller.set_gc_buttons(0, {buttons})
    controller.get_gc_buttons(0)