# -- DOLHPIN IMPORTS --
#from dolphin import savestate # for loading savestates
#from dolphin import event # for resetting emulation
#from dolphin import gui # for status messages

# -- OTHER IMPORTS --
from sys import path


# Current issue with dolphin causing a deadlock when loading savestetes from scripts
# https:\\github.com/TASLabz/dolphin/issues/123

def init():
# Running dolphin in command line causes some issues, 
# so I will have to open dolphin and run the script through the gui,
# making sure to use the correct config
    
    venv_dir ='Z:\\project\\hjs115\\venv\\Lib\\site-packages'
    path.append(venv_dir)
    # Adds my venv directory to the path of pytohn used by dolphin
    path.append('Z:\\project\\hjs115')

    # 3.) Load Savestate

    # 4.) Pause Emulation
    return



def step():
    # Read Frame
    # Calculate rewards
    # update q network
    # identify input with highest estimated reward
    # update controller
    # advance frame?
    return 
# Assumes dolphin is already open
def reset():
    # Load Default savestate
    # Reset Controller
    # wipe framedumps folder
    return

init()