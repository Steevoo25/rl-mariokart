# -- DOLHPIN IMPORTS --
from dolphin import event # gives awaitable routine that returns when a frame is drawn

DEFAULT_CONTROLLER = {"A":True,"B":False,"Up":False,"StickX":128}
START_STATE = (1.128, 0.992, 0)

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
import json
import logging

from environment.load_savestate import load_using_fkey as load_savestate
from environment.press_button import press_button as set_controller
from environment.calculate_reward import calculate_reward
from environment.memory_viewer import getRaceInfo
from environment.termination_check import check_termination
from q_learning_agent import update_q_table, epsilon_greedy

def print_state_to_dolphin_log(frame, speed, racePercent, mt, reward, total_reward):
    print(f'''Frame: {frame}
    Speed: {speed}
    Race%: {racePercent}
    Miniturbo: {mt}
    Reward: {reward}
    Total Reward: {total_reward}''')

# A helper function to convert a tuple of actions (used in the q-learning process) to a dictionary (to send to emulator)
def convert_actions_to_dict(action):
    return {"A": action[0],"B": action[1],"Up": action[2],"StickX": action[3]}

## Socket Initialisation
# This script will be running within Dolphin's embedded python, meaning it has a lot of limitations
# To get around these I will send the environment data to a seperate Agent script

HOST = socket.gethostname()
PORT = 5555
print(f'Host : {HOST}')
env_socket = socket.socket()
#env_socket.connect((HOST,PORT)) # Uncomment when training

## Initialisations
reward = 0
total_reward = 0
frame_counter = 0
termination_flag = False
frameInfo_previous = list(START_STATE)
is_logging = False
reset_requested = False
episode_counter = 0
controller_inputs = []

epsilon = 0.8
gamma = 1
alpha = 0.4

log = open("C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\Evaluation\\q-learning.log", 'w')
### Main Training Loop ###

while True:
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
        frameInfo_current = getRaceInfo()
        # --- Check termination
        accelerating = frameInfo_current[0] > frameInfo_previous[0]
        termination_flag = check_termination(frameInfo_current, accelerating)
        # --- Get response from Rainbow based on previous frame
        #response = json.loads(env_socket.recv(131702).decode("utf-8"))
        #response = [DEFAULT_CONTROLLER, True]
        #action = response[0]
        #reset_requested = response[1]
        
    # -- Get action by epsilon-greedy policy
    action = epsilon_greedy(tuple(frameInfo_current), eps=epsilon)
    
    # -- Calculate reward
    reward = calculate_reward(frameInfo_current, frameInfo_previous)
    # -- Update Q-Table
    update_q_table(tuple(frameInfo_previous), action, reward, tuple(frameInfo_current), alpha, gamma)
    
    # update previous_frame_info 
    frameInfo_previous = frameInfo_current
    # update total reward
    total_reward = total_reward + reward

    if is_logging:
    # Print state to dolphin log
        print_state_to_dolphin_log(frame_counter, *frameInfo_current, reward, total_reward)

    if termination_flag:
    # Reset
        #print(f"{episode_counter}, {reward}, {frame_counter}, {frameInfo_current}\n")
        log.write(f"{episode_counter}, {reward}, {frame_counter}, {frameInfo_current}, {controller_inputs}\n")
        frame_counter = 0
        episode_counter += 1
        controller_inputs = []
        await load_savestate()
        continue

    # -- Send data to Rainbow
    # encode data as json object and send to agent process
    # data_to_send = json.dumps((reward, termination_flag, frame_counter)).encode("utf-8")
    # env_socket.sendall(data_to_send)

    # -- Send inputs to Dolphin
    action = convert_actions_to_dict(action)
    controller_inputs.append(action)
    set_controller(action)