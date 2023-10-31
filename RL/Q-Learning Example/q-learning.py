import gym
import random

env = gym.make('Taxi-v3')
# Initialise values
# Learning rate
alpha = 0.4
# Discount Factor
gamma = 0.999
# Greedy Probability decider thing idk 
epsilon = 0.017

# Initialise Q Table

q = {}
# Q Table = dictionary storing state action pair, and its Q-Value
for s in range(env.observation_space.n):
    for a in range (env.action_space.n):
        q[(s,a)] = 0.0

# Update Q table based on action taken
def update_q_table(prev_state, action, reward, next_state, alpha, gamma):
    qa = max([q[(next_state, a)] for a in range(env.action_space.n)])
    q[(prev_state[0], action)] += alpha * (reward + gamma * qa - q[(prev_state[0], action)])

# Policy to decide which action to take, 
def epsilon_greedy_policy(state, epsilon): 
    if random.uniform(0,1) < epsilon:
        # Explore a new action, P(new action) = 1-epsilon
        return env.action_space.sample()
        
    else:
        # Select the best action, P(best action) = epsilon
        return max(list(range(env.action_space.n)), key = lambda x: q[((state[0], x))])
        
# For each episode
for i in range(8000):
    r=0
    prev_state = env.reset()
    
    while (True): 
        print(prev_state)
        #In each state we select action by epsilon greedy policy 
        action = epsilon_greedy_policy(prev_state, epsilon) 
        #then we take the selected action and move to the next state
        nextstate, reward, done, _,_ = env.step(action) 
        #and we update the q value using the update_q_table() function #which updates q table according to our update rule. 
        update_q_table(prev_state, action, reward, nextstate, alpha, gamma)
        #then we update the previous state as next state
        prev_state = nextstate 
        #and store the rewards in r
        r+=reward
        if done:
            break
    print('Total reward: ', r)
    
env.close()


