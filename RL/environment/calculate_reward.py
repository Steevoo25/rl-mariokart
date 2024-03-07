# [0] = XZ Velocity
# [1] = Race%
# [2] = MT

# --- Constants --- 
NORMAL_MAX_SPEED = 84
ABSOLUTE_MAX_VELOCITY = 120
MIN_ACCEPTABLE_SPEED = 65

CHARGED_MINITURBO = 270
NOT_CHARGING = 0
LAP_COMPLETE = 2

VELOCITY_WEIGHT = 1
RACE_PERCENT_WEIGHT = 25
MT_WEIGHT = 8

CP_REWARD = 20
LAP_COMPLETE_REWARD = 30
MT_FAILED_PENALTY = 50

def calculate_reward(frameInfo_current, frameInfo_previous):
    
    curr_vel, curr_racepercent, curr_mt, curr_cp = frameInfo_current
    prev_vel, prev_racepercent, prev_mt, prev_cp = frameInfo_previous
    
    #-- Velocity --
    # Need: Current speed, Previous speed, Current Race%
    R_vel = round(calculate_velocity_reward(curr_vel, prev_vel) * VELOCITY_WEIGHT, 5)
    
    #-- Race % --
    # Need: current and previous Race&
    R_racepercent = round(calculate_race_percent_reward(curr_racepercent, prev_racepercent) * RACE_PERCENT_WEIGHT, 5)
    
    #-- Miniturbo --
    # Need: Current and Previous MT
    R_mt = calculate_miniturbo_reward(curr_mt, prev_mt) * MT_WEIGHT
    
    R_cp = calculate_cp_reward(curr_cp, prev_cp)
    
    #print_rewards(R_vel, R_racepercent, R_mt, frameInfo_current)
    return round(R_vel + R_racepercent + R_mt + R_cp, 1), R_vel, R_racepercent, R_mt, R_cp
    
def calculate_velocity_reward(S_current: float, S_prev: float):

    # Scale velocity to value between 0 and 1
    S_scaled = S_current / ABSOLUTE_MAX_VELOCITY
    
    # if a boost has been performed
    if S_current > NORMAL_MAX_SPEED:
        return S_scaled * 1.6
    elif S_current > MIN_ACCEPTABLE_SPEED:
        return S_scaled
    else :
        return -S_scaled

# Options
# 1. return fixed amount if race% has increased
# 2. return a scaled percentage increase
#       -- This will decrease as race% increases
# 3. return a scaled flat difference
#       -- This will be most effective
def calculate_race_percent_reward(racePercent_current: float, racePercent_previous: float):
    
    difference = racePercent_current - racePercent_previous
    #print(f"Current: {racePercent_current}, Previous: {racePercent_previous}, Difference: {difference}")
    # Lap is complete
    if racePercent_current > LAP_COMPLETE:
        return LAP_COMPLETE_REWARD
    else:
        return difference * 100
    
def calculate_miniturbo_reward(mt_current: int, mt_previous:int):

    # miniturbo has been fully charged and released
    if mt_previous == CHARGED_MINITURBO:
        return 0.1
    # miniturbo is charging
    if mt_current > 0:
        return 0.05
    # no miniturbo being performed
    if mt_current == NOT_CHARGING:
        return 0
    # started miniturbo and released it before fully charging
    if mt_previous < CHARGED_MINITURBO and mt_current < mt_previous:
        return MT_FAILED_PENALTY
    
# Gives a static reward for reaching a checkpoint
def calculate_cp_reward(cp_current: int, cp_previous: int) -> int:
    if cp_current > cp_previous : return CP_REWARD
    else: return 0
    
def print_rewards(R_v, R_racepercent, R_mt, frameInfo):
    print(f'Velocity: {frameInfo[0]}, Reward: {R_v}')
    print(f'Race Percent: {frameInfo[1]}, Reward: {R_racepercent}')
    print(f'Miniturbo: {frameInfo[2]}, Reward: {R_mt}')
    print(f'Total: {R_v + R_racepercent + R_mt}')
    

# -- TESTING --

def test_speed():
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
