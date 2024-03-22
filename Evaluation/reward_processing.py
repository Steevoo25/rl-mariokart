import pandas as pd
from matplotlib import pyplot as plt

DEMO_FILE = 'q-learning-05_03_2024--16-00.csv'
filepath = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\Evaluation\\data\\q-learning\\rewards\\'
filename = 'q-learning-05_03_2024--13-23.csv'

rewards = pd.read_csv(f'{filepath}{filename}')
column_names = ["total_reward","vel_reward","perc_reward","mt_reward"]
#print(rewards)

x_axis = rewards.index.tolist()

for column in column_names:
    plt.plot(x_axis,rewards[column] , label=column)
    
# Set y axis scale
plt.ylim(0, 4000)

plt.legend()
plt.show()