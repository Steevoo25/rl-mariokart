# A script to generate all permutations of the abstracted controller

from itertools import product
# Returns and indexed dictionary of all controller permutations
def generate_action_space():
    # Define the possible states for the buttons and analog stick
    buttons = [True, False]
    analog_stick_angles = [0, 64, 128, 192, 255]

    # Generate all possible permutations using itertools.product
    button_states = list(product(buttons, repeat=2))  # All possible combinations of 3 buttons

    # Generate permutations and store them in a list of dictionaries
    permutations = []
    for button_state in button_states:
        for analog_state in analog_stick_angles:
            permutation_dict = {"B": button_state[0], "Up": button_state[1], "StickX": analog_state}
            permutations.append(permutation_dict)
    return permutations
    

