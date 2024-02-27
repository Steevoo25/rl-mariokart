import pandas as pd
from matplotlib import pyplot as plt

path = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\Evaluation\\data\\q-learning-17-15--27_02_2024.csv'
# Read into dataframe
df = pd.read_csv(path)
# Remove 1st episode (idk why -100 reward)
df = df[1:]

# Plotting
plt.plot(df['Episode'], df['Total_Reward'], label='Return')
plt.plot(df['Episode'], df['Frame_Count'], label='Survival Time')

plt.xlabel('Episode number')
plt.ylabel('Return/Survival Time')
plt.title('Line Graph')

plt.legend()

plt.show()

