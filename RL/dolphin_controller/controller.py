
class Controller:
    a_button: bool
    b_button: bool
    d_pad_up: bool
    stick_angle: int
    
    ALLOWED_STICK_ANGLES = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    
    # Initialise controller with no inputs
    def __init__(self):
        self.a_button = False
        self.b_button = False
        self.d_pad_up = False
        self.stick_angle = 7
    
    # Return state of controller
    def __str__(self):
        return f'A:{self.a_button}\nB:{self.b_button}\nD-Pad Up:{self.d_pad_up}\nStick Angle:{self.stick_angle}\n'

    # Reset controller to no inputs
    def reset(self):
        self.__init__

    # Press a given button
    def press_button(self, button:str):
        if button == 'A':
            self.a_button = True
        elif button == 'B':
            self.b_button = True
        elif button == 'D-Pad Up':
            self.d_pad_up = True
        else:
            raise Exception(f"Button not recognised: {button}")

    # Tilt the main stick a certain angle
    def tilt_stick(self, angle:int):
        if angle in self.ALLOWED_STICK_ANGLES:
            self.stick_angle = angle
        else:
            raise Exception(f"Stick angle out of range: {angle}")

controller = Controller()
controller.press_button('A')
controller.tilt_stick(10)
print(controller)