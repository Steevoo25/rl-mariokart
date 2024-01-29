from memory_viewer import getRaceInfo

# [0] = XZ Velocity
# [1] = Race%
# [2] = MT

# --- Constants --- 
NORMAL_MAX_SPEED = 84
ABSOLUTE_MAX_VELOCITY = 120
MIN_ACCEPTABLE_SPEED = 65
END_OF_FIRST_STRAIGHT = 1.073
CHARGED_MINITURBO = 270
NOT_CHARGING = 0

def calculate_reward(frameInfo_previous):
    # Get current frame values
    frameInfo_current = getRaceInfo()
    
    #-- Velocity --
    # Need: Current speed, Previous speed, Current Race%
    velocity_calculation_info = frameInfo_current[0], frameInfo_previous[0], frameInfo_current[1]
    R_v = calculate_velocity_reward(velocity_calculation_info)
    
    #-- Race % --
    # Need: current and previous Race&
    racePercent_calculation_info = frameInfo_current[1], frameInfo_previous[1]
    R_racepercent = calculate_race_percent_reward(racePercent_calculation_info)
    
    #-- Miniturbo --
    # Need: Current and Previous MT
    mt_calculation_info = frameInfo_current[2], frameInfo_previous[2]
    R_mt = calculate_miniturbo_reward(mt_calculation_info)
    
    # Print rewards to log
    print_rewards(R_v,R_racepercent,R_mt, frameInfo_current)
    return R_v + R_racepercent + R_mt
    
def calculate_velocity_reward(S_current: float, S_previous:float, racePercent: float):
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

def calculate_race_percent_reward(racePercent_current: float, racePercent_previous: float):

    return 1
    
def calculate_miniturbo_reward(mt_current: int, mt_previous:int):
    # miniturbo has been fully charged and released
    if mt_previous == CHARGED_MINITURBO:
        return 0.2
    # miniturbo is charging
    if mt_current > mt_previous:
        return 0.01
    # no miniturbo being performed
    if mt_current == NOT_CHARGING:
        return 0
    # started miniturbo and released it before fully charging
    if mt_previous < CHARGED_MINITURBO and mt_current < mt_previous:
        return -0.2
    
def print_rewards(R_v,R_racepercent,R_mt, frameInfo):
    print(f'Velocity:{frameInfo[0]}, Reward:{R_v}')
    print(f'Race Percent:{frameInfo[1]}, Reward:{R_racepercent}')
    print(f'Miniturbo:{frameInfo[2]}, Reward:{R_mt}')
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
