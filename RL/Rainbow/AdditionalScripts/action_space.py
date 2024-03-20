# A script to generate all permutations of the abstracted controller

from itertools import product
# Returns and indexed dictionary of all controller permutations
def generate_action_space():
    # # Define the possible states for the buttons and analog stick
    # buttons = [True, False]
    # analog_stick_angles = [0, 64, 128, 192, 255]

    # # Generate all possible permutations using itertools.product
    # button_states = list(product(buttons, repeat=2))  # All possible combinations of 2 buttons

    # # Generate permutations and store them in a list of dictionaries
    # permutations = []
    # for button_state in button_states:
    #     for analog_state in analog_stick_angles:
    #         permutation_dict = {"B": button_state[0], "Up": button_state[1], "StickX": analog_state}
    #         jump_in_place = (button_state[0] == True and analog_state == 128)
    #         turn_in_wheelie = (button_state[1] == True and not analog_state == 128)
    #         if not (jump_in_place or turn_in_wheelie):
    #             permutations.append(permutation_dict)
    permutations = [{"B": True, "Up": False, "StickX": 0},{"B": True, "Up": False, "StickX": 64},{"B": True, "Up": False, "StickX": 192},{"B": True, "Up": False, "StickX": 255},{"B": False, "Up": True, "StickX": 128},]
    return permutations
    
