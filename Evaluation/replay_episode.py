# A script that opens a pickle file containing an array of controller states
# and feeds them one by one to dolphin, essentially replaying the episode
from dolphin import event, controller, gui
import pickle

TIME_STEP = 20
PROJECT_DIR = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\'
filename = 'q-learning-06_03_2024--13-55'

# A helper function to convert a tuple of actions (used in the q-learning process) to a dictionary (to send to emulator)
def convert_actions_to_dict(action: tuple):
    return {"A": True, "B": action[0],"Up": action[1],"StickX": action[2]}

best_inputs_file = f"{PROJECT_DIR}Evaluation\\data\\q-learning\\controller_episodes\\{filename}.pkl"
# Load pickle file
controller_inputs = pickle.load(open(best_inputs_file, "rb"))
# Loop through file
counter = 0

for i in range(len(controller_inputs) * TIME_STEP) :
    await event.frameadvance() # wait for dolphin
    if i % TIME_STEP == 0 : 
        action = convert_actions_to_dict(controller_inputs[counter])
        counter +=1
    controller.set_gc_buttons(0,action) # set controller
    

##TODO: Pause emulation
gui.add_osd_message('End of episode')
