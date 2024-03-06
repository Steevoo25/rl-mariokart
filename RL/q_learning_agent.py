# An agent that uses Q-Learning
import random

# Action Space
    # Action tuples contains a list of all possible inputs as tuples
from Rainbow.AdditionalScripts.action_space import generate_action_space
action_space = generate_action_space()
ACTION_COUNT = len(action_space) - 1 ## for indexing purposes

# Convert array of dictionaries to array of tuples
action_tuples = []
for dicts in action_space:
    action_tuples.append(tuple(dicts.values()))
    
# Q-Table
    # Table of Q values for each state-action pair
    # q[(s,a)] = q[((float, float, int), (Bool, Bool, Bool, int))]
    # q-value of unvisited state-action pairs is undefined, meaning i need the helper functions
q = {}
# Helper function to choose the best action in a given state 
# As my q-Table would be massive if I fully initialised it, I will check if a value exists in the try clause
# If it does exist, use that Q-Value
# If it does not exist then return 0

def handle_unassigned_q_index(state, x):
    try:
        value = q[(state), (action_tuples[x])]
    except KeyError:
        value = 0
    finally:
        return value

def handle_unassigned_q_action(next_state, action):
    try:
        value = q[next_state, action]
    except KeyError:
        value = 0
    finally:
        return value

# --- Epsilon-Greedy Policy
def epsilon_greedy(state, eps):
    # If all actions have been explored, always move to it
    # count all occurences of state in q
    count = sum(1 for key in q.keys() if key[0] == state)
    if count == ACTION_COUNT: 
        eps = -1 # always return best
        print("Fully explored:", state)
    # Pick random action with probability epsilon
    if random.uniform(0,1) < eps:
        return action_tuples[random.randint(0, ACTION_COUNT)], 'Exploring'
    # Choose best action in current state with probability epsilon
    else:
        return action_tuples[max(range(ACTION_COUNT), key= lambda x : handle_unassigned_q_index(state, x))], 'Exploiting'
        # Explanation of this line:
        # max() function gives index of best action, based on its q-value
        # action_tuples[] returns the action from its index
        
# --- Update Rule
# Returns Q-value of action-state pair
def update_q_table(prev_state, action, reward, next_state, alpha, gamma) -> float:
    # find a that maximises value of Q in next_state
    max_future_q = max([handle_unassigned_q_action(next_state, action) for action in action_tuples])
    
    try:
        q[prev_state, action] += alpha * (reward + (gamma * max_future_q) - q[prev_state, action])
    except KeyError:
        q[prev_state, action] = alpha * (reward + (gamma * max_future_q))
    finally:
        return q[prev_state, action]

def get_q_table():
    return q