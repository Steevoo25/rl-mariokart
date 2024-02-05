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
from load_savestate import load_using_fkey as load_savestate
from press_button import press_button as set_controller
from calculate_reward import calculate_reward
from memory_viewer import getRaceInfo
# Initialise empty frame info
# Savestate has 1 frame of pressing accelerating so learning does not terminate immediately
previousFrameInfo = [0,0,0]


def reset():
# Running dolphin in command line causes some issues, 
# so I will have to open dolphin and run the script through the gui,
# making sure to use the correct config
    # 1.) Load Savestate
    # Because init() will be called in a frameadvance, I dont need it now
    total_reward = 0
    load_savestate()
    # 2.) Reset Controller
    set_controller(DEFAULT_CONTROLLER)

def step():
    #Stores the current frames raceInfo in previousFrameInfo
    previousFrameInfo = getRaceInfo()
    # Read Frame
    # Calculate rewards
    total_reward = 0
    reward = calculate_reward(previousFrameInfo)
    total_reward = total_reward + reward
    print(total_reward)
    
    # update q network
    # identify input with highest estimated reward
    return total_reward