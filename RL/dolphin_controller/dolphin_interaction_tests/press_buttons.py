#from dolphin import controller, gui
import dolphin.controller as controller
import dolphin.gui as gui

from time import sleep
red = 0xffff0000

gui.add_osd_message("Pressing A", 2000,red)

controller.set_gc_buttons(0, {"A": True})
controller.get_gc_buttons(0)