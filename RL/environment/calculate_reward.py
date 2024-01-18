from frame_processor import process_frame

# [0] = XZ Velocity
# [1] = Race%
# [2] = MT
# --- Constants --- 
NORMAL_MAX_SPEED = 84
MIN_ACCEPTABLE_SPEED = 70
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
    if S_current > NORMAL_MAX_SPEED:
        return 0.8
    if S_current > 70:
        return 0.5
    if racePercent < END_OF_FIRST_STRAIGHT and S_current > S_previous:
        return 0.2
    else:
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