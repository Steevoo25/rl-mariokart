# An agent that uses Q-Learning
import random
import pickle as pkl
PROJECT_DIR = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\'

# Action Space
from Rainbow.AdditionalScripts.action_space import generate_action_space

action_space = generate_action_space()
ACTION_COUNT = len(action_space) - 1 ## for indexing purposes

# Convert to tuple - to be used as key
action_tuples = []
for dicts in action_space:
    action_tuples.append(tuple(dicts.values()))

q_file = f'{PROJECT_DIR}RL\\q_table.pkl'  
def save_q():
    pkl.dump(q, open(q_file, "wb"))
# Reset q
#q = {}
#save_q()

print("Loading q table")
q = pkl.load(open(q_file, 'rb'))
print("table size:", len(q))

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

def optimistically_handle_unassigned_q_action(next_state, action):
    try:
        value = q[next_state, action]
    except KeyError:
        value = 50
    finally:
        return value

# --- Epsilon-Greedy Policy
def epsilon_greedy(state, eps):

    # If all actions have been explored, always move to it]
    # count all occurences of state in q
    explored_actions = sum(1 for key in q.keys() if key[0] == state)
    print("Explored actions:", explored_actions)

    if explored_actions >= ACTION_COUNT +1: 
        eps = 0.25 # high chance of choosing best
        print("Fully explored:", state, " count " , explored_actions)
    for action in action_tuples:
        value = handle_unassigned_q_action(state, action)
        print("Action:", action, ", Value:", value )

    best_action =  action_tuples[max(range(ACTION_COUNT + 1), key= lambda x : handle_unassigned_q_index(state, x))]     

    # Pick random action with probability epsilon
    if random.uniform(0,1) < eps or explored_actions == 0:
        random_action = action_tuples[random.randint(0, ACTION_COUNT)]
        return random_action, f"Exploring - RANDOM (Best:{best_action})"
    # Choose best action in current state with probability 1-epsilon
    else:

        return best_action, "Exploiting - BEST"
        # Explanation of this line:
        # max() function gives index of best action, based on its q-value
        # action_tuples[] returns the action from its index
        
# --- Update Rule
# Returns Q-value of action-state pair
def update_q_table(prev_state, action, reward, next_state, alpha, gamma) -> float:
    
    # pick an action via epsilon greedy-policy in next state
    #future_action = epsilon_greedy(next_state, eps)
    future_q = [(action, optimistically_handle_unassigned_q_action(next_state, action)) for action in action_tuples]
    max_future_q = max(future_q, key=lambda x: x[1])
    avg_future_q = sum([q[1] for q in future_q]) / sum(1 for q in future_q if not q == 0)
    ##check here
    #print("future", future_q)
    #print("max", max_future_q[1])
    print("avg future", avg_future_q)

    # Checks if current state exists, initialises if not
    try:
        a = q[prev_state, action]
    except KeyError:
        q[prev_state, action] = 0

    q[prev_state, action] += (1-alpha) * q[prev_state, action] + alpha * (reward + (gamma * avg_future_q) - q[prev_state, action])
    q[prev_state, action] = round(q[prev_state, action], 4)
    return q[prev_state, action]

# Recursively picks a random action in a given state and returns it
#def sum_future_rewards(state, gamma, prev_reward, eps) -> float:
    ## useful? think no lol


def get_q_table():
    return q