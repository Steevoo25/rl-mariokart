# An agent that uses Q-Learning
import random
# Constants
eps = 0.2

START_STATE = (1.128, 0.992, 0)

# Action Space
    # Action tuples contains a list of all possible inputs as tuples
from Rainbow.AdditionalScripts.action_space import generate_action_space
action_space = generate_action_space()
TOTAL_ACTIONS = len(action_space)

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
# Epsilon-Greedy Policy
def epsilon_greedy(state, eps):
    # Pick random action with probability epsilon
    if random.uniform(0,1) < eps:
        return action_tuples[random.randint(0,TOTAL_ACTIONS - 1)]
    # Choose best action in current state with probability epsilon
    else:
        return max()
print(epsilon_greedy(1, eps))
# Update Rule
