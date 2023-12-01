from dataclasses import dataclass


class Controller:
    a_button: bool
    b_button: bool
    d_pad_up: bool
    stick_angle: int
    
    def __init__(self):
        self.a_button = False
        self.b_button = False
        self.d_pad_up = False
        self.stick_angle = 7
        
    def __str__(self):
        return f'A:{self.a_button}\nB:{self.b_button}\nD-Pad Up:{self.d_pad_up}\nStick Angle:{self.stick_angle}\n'
        
    def reset(self):
        self.__init__

controller = Controller()
controller.a_button = True
print(controller)