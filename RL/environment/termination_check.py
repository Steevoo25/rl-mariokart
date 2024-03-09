# A script that checks if the episode needs to terminate, given the current and previous raceInfo
# Constants
MIN_ACCEPTABLE_SPEED = 69
LAP_COMPLETED = 2
RACE_COMPLETED = 4

def check_termination(raceInfo) -> bool:
    vel, racePercent = raceInfo
    
    # speed is too low
    if vel < MIN_ACCEPTABLE_SPEED:
        return True

    if racePercent > LAP_COMPLETED:
        return True
    # --- Uncomment if training for whole race
    # if racePercent > RACE_COMPLETED:
    #     return True
    return False