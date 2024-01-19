from frame_processor import process_frame

# [0] = XZ Velocity
# [1] = Race%
# [2] = MT
# --- Constants --- 
NORMAL_MAX_SPEED = 84
ABSOLUTE_MAX_VELOCITY = 120
MIN_ACCEPTABLE_SPEED = 65
END_OF_FIRST_STRAIGHT = 1.073

def calculate_reward(frameInfo_previous):
    # Get current frame values
    frameInfo_current = process_frame(1)
    # Calculate Rewards for each value
    R_v = calculate_velocity_reward(frameInfo_current[0], frameInfo_previous[0], frameInfo_current[1])
    R_racepercent = calculate_race_percent_reward(frameInfo_current[1])
    R_mt = calculate_miniturbo_reward(frameInfo_current[2], frameInfo_previous[2])
    # Print rewards to log
    print_rewards(R_v,R_racepercent,R_mt, frameInfo_current)
    return R_v + R_racepercent + R_mt
    
def calculate_velocity_reward(S_current: float,S_previous:float, racePercent: float):
    # Scale velocity to value between 1 and 2
    S_scaled = S_current / ABSOLUTE_MAX_VELOCITY
    # if a boost has been performed
    if S_current > NORMAL_MAX_SPEED:
        return S_scaled * 1.2
    # Normal driving
    if S_current >= MIN_ACCEPTABLE_SPEED:
        return S_scaled
    # Speed is low but we are at the start of the episode so dont reset
    if racePercent < END_OF_FIRST_STRAIGHT and S_current > S_previous:
        return S_scaled
    # Speed is low after start of race OR speed is low and not accelerating at start of race
    else:
    # A return value of 0 results in the episode resetting
        return 0

def calculate_race_percent_reward(racePercent: float):
    return 1
    
def calculate_miniturbo_reward(mt_current: int, mt_previous:int):
    return 1
    
def print_rewards(R_v,R_racepercent,R_mt, frameInfo):
    print(f'Velocity:{frameInfo[0]}, Reward:{R_v}')
    print(f'Race Percent:{frameInfo[1]}, Reward:{R_racepercent}')
    print(f'Miniturbo:{frameInfo[2]}, Reward:{R_mt}')
    print(f'Total: {R_v + R_racepercent + R_mt}')
    
    
# -- TESTING --
# Speed is greater than normal -> bonus Reward
print(f"Speed greater than normal Reward: {calculate_velocity_reward(90,90,1)}")

# Speed is normal (top speed) -> Normal reward
print(f"Speed as expected Reward: {calculate_velocity_reward(84,84,1)}")

# Speed is low and not accelerating at start of race -> no reward (end)
print(f"Speed low but start of race (not accelerating) Reward: {calculate_velocity_reward(50,50,1)}")

# Speed is low and accelerating at start of race -> normal reward
print(f"Speed low but start of race (accelerating) Reward: {calculate_velocity_reward(50,40,1)}")

# Speed is low and it is not the start of the race -> no reward (end)
print(f"Speed low and not start of race: {calculate_velocity_reward(50,50,2)}")
