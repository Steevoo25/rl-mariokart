# -- DOLHPIN IMPORTS --
from dolphin import event # gives awaitable routine that returns when a frame is drawn
PROJECT_DIR = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\'

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
from pickle import dump
from datetime import datetime

from environment.load_savestate import load_using_fkey as load_savestate
from environment.press_button import press_button as set_controller
from environment.calculate_reward import calculate_reward
from environment.memory_viewer import getRaceInfo, getCurrentXZPos
from environment.termination_check import check_termination
from q_learning_agent import update_q_table, epsilon_greedy, save_q

DEFAULT_CONTROLLR_TUPLE = (False, False, 128)
START_STATE = (76, (-149, -54), (0, 0), False, 0)
# [0] = XZ Velocity
# [1] = XZ position
# [2] = (MTdirection, charge)
# [3] = Wheelie
# [4] = CP
MAX_EPISODES = 5000
TIME_STEP = 20 #Frames between each step

# A function to convert a tuple of actions (used in q-table as key) to a dict (to send to emulator)
def convert_actions_to_dict(action: tuple):
    return {"A": True, "B": action[0],"Up": action[1],"StickX": action[2]}

# A function to get the direction of a drift
# Returns 0 = not drifting, 1 = drifting left, 2 = drifting right
def specify_mt_direction(action):
    if action[0] == True: #if B is being pressed
        # Check direction of drift
        if action[2] < 128: # 1 is left
            return 1
        if action[2] > 128:
            return 2
    return 0

#--- Initialisations

episode_counter = 0

# Termination checking
termination_flag = False
just_reset = True

# State
stepInfo_previous = list(START_STATE)
action = DEFAULT_CONTROLLR_TUPLE
drift_direction = 0 # 0= not drifting, 1 = left, 2 = right

# Rewards
step_reward, total_reward, step_reward_vel, step_reward_perc, step_reward_mt, best_reward = 0,0,0,0,0,0

## Q-Learning parameters
epsilon = 0.6  #Higher = more chance of random action
gamma = 0.8 # Higher = more focus on future rewards
alpha = 0.6 # Higher = newer Q-Values will have more impact

## Logging
is_logging = True
controller_inputs = []
date_and_time = datetime.now().strftime("%d_%m_%Y--%H-%M")
if is_logging:
    log_file = f"{PROJECT_DIR}Evaluation\\data\\q-learning\\episodes\\q-learning-{date_and_time}.csv"
    log = open(log_file, 'w')

    # Column Headers
    log.write("Episode,Total_Reward,Frame_Count\n")

    # Controller Inputs 
    best_inputs_file = f"{PROJECT_DIR}Evaluation\\data\\q-learning\\controller_episodes\\q-learning-{date_and_time}.pkl"

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
    stepInfo_current = list(getRaceInfo()) # cast as list as we are going to edit it
    
    # If we are drifting check direction
    if stepInfo_previous[2][1] == 0 or stepInfo_current[2] == 0:
        drift_direction = specify_mt_direction(action)
    # Update mt info
    stepInfo_current[2] = drift_direction, stepInfo_current[2]
    
    # Calculate Reward
    step_reward, step_reward_vel, step_reward_perc, step_reward_mt = calculate_reward(stepInfo_current, stepInfo_previous)
    termination_flag = check_termination(stepInfo_current[:2])
    # Add xz pos for q table
    stepInfo_current[1] = getCurrentXZPos()
    print("Current state", stepInfo_current)        
    print("Reward gained:", step_reward)
    print("vel_reward", step_reward_vel, "perc_reward", step_reward_perc, "mt reward", step_reward_mt)

    # -- Update Q-Table
    q = update_q_table(tuple(stepInfo_previous[:-1]), action, step_reward, tuple(stepInfo_current[:-1]), alpha, gamma)

    if termination_flag:
        # terminating gives -ve reward
        step_reward = -100
        #print("Reward gained:", step_reward)
        print("Terminating, updating: ", stepInfo_previous, " with reward ", step_reward)
        update_q_table(tuple(stepInfo_previous[:-1]), action, step_reward, tuple(stepInfo_current[:-1]), alpha, gamma)
        
        # Log episode info
        if is_logging:
            log.write(f"{episode_counter}, {total_reward},\n")#
            # If its the best we've seen
            if total_reward > best_reward:
                # update best reward
                best_reward = total_reward
                # save controller inputs to pkl file
                dump(controller_inputs, open(f'{best_inputs_file}', "wb"))
            controller_inputs = []

        # Reset for next episode
        episode_counter += 1
        termination_flag = False
        action = DEFAULT_CONTROLLR_TUPLE
        just_reset = True
        
        if episode_counter % TIME_STEP == 0: # save q table every 20 episodes
            save_q()         
        await load_savestate()
        continue
    else:
        # Next Step
        just_reset = False
        total_reward = total_reward + step_reward
        step_reward = 0
        stepInfo_previous = stepInfo_current