def generate_action_space():
    permutations = [{"B": True, "Up": False, "StickX": 0}, # hard drift left
    {"B": True, "Up": False, "StickX": 64}, # soft drift left
    {"B": True, "Up": False, "StickX": 192}, # soft drift right
    {"B": True, "Up": False, "StickX": 255}, # hard drift right
    {"B": False, "Up": True, "StickX": 128}, # wheelie straight
    {"B": False, "Up": False, "StickX": 64}, # slight turn left
    {"B": False, "Up": False, "StickX": 192}] # sligh turn right
    return permutations
