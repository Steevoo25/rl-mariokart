
# -- DOLHPIN IMPORTS --
from dolphin import event # gives awaitable routine that returns when a frame is drawn

DEFAULT_CONTROLLER = {"A":True,"B":False,"Up":False,"StickX":128}
START_STATE = (76.332, 1.019, 0)
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
import logging
from pickle import dump
from datetime import datetime

from environment.load_savestate import load_using_fkey as load_savestate
from environment.press_button import press_button as set_controller
from environment.calculate_reward import calculate_reward
from environment.memory_viewer import getRaceInfo
from environment.termination_check import check_termination
from q_learning_agent import update_q_table, epsilon_greedy, get_q_table

def print_state_to_dolphin_log(episode, frame, speed, racePercent, mt, reward):
    print(f'''Episode: {episode} Frame: {frame}, Speed: {speed}, Race%: {racePercent}, Miniturbo: {mt}, Reward: {reward}''')

# A helper function to convert a tuple of actions (used in the q-learning process) to a dictionary (to send to emulator)
def convert_actions_to_dict(action):
    return {"A": True, "B": action[0],"Up": action[1],"StickX": action[2]}

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
termination_flag = False
frameInfo_previous = list(START_STATE)
is_logging = True
reset_requested = False
episode_counter = 0
controller_inputs = []
best_reward = 0

reward_logging = False
total_reward_vel = 0
total_reward_perc = 0
total_reward_mt = 0

## Q-Learning parameters
epsilon = 0.7  #Higher = more chance of random action
gamma = 0.6 # Higher = more focus on future rewards
alpha = 1 # Higher = newer Q-Values will have more impact

## Logging

date_and_time = datetime.now().strftime("%d_%m_%Y--%H-%M")

log_file = f"{PROJECT_DIR}Evaluation\\data\\q-learning-{date_and_time}.csv"
log = open(log_file, 'w')

# Column Headers
log.write("Episode,Total_Reward,Frame_Count,Velocity_Reward,RacePercent_Reward,MT_Reward\n")

# Controller Inputs 
best_inputs_file = f"{PROJECT_DIR}Evaluation\\controller_episodes\\q-learning-{date_and_time}.pkl"
if reward_logging:
    reward_log_file = f"{PROJECT_DIR}Evaluation\\data\\rewards\\q-learning-{date_and_time}.csv"
    reward_log = open(reward_log_file, 'w')
    reward_log.write("total_reward,vel_reward,perc_reward,mt_reward")

### Main Training Loop ###
# -------------------------

while episode_counter < MAX_EPISODES:
    await event.frameadvance()
    frame_counter += 1
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
        # --- Check termination
        termination_flag = check_termination(frameInfo_current)
    
    # --- Get response from Rainbow based on previous frame
    response = json.loads(env_socket.recv(131702).decode("utf-8"))
    
    
    action = response[0]
    print("action ", action)
    reset_requested = response[1]

    # -- Calculate reward
    reward, vel_reward, perc_reward, mt_reward = calculate_reward(frameInfo_current, frameInfo_previous)
    #print(vel_reward, perc_reward, mt_reward)
    
    
    # -- Send data to Rainbow
    # encode data as json object and send to agent process
    data_to_send = json.dumps((reward, termination_flag, frame_counter)).encode("utf-8")
    env_socket.sendall(data_to_send)
    
    # update previous_frame_info 
    frameInfo_previous = frameInfo_current
    # update total reward
    total_reward = total_reward + reward

    if reward_logging:
        # log individual reward values
        total_reward_vel += vel_reward
        total_reward_perc += perc_reward
        total_reward_mt += mt_reward
        
        reward_log.write(f"{total_reward},{total_reward_vel},{total_reward_perc},{total_reward_mt}")
        
        
    if is_logging:
    # Print state to dolphin log
        print_state_to_dolphin_log(episode_counter, frame_counter, *frameInfo_current, reward)
        #print(f"{episode_counter}, {reward}, {frame_counter}, {q}, {action}, {frameInfo_current}\n")
        

    if termination_flag:
    # Reset
        q = update_q_table(tuple(frameInfo_previous), action, -10, tuple(frameInfo_current), alpha, gamma)
        # Log episode info
        print(f"{episode_counter}, {total_reward}, {frame_counter}, {q},  {frameInfo_current}, {controller_inputs}\n")
        log.write(f"{episode_counter}, {total_reward}, {frame_counter}, {vel_reward}, {perc_reward}, {mt_reward}\n") # {q} , {frameInfo_current}\n")
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


    # -- Send inputs to Dolphin
    action = convert_actions_to_dict(action)
    controller_inputs.append(action)
    set_controller(action)