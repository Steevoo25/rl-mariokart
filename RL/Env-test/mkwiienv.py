import gym # Make sure correct interpreter is used
import mario_env

env_id = "MarioEnv-v0"

try:
    env = gym.make(env_id)
    env.reset()
except Exception as e:
    print(f"Error creating Environmnent {e}")