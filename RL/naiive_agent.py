from dolphin import event

from sys import path
# Add venv dir to path to allow external packages
venv_dir ='C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\venv\\Lib\\site-packages'
path.append(venv_dir)
# Add this dir to path to allow imports from other scripts
this_dir = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\RL'
path.append(this_dir)

from random import choice
from environment.press_button import press_button as set_controller
from RL.environment.dolphin_env import reset, step
#from RL.Rainbow.AdditionalScripts.action_space import action_dict as action_space

CONTROLLER_PERMUTATIONS = 39
# STICK_ANGLES = [0,64,128,192,256]

# def random_button() -> bool:
#     return choice([True, False])

# # Technically should be int but dolphin is expecting a float
# def random_stick() -> float:
#     return choice(STICK_ANGLES)

# # Creates a dictionary containing random controller inputs
# def generate_random_controller_state():

#     default_controller = {"A":False,"B":False,"Up":False,"StickX":128}
    
#     default_controller["A"] = random_button()
#     default_controller["B"] = random_button()
#     default_controller["Up"] = random_button()
#     default_controller["StickX"] = random_stick()
    
#     return default_controller

def run_agent():

    set_controller(action_space[choice(range(CONTROLLER_PERMUTATIONS))])
    #step()

# When the script is first ran, emulation needs to be reset
needs_reset = True
event.on_frameadvance(run_agent)