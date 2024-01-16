## Dolphin has an issue where trying to load a savestate not created using the API through the API causes a crash.
# In short, to load a savestate using the API, I first need to save a state using the API

from dolphin import savestate

path = 'C:\\Users\\steve\\OneDrive\\Documents\\3rd Year\\Project\\my-project\\savestates\\start.sav'
savestate.save_to_file(path)
print(f"Saved current state to {path}")
