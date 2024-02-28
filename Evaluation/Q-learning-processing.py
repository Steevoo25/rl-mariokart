import pandas as pd
from matplotlib import pyplot as plt

path = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\Evaluation\\q-learning-22-08--27_02_2024.csv'
# Read into dataframe
df = pd.read_csv(path)
# Remove 1st episode (idk why -100 reward)
df = df[1:]

# Smooth the data
smoothing_window = 10
smoothed_reward = pd.Series(df['Total_Reward']).rolling(window=smoothing_window, min_periods=1, center=True).mean()

# Plotting
#plt.plot(df['Episode'], df['Total_Reward'], label='Return', linewidth=0.1)
plt.plot(df['Episode'], smoothed_reward, label='Return', linewidth=0.3)
#plt.plot(df['Episode'], df['Frame_Count'], label='Survival Time')

# Set x axis scale
plt.ylim(0, 500)

# Lables
plt.xlabel('Episode number')
plt.ylabel('Return')
plt.title('Line Graph')

plt.legend()

plt.show()