
# -- DOLHPIN IMPORTS --
from dolphin import event # gives awaitable routine that returns when a frame is drawn
DEFAULT_CONTROLLER_LIST = [False, False, 128]
DEFAULT_CONTROLLER = {"A":True,"B":False,"Up":False,"StickX":128}
START_STATE = (76.332, 0.9, 0, 0)
PROJECT_DIR = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\'
MAX_EPISODES = 5000

# As the script is run within the dolphin executable, 
# Append the true path of scripts to import
from sys import path

# Add venv dir to path to allow external packages
venv_dir =f'{PROJECT_DIR}venv\\Lib\\site-packages'
path.append(venv_dir)
# Add this dir to path to allow imports from other scripts
this_dir = f'{PROJECT_DIR}RL'
path.append(this_dir)

# -- OTHER IMPORTS --
import socket
import json
from pickle import dump
from datetime import datetime

from environment.load_savestate import load_using_fkey as load_savestate
from environment.press_button import press_button as set_controller
from environment.calculate_reward import calculate_reward
from environment.memory_viewer import getRaceInfo
from environment.termination_check import check_termination

def print_state_to_dolphin_log(episode, frame, frameInfo:tuple, reward):
    print(f'''Episode: {episode} Frame: {frame}, FrameInfo: {frameInfo}, Reward: {reward}''')

## Socket Initialisation
# This script will be running within Dolphin's embedded python, meaning it has a lot of limitations
# To get around these I will send the environment data to a seperate Agent script

HOST = socket.gethostname()
PORT = 5555
print(f'Host : {HOST}')
env_socket = socket.socket()
env_socket.connect((HOST,PORT)) # Uncomment when training

## Initialisations
reward = 0
total_reward = 0
frame_counter = 0
step_reward = 0
file_number = -1
termination_flag = False
frameInfo_previous = list(START_STATE)
is_logging = True
reset_requested = False
episode_counter = 0
controller_inputs = []
best_reward = 0
action = DEFAULT_CONTROLLER

## Logging

date_and_time = datetime.now().strftime("%d_%m_%Y--%H-%M")

log_file = f"{PROJECT_DIR}Evaluation\\data\\deep-learning\\episodes\\deep-learning-{date_and_time}.csv"
log = open(log_file, 'w')

# Column Headers
log.write("Episode,Total_Reward,Frame_Count,Velocity_Reward,RacePercent_Reward,MT_Reward\n")

# Controller Inputs 
best_inputs_file = f"{PROJECT_DIR}Evaluation\\data\\deep-learning\\controller_episodes\\deep-learning{date_and_time}.pkl"

### Main Training Loop ###
# -------------------------
await load_savestate()
while episode_counter < MAX_EPISODES:
    await event.frameadvance()
    frame_counter += 1
    file_number += 1
    # Get frameInfo
    if frame_counter == 1:
    # If episode has jsut started don't reset
        frameInfo_current = list(START_STATE)
        termination_flag = False
        total_reward = 0
        reward = 0
    else:
    #--- Get current frame info
        frameInfo_current = getRaceInfo()
        reward, _, _, _, _ = calculate_reward(frameInfo_current, frameInfo_previous)
        step_reward += reward
            # --- Check termination
        termination_flag = check_termination(frameInfo_current)

        if frame_counter % 8 == 0 : 
            
        # --- Get response from Rainbow based on previous frame
            response = json.loads(env_socket.recv(131702).decode("utf-8"))
            action = response[0]
            controller_inputs.append(action)
            print("action ", action)
            reset_requested = response[1]
            print("reset_requested", reset_requested)    
        
        # -- Send data to Rainbow
        # encode data as json object and send to agent process
            data_to_send = json.dumps((step_reward, termination_flag, frame_counter, file_number)).encode("utf-8")
            env_socket.sendall(data_to_send)
            
            if is_logging:
        # Print state to dolphin log
                print_state_to_dolphin_log(episode_counter, frame_counter, frameInfo_current, reward)
            #print(f"{episode_counter}, {reward}, {frame_counter}, {q}, {action}, {frameInfo_current}\n")
            

            if termination_flag:# or reset_requested:
        # Reset
            # Log episode info
                print(f"{episode_counter}, {total_reward}, {frame_counter},  {frameInfo_current}, {controller_inputs}\n")
                log.write(f"{episode_counter}, {total_reward}, {frame_counter}\n")#" {vel_reward}, {perc_reward}, {mt_reward}\n") # {q} , {frameInfo_current}\n")
            # If its the best we've seen
                if total_reward > best_reward:
                # update best reward
                    best_reward = total_reward
                # save controller inputs to pkl file
                    dump(controller_inputs, open(f'{best_inputs_file}', "wb"))
                
                frame_counter = 0
                episode_counter += 1
                controller_inputs = []
                frameInfo_previous = list(START_STATE)
                await load_savestate()
                continue

            step_reward = 0

        # update previous_frame_info 
        frameInfo_previous = frameInfo_current  
        # update total reward
        total_reward = total_reward + step_reward
         # -- Send inputs to Dolphin
    action["A"] = True
    set_controller(action)