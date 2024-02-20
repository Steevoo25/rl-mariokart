# An agent that uses Q-Learning
import random
# Constants
eps = 0.2

# Action Space
    # Action tuples contains a list of all possible inputs as tuples
from Rainbow.AdditionalScripts.action_space import generate_action_space
action_space = generate_action_space()
action_tuples = []
for dicts in action_space:
    action_tuples.append(tuple(dicts.values()))
# State Space

# Q-Table
    # Table of Q values for each state-action pair
    # q[(s,a)] = q[(("vel": float, "RacePerc": float, "mt": int), )]
# I dont want to store all the q-values for every state and action straight away
# I will check if a value exists and return 0 if not
q = {}
# q[()]
# Epsilon-Greedy Policy
def epsilon_greedy(state, eps):
    # Pick random action with probability epsilon
    if random.uniform(0,1) < eps:
        return 1
    # Choose best action in current state with probability epsilon
    else:
        return 0
        
# Update Rule
