# A script that checks if the episode needs to terminate, given the current and previous raceInfo
# Constants
from memory_viewer import getCurrentRoadType
MIN_ACCEPTABLE_SPEED = 60
LAP_COMPLETED = 2
RACE_COMPLETED = 4
OFFROAD = 3

def check_termination(raceInfo) -> bool:
    vel, racePercent = raceInfo
    
    if getCurrentRoadType() == OFFROAD:
        return True
    # speed is too low
    if vel < MIN_ACCEPTABLE_SPEED:
        return True
    # if racePercent > LAP_COMPLETED:# --- Uncomment if training for lap
    #     return True
    if racePercent > RACE_COMPLETED:
        return True
    return False