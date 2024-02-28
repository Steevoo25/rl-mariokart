# A script that opens a pickle file containing an array of controller states
# and feeds them one by one to dolphin, essentially replaying the episode
from dolphin import event, controller, gui
import pickle


PROJECT_DIR = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\'
date_and_time = '22-08--27_02_2024'

best_inputs_file = f"{PROJECT_DIR}Evaluation\\controller_episodes\\q-learning-{date_and_time}.pkl"

controller_inputs = pickle.load(open(best_inputs_file, "rb"))

for i in range(len(controller_inputs)):
    await event.frameadvance()
    controller.set_gc_buttons(0,controller_inputs[i])

gui.add_osd_message('End of episode')