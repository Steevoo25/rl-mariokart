# -- DOLHPIN IMPORTS --
from dolphin import event # gives awaitable routine that returns when a frame is drawn

#DEFAULT_CONTROLLER = {"A":True,"B":False,"Up":False,"StickX":128}
DEFAULT_CONTROLLR_TUPLE = (False, False, 128)

START_STATE = (76, 0.98, 0, False, 0)
# [0] = XZ Velocity
# [1] = Race%
# [2] = MT
# [3] = Wheelie
# [4] = CP

PROJECT_DIR = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\'
MAX_EPISODES = 5000
TIME_STEP = 20 #Frames between each step

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
import json
import logging
import math
from pickle import dump
from datetime import datetime

from environment.load_savestate import load_using_fkey as load_savestate
from environment.press_button import press_button as set_controller
from environment.calculate_reward import calculate_reward
from environment.memory_viewer import getRaceInfo
from environment.termination_check import check_termination
from q_learning_agent import update_q_table, epsilon_greedy, get_q_table

def print_state_to_dolphin_log(episode, frame, speed, racePercent, mt, reward, q, action_choice):
    print(f'''Episode: {episode} Frame: {frame}, Speed: {speed}, Race%: {racePercent}, Miniturbo: {mt}, Reward: {reward}, Q-Value: {q}, Action Choice: {action_choice}''')

# A helper function to convert a tuple of actions (used in the q-learning process) to a dictionary (to send to emulator)
def convert_actions_to_dict(action: tuple):
    return {"A": True, "B": action[0],"Up": action[1],"StickX": action[2]}

def specify_mt_direction(action):
    if action[0] == True: #if B is being pressed
        # Check direction of drift
        if action[2] < 128: # 1 is left
            return 1
        if action[2] > 128:
            return 2
    return 0

## Initialisations
frame_reward = 0
step_reward = 0
total_reward = 0
frame_counter = 0
termination_flag = False
frameInfo_previous = list(START_STATE)
stepInfo_previous = list(START_STATE)
is_logging = False
episode_counter = 0
controller_inputs = []
best_reward = 0
action = DEFAULT_CONTROLLR_TUPLE
reward_logging = False
drift_direction = 0 # 0= not drifting, 1 = left, 2 = right
just_reset = True

step_reward_vel = 0
step_reward_perc = 0
step_reward_mt = 0
step_reward_cp = 0

## Q-Learning parameters
epsilon = 0.6  #Higher = more chance of random action
gamma = 0.5 # Higher = more focus on future rewards
alpha = 0.7 # Higher = newer Q-Values will have more impact

## Logging
## ---
date_and_time = datetime.now().strftime("%d_%m_%Y--%H-%M")
if is_logging:
    log_file = f"{PROJECT_DIR}Evaluation\\data\\q-learning\\episodes\\q-learning-{date_and_time}.csv"
    log = open(log_file, 'w')

    # Column Headers
    log.write("Episode,Total_Reward,Frame_Count\n")

    # Controller Inputs 
    best_inputs_file = f"{PROJECT_DIR}Evaluation\\data\\q-learning\\controller_episodes\\q-learning-{date_and_time}.pkl"
if reward_logging:

    total_reward_vel = 0
    total_reward_perc = 0
    total_reward_mt = 0    
    total_reward_cp = 0
    
    reward_log_file = f"{PROJECT_DIR}Evaluation\\data\\q-learning\\rewards\\q-learning-{date_and_time}.csv"
    reward_log = open(reward_log_file, 'w')
    reward_log.write("total_reward,vel_reward,perc_reward,mt_reward,cp_reward\n")

### Main Training Loop ###
# -------------------------

while True:

    if just_reset:
    # If episode has jsut started don't reset
        print("-" * 10, "NEW EPISODE: ", episode_counter)
        stepInfo_previous = list(START_STATE)
        termination_flag = False
        total_reward = 0
        step_reward = 0

    # -- Get action by epsilon-greedy policy
    action, action_choice = epsilon_greedy(tuple(stepInfo_previous[:-1]), epsilon)
    print(action_choice , "in state", stepInfo_previous[:-1], "with action", action) 
    controller_inputs.append(action)   

    # Perform action and move to next state
    for _ in range(TIME_STEP):
        sent_action = convert_actions_to_dict(action)
        set_controller(sent_action)
        await event.frameadvance()
        
    # Recieve reward
    stepInfo_current = list(getRaceInfo())
    step_reward, step_reward_vel, step_reward_perc, step_reward_mt, step_reward_cp = calculate_reward(stepInfo_current, stepInfo_previous)
    termination_flag = check_termination(stepInfo_current[:2])

    # If we are drifting check direction
    if stepInfo_previous[2] == 0 or stepInfo_current[2] == 0:
        drift_direction = specify_mt_direction(action)
        #print("drift_direction", drift_direction)

    if stepInfo_current[2] > 0:
        stepInfo_current[2] = drift_direction



    print("Current state", stepInfo_current)        
    print("Reward gained:", step_reward)
    print("vel_reward", step_reward_vel, "perc_reward", step_reward_perc)

    # -- Update Q-Table
    q = update_q_table(tuple(stepInfo_previous[:-1]), action, step_reward, tuple(stepInfo_current[:-1]), alpha, gamma, epsilon)

    if termination_flag:
        # If it terminates while holing mt
        if stepInfo_current[2] > 0:
            step_reward = step_reward - 10
        #print("Reward gained:", step_reward)
        print("Terminating, updating: ", stepInfo_previous, " with reward ", step_reward)
        update_q_table(tuple(stepInfo_previous[:-1]), action, step_reward, tuple(stepInfo_current[:-1]), alpha, gamma, epsilon)
        #print(f"{episode_counter}, {total_reward}, {frame_counter}, {frameInfo_current}, {controller_inputs}\n")
        
        # Log episode info
        if is_logging:
            log.write(f"{episode_counter}, {total_reward}, {frame_counter}\n")# {vel_reward}, {perc_reward}, {mt_reward}\n") # {q} , {frameInfo_current}\n")
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
        termination_flag = False
        action = DEFAULT_CONTROLLR_TUPLE
        just_reset = True

        await load_savestate()
        continue
    else:
        just_reset = False  
        total_reward = total_reward + step_reward      
        step_reward = 0
        stepInfo_previous = stepInfo_current