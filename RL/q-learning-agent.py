# An agent that uses Q-Learning
import random
# Constants
eps = 0.2

START_STATE = (1.128, 0.992, 0)

# Action Space
    # Action tuples contains a list of all possible inputs as tuples
from Rainbow.AdditionalScripts.action_space import generate_action_space
action_space = generate_action_space()
ACTION_COUNT = len(action_space) - 1 ## for indexing purposes

# Convert array of dictionaries to array of tuples
action_tuples = []
for dicts in action_space:
    action_tuples.append(tuple(dicts.values()))
    
# State Space
sample_state = (24.5, 34.5, 3)
# Q-Table
    # Table of Q values for each state-action pair
    # q[(s,a)] = q[((float, float, int), (Bool, Bool, Bool, int))]
q = {}
q[(sample_state), (True, True, True, 64)] = 1
q[(sample_state), (True, True, False, 64)] = 5
# Helper function to choose the best action in a given state 
# As my q-Table would be massive if I fully initialised it, I will check if a value exists in the try clause
# If it does exist, use that Q-Value
# If it does not exist then return 0

def choose_best(state, x):
    try:
        value = q[(state), (action_tuples[x])]
    except KeyError:
        value = 0
    finally:
        return value
# Epsilon-Greedy Policy
def epsilon_greedy(state, eps):
    # Pick random action with probability epsilon
    if random.uniform(0,1) < eps:
        return action_tuples[random.randint(0, ACTION_COUNT)]
    # Choose best action in current state with probability epsilon
    else:
        return action_tuples[max(range(ACTION_COUNT), key= lambda x : choose_best(state, x))]
        # Explanation of this line:
        # max() function gives index of best action, based on its q-value
        # action_tuples[] returns the action from its index
# Update Rule

