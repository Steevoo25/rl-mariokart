from controller import Controller

controller = Controller()
try:
    # Test some normal data
    controller.press_button('A')
    controller.press_button('B')
    controller.press_button('D-Pad Up')
    controller.tilt_stick(10)
    
    # Test some erroneous data
    controller.tilt_stick(20)
    controller.press_button('X')
except:
    Exception()

print(controller)
controller.reset()
print(controller)