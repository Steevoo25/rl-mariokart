# A script that opens a pickle file containing an array of controller states
# and feeds them one by one to dolphin, essentially replaying the episode
from dolphin import event, controller, gui
import pickle


PROJECT_DIR = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\'
filename = 'q-learning-11-11--29_02_2024'

best_inputs_file = f"{PROJECT_DIR}Evaluation\\controller_episodes\\{filename}.pkl"
# Load pickle file
controller_inputs = pickle.load(open(best_inputs_file, "rb"))
# Loop through file
for i in range(len(controller_inputs)):
    await event.frameadvance() # wait for dolphin
    controller.set_gc_buttons(0,controller_inputs[i]) # set controller

##TODO: Pause emulation
gui.add_osd_message('End of episode')
