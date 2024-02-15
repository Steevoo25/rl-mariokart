# A script to generate all permutations of the abstracted controller

from itertools import product
# Returns and indexed dictionary of all controller permutations
def generate_action_space():
    # Define the possible states for the buttons and analog stick
    buttons = [True, False]
    analog_stick_angles = [0, 64, 128, 192, 256]

    # Generate all possible permutations using itertools.product
    button_states = list(product(buttons, repeat=3))  # All possible combinations of 3 buttons

    # Generate permutations and store them in a list of dictionaries
    permutations = []
    for button_state in button_states:
        for analog_state in analog_stick_angles:
            permutation_dict = {"A": button_state[0], "B": button_state[1], "Up": button_state[2], "StickX": analog_state}
            permutations.append(permutation_dict)

    action_dict = {}
    # Print all possible permutations of the controller as dictionaries
    for idx, permutation in enumerate(permutations):
        action_dict[idx] = permutation
    return action_dict

