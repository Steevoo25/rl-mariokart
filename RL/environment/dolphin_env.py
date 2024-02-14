# -- DOLHPIN IMPORTS --
#from dolphin import savestate # for loading savestates
from dolphin import event # for resetting emulation

DEFAULT_CONTROLLER = {"A":False,"B":False,"Up":False,"StickX":128}

# As the script is run within the dolphin executable, 
# Append the true path of scripts to import
from sys import path, getsizeof

# Add venv dir to path to allow external packages
venv_dir ='C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\venv\\Lib\\site-packages'
path.append(venv_dir)
# Add this dir to path to allow imports from other scripts
this_dir = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\RL'
path.append(this_dir)

# -- OTHER IMPORTS --
import socket
import json

from load_savestate import load_using_fkey as load_savestate
from press_button import press_button as set_controller
from calculate_reward import calculate_reward
from memory_viewer import getRaceInfo
from termination_check import check_termination

def print_state_to_dolphin_log(frame, speed, racePercent, mt, terminate, reward, total_reward):
    print(f'''Frame: {frame}
    Speed: {speed}
    Race%: {racePercent}
    Miniturbo: {mt}
    Termination Flag: {terminate}
    Reward: {reward}
    Total Reward: {total_reward}''')

## Socket Initialisation
# This script will be running within Dolphin's embedded python, meaning it has a lot of limitations
# To get around these I will send the environment data to a seperate Agent script

HOST = socket.gethostname()
PORT = 5555
print(f'Host : {HOST}')
env_socket = socket.socket()
#env_socket.connect((HOST,PORT)) # Uncomment when training

## Initialisations
frameInfo_previous = [0,0,0]
reward = 0
total_reward = 0
frame_counter = 0
termination_flag = False

### Main Training Loop ###
just_reset = False

while True:
    await event.frameadvance()
    frame_counter +=1
    # Get frameInfo
    if frame_counter == 1:
        frameInfo_current = [0,0,0]
    else:
        frameInfo_current = getRaceInfo()
    
    # Check termination
    # -----
    # Termination Conditions
    accelerating = frameInfo_current[0] > frameInfo_previous[0]
    termination_flag = check_termination(frameInfo_current, accelerating)
    # Low speed
    # Race is complete
    
    # Get response from previous frame
    # -----
    # action
    action = DEFAULT_CONTROLLER
    # reset
    
    # -- Calculate reward
    reward = calculate_reward(frameInfo_current, frameInfo_previous)
    # update previous_frame_info 
    frameInfo_previous = getRaceInfo()
    # update total reward
    total_reward = total_reward + reward
    # Rainbow is configured to take 4 things
    # pixel Value - this is done within the rainbow process
        # Print state to dolphin log
    print_state_to_dolphin_log(frame_counter, *frameInfo_current, termination_flag, reward, total_reward )
    # Reward Value
    # termination flag
    # frame counter
    # -- Send data to Rainbow
    # encode data as json object and send to agent process

    data_to_send = json.dumps((reward, termination_flag, frame_counter)).encode("utf-8")
    
    # env_socket.sendall(data_to_send)
    # -- Send inputs to Dolphin
    set_controller(action)