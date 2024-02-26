# A script that checks if the episode needs to terminate, given the current and previous raceInfo
# Constants
MIN_ACCEPTABLE_SPEED = 60
END_OF_FIRST_STRAIGHT = 1.073
LAP_COMPLETED = 2
RACE_COMPLETED = 4

def check_termination(raceInfo, accelerating : bool):
    vel, racePercent, mt = raceInfo
    
    # speed is too low
    if vel < MIN_ACCEPTABLE_SPEED:
        # give some leeway at start of race -> dont terminate
        if racePercent < END_OF_FIRST_STRAIGHT and accelerating:
            return False
        return True

    if racePercent > LAP_COMPLETED:
        return True
    # --- Uncomment if training for whole race
    # if racePercent > RACE_COMPLETED:
    #     return True
    return False