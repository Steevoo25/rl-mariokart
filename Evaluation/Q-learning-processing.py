import pandas as pd
from matplotlib import pyplot as plt
#filename = input("filename:")
#laptop
#path = f'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\Evaluation\\data\\q-learning\\episodes\\{filename}.csv'
#pc
full_session_files = ['Agent_A_5kEps','Agent_B_5kEps','Agent_C_5kEps']

# Smooth the data

for filename in full_session_files:
    path = f'C:\\project\\hjs115\Evaluation\\data\\episodes\\{filename}.csv'
    # Read into dataframe
    df = pd.read_csv(path)
    smoothing_window = len(df) // 10
    smoothed_reward = pd.Series(df['Total_Reward']).rolling(window=smoothing_window, min_periods=5, center=True).mean()
    # Plotting
    plt.plot(df['Episode'], smoothed_reward, label=filename[:7], linewidth=1)

# Set x axis scale
plt.ylim(0, 400)
# Add 1-lap line
plt.axhline(y=220, color='gray', linestyle='--', label='Lap 1 Complete')
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
