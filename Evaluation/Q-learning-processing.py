import pandas as pd
from matplotlib import pyplot as plt
filename = 'q-learning-07_03_2024--19-20'
path = f'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\Evaluation\\data\\q-learning\\episodes\\{filename}.csv'
# Read into dataframe
df = pd.read_csv(path, )
# Remove episodes 1 and 3 (idk why -100 reward)

df = df[1:]

# Smooth the data
smoothing_window = len(df) // 10

smoothed_reward = pd.Series(df['Total_Reward']).rolling(window=smoothing_window, min_periods=1, center=True).mean()

# Plotting
#plt.plot(df['Episode'], df['Total_Reward'], label='Return', linewidth=0.1)
plt.plot(df['Episode'], smoothed_reward, label='Return', linewidth=1)
#plt.plot(df['Episode'], df['Frame_Count'], label='Survival Time')

# Set x axis scale
plt.ylim(200, 1000)

# Lables
plt.xlabel('Episode number')
plt.ylabel('Return')
plt.title(f'Return from each episode after {len(df)} Episodes')

plt.legend()

# Edit filepath to save png
path = path.replace("csv", "png")
path = path.replace("data", "plots")

#plt.savefig(path)

plt.show()
