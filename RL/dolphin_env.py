# -- DOLHPIN IMPORTS --
from dolphin import event # gives awaitable routine that returns when a frame is drawn

#DEFAULT_CONTROLLER = {"A":True,"B":False,"Up":False,"StickX":128}
DEFAULT_CONTROLLER_LIST = [False, False, 128]
START_STATE = (76.332, 0.98, 0, 0)
PROJECT_DIR = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\'
MAX_EPISODES = 5000
TIME_STEP = 30 #Frames between each step

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
def convert_actions_to_dict(action):
    return {"A": True, "B": action[0],"Up": action[1],"StickX": action[2]}

## Initialisations
reward = 0
total_reward = 0
frame_counter = 0
termination_flag = False
frameInfo_previous = list(START_STATE)
is_logging = True
episode_counter = 0
controller_inputs = []
best_reward = 0
action = DEFAULT_CONTROLLER_LIST
reward_logging = False

## Q-Learning parameters
epsilon = 0.7  #Higher = more chance of random action
gamma = 0.6 # Higher = more focus on future rewards
alpha = 1 # Higher = newer Q-Values will have more impact

## Logging
## ---
date_and_time = datetime.now().strftime("%d_%m_%Y--%H-%M")

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
    await event.frameadvance()
    
    frame_counter += 1
    # Get frameInfo
    if frame_counter == 1:
    # If episode has jsut started don't reset
        frameInfo_current = list(START_STATE)
        termination_flag = False
        total_reward = 0
        total_reward_vel = 0
        total_reward_perc = 0
        total_reward_mt = 0
        total_reward_cp = 0
        reward = 0
    else:
        if frame_counter % TIME_STEP == 0 : 
            #--- Get current frame info
            frameInfo_current = getRaceInfo()
            # --- Check termination
            termination_flag = check_termination(frameInfo_current)    
           
            # -- Get action by epsilon-greedy policy
            action, action_choice = epsilon_greedy(tuple(frameInfo_current), epsilon)
            
            controller_inputs.append(action)
            # -- Calculate reward
            # TODO: Implement Checkpoint rewards
            reward, vel_reward, perc_reward, mt_reward, cp_reward = calculate_reward(frameInfo_current, frameInfo_previous)
            #print(vel_reward, perc_reward, mt_reward, cp_reward)
            
            # round float statespace values and remove cp
            frameInfo_rounded_current = map(lambda x: round(x, 2), frameInfo_current[:-1])
            frameInfo_rounded_previous = map(lambda x: round(x, 2), frameInfo_previous[:-1])
            
            # -- Update Q-Table
            q = update_q_table(tuple(frameInfo_rounded_previous), action, reward, tuple(frameInfo_rounded_current), alpha, gamma)
            
            # update previous_frame_info 
            frameInfo_previous = frameInfo_current
            # update total reward
            total_reward = total_reward + reward

            if reward_logging:
                # log individual reward values
                total_reward_vel += vel_reward
                total_reward_perc += perc_reward
                total_reward_mt += mt_reward
                total_reward_cp += cp_reward
                
                reward_log.write(f"{total_reward},{total_reward_vel},{total_reward_perc},{total_reward_mt},{total_reward_cp}\n")
                

            if termination_flag:
            # Reset
                q = update_q_table(tuple(frameInfo_previous), action, -10, tuple(frameInfo_current), alpha, gamma)
                # Log episode info
                if is_logging:
                    print(f"{episode_counter}, {total_reward}, {frame_counter}, {frameInfo_current}, {controller_inputs}\n")
                    log.write(f"{episode_counter}, {total_reward}, {frame_counter}")# {vel_reward}, {perc_reward}, {mt_reward}\n") # {q} , {frameInfo_current}\n")
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
                await load_savestate()
                continue

            # -- Send inputs to Dolphin
        sent_action = convert_actions_to_dict(action)
        set_controller(sent_action)