# -- DOLHPIN IMPORTS --
#from dolphin import savestate # for loading savestates
from dolphin import event # for resetting emulation
from press_button import myGCInputs

default_controller = ({"A":False,"B":False,"Up":False,"StickX":7})
# As the script is run within the dolphin executable, 
# Append the true path of scripts to import
from sys import path

# Add venv dir to path to allow external packages
venv_dir ='C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\venv\\Lib\\site-packages'
path.append(venv_dir)
# Add this dir to path to allow imports from other scripts
this_dir = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\RL\\dolphin_interaction_tests'
path.append(this_dir)

# -- OTHER IMPORTS --
from load_savestate import load_using_fkey as load_savestate
from press_button import press_button as set_controller
from calculate_reward import calculate_reward

# Initialise empty frame info
# Savestate has 1 frame of pressing accelerating so learning does not terminate immediately
previousFrameInfo = [0,0,0]


def init():
# Running dolphin in command line causes some issues, 
# so I will have to open dolphin and run the script through the gui,
# making sure to use the correct config
    # 1.) Load Savestate
    event.on_frameadvance(load_savestate)
    # 2.) Reset Controller
    set_controller({"A":False,"B":False,"Up":False,"StickX":7})


def step():
    # Read Frame
    # Calculate rewards
    total_reward = 0
    reward = calculate_reward(previousFrameInfo)
    total_reward = total_reward + reward
    print(total_reward)
    # update q network
    # identify input with highest estimated reward
    # update controller
    
# Assumes dolphin is already open
def reset():
    total_reward = 0
    # Load Default savestate
    # Reset Controller
    set_controller()
    # wipe framedumps folder
    
# I want to :
# Load savestate
# reset controller
# start episode
# 
init()
step()


# Running
# init()
# step()
# gives this log
# 35:59:604 Scripting\Python\Modules\doliomodule.cpp:26 N[Scripting]: Script stdout: Controller State: {'A': False, 'B': False, 'Up': False, 'StickX': 7}
# 35:59:604 Scripting\Python\Modules\doliomodule.cpp:26 N[Scripting]: Script stdout: Velocity: 0.010605193674564362, Reward: 8.837661395470302e-05
# 35:59:604 Scripting\Python\Modules\doliomodule.cpp:26 N[Scripting]: Script stdout: Race Percent: 0.9938051104545593, Reward: 0.9938051104545593
# 35:59:604 Scripting\Python\Modules\doliomodule.cpp:26 N[Scripting]: Script stdout: Miniturbo: 0, Reward: 0
# 35:59:604 Scripting\Python\Modules\doliomodule.cpp:26 N[Scripting]: Script stdout: Total: 0.993893487068514
# 35:59:604 Scripting\Python\Modules\doliomodule.cpp:26 N[Scripting]: Script stdout: 0.993893487068514
# 35:59:609 Scripting\Python\Modules\doliomodule.cpp:26 N[Scripting]: Script stdout: loading savestate using f-key
# 35:59:717 Scripting\Python\Modules\doliomodule.cpp:26 N[Scripting]: Script stdout: Unregistering frameadvance listener for loading state
# Meaning the frameadvance listener is working after step() has finished. Adding a small delay inbetween and putting step in the event listener do not
# fix the issue