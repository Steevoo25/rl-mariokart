from dolphin import controller
from time import sleep

from typing import TypedDict

CONTROLLER_INDEX = 0
# Define my subset of controller inputs
class myGCInputs(TypedDict, total=False):
    # A button
    A:bool
    # B button
    B: bool
    # D-Pad Up
    Up: bool
    # Control stick Horizontal Axis
    # Ranges from 0 to 255, 128 is neutral
    StickX: float

# Wrapper function to hide controller index (will always be 0 as using one controller)

def press_button(buttons):

    print(f"Controller State: {buttons}")
    
    controller.set_gc_buttons(CONTROLLER_INDEX, buttons)
    #controller.get_gc_buttons(CONTROLLER_INDEX)