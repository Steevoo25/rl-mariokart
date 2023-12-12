import pyautogui as pag

class Controller:
    __a_button: bool
    __b_button: bool
    __d_pad_up: bool
    __stick_angle: int
    
    ALLOWED_STICK_ANGLES = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    
    # Initialise controller with no inputs
    def __init__(self):
        self.reset()
    
    # Return state of controller
    def __str__(self):
        return f'A:{self.__a_button}\nB:{self.__b_button}\nD-Pad Up:{self.__d_pad_up}\nStick Angle:{self.__stick_angle}'

    # Reset controller to no inputs
    def reset(self):
        self.__a_button = False
        self.__b_button = False
        self.__d_pad_up = False
        self.__stick_angle = 7

    # Press a given button
    def press_button(self, button:str):
        if button == 'A':
            self.__a_button = True           
        elif button == 'B':
            self.__b_button = True            
        elif button == 'D-Pad Up':
            self.__d_pad_up = True
        else:
            raise Exception(f"Button not recognised: {button}")

    # Tilt the main stick a certain angle
    def tilt_stick(self, angle:int):
        if angle in self.ALLOWED_STICK_ANGLES:
            self.__stick_angle = angle
        else:
            raise Exception(f"Stick angle out of range: {angle}")
    
    def output_controller_state(self):
        # Looking at the current state of the controller,
        # Press the mapped keys on the keyboard
        if self.__a_button :
            pag.press('X')
        if self.__b_button :
            pag.press('Z')
        if self.__d_pad_up :
            pag.press('T')
        # TODO: Handle Stick angle
        
        return

