# -- DOLHPIN IMPORTS --
#from dolphin import savestate # for loading savestates
from dolphin import event # for resetting emulation
from press_button import myGCInputs

DEFAULT_CONTROLLER = {"A":False,"B":False,"Up":False,"StickX":128}

# As the script is run within the dolphin executable, 
# Append the true path of scripts to import
from sys import path

# Add venv dir to path to allow external packages
venv_dir ='C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\venv\\Lib\\site-packages'
path.append(venv_dir)
# Add this dir to path to allow imports from other scripts
this_dir = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\RL'
path.append(this_dir)

# -- OTHER IMPORTS --
import socket

from load_savestate import load_using_fkey as load_savestate
from press_button import press_button as set_controller
from calculate_reward import calculate_reward
from memory_viewer import getRaceInfo

# Savestate has 1 frame of pressing accelerating so learning does not terminate immediately


def reset():
# Running dolphin in command line causes some issues, 
# so I will have to open dolphin and run the script through the gui,
# making sure to use the correct config
    # 1.) Load Savestate
    # Because init() will be called in a frameadvance, I dont need it now
    
    load_savestate()
    # 2.) Reset Controller
    set_controller(DEFAULT_CONTROLLER)

def step():
    previousFrameInfo = 0
    # Read Frame
    # Calculate rewards
    if previousFrameInfo == 0:
        reward, previousFrameInfo = calculate_reward()
    else:
        previousFrameInfo = 0
    print(reward)
    
    #Stores the current frames raceInfo in previousFrameInfo
    # update q network
    # identify input with highest estimated reward
    return reward


## Socket Initialisation
# This script will be running within Dolphin's embedded python, meaning it has a lot of limitations
# To get around these I will send the environment data to a seperate Agent script

HOST = socket.gethostname()
PORT = 5555
print(f'Host : {HOST}')
env_socket = socket.socket()
#env_socket.connect((HOST,PORT)) # Uncomment when training

## Initialisations
previous_frame_info = 0
reward = 0
frame_counter = 0

### Main Training Loop ###
just_reset = False

while True:
    await event.frameadvance()
    frame_counter +=1
    print(f"Frame: {frame_counter}")