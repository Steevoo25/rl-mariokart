from time import sleep
from dolphin import savestate, event

path = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\savestates\\start.sav'

def load_using_api():
    message = f"Loading savestate using dolphin api from: {path}"
    print(message)
    # sleep for 1 second to avoid deadlock
    sleep(1)
    savestate.load_from_file(path)
    sleep(1)

event.on_frameadvance(load_using_api())