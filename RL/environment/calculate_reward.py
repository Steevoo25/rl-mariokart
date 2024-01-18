from frame_processor import process_frame

def calculate_reward(prev_frame_values):
    process_frame(1)
    

def calculate_velocity_reward(velocity: float, racePercent: float):
    return 1
    
def calculate_race_percent_reward(racePercent: float):
    return 1
    
def calculate_miniturbo_reward(miniturbo: int):
    return 1
    