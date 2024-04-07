# RL in Mariokart Wii

This project contains code for training a Q-learning Agent

## Requirements
- A Mariokart Wii ISO, obtained through the steps outlined [here](https://dolphin-emu.org/docs/guides/ripping-games/) (requiring a copy of the game disk (NTSC-U version), a Wii console with [homebrew](https://www.wiibrew.org/wiki/Homebrew_setup), an SD card and a PC/laptop)
- [TASLabz Dolphin build](https://github.com/TASLabz/dolphin)
- Python 3.8
## Setup
### Code
1. Create a venv using `requirements.txt` from the project root directory
2. In `dolphin_env_v2.py` change _PROJECT_DIR_ to the path to the project directory
3. In `dolphin_env_v2.py` change _venv_dir_ to the path to the venv made in 1.
4. Copy _PROJECT_DIR_ from `dolphin_env_v2.py` into `q_learning_agent.py`
### Dolphin
Following Dolphin's [Build instructions](https://github.com/dolphin-emu/dolphin) build the TASLabz fork with scripting support
#### Add Script to Dolphin Scripting Directory
Open Dolphin and go to __View__ at the top of the screen and make sure Scripting is checked. This will give a panel on the left hand side of the screen. Click the '+' button in that panel and select `dolphin_env_v2.py` in the dialogue. This will add `dolphin_env_v2.py` to the Script directory. Repeat this process for `q_learning_agent.py`
#### Create Savestate Slot
1. Open Dolphin, click on __Open__, then navigate to the ISO file to run the game (this will open in another window)
2. Once the game is open, pause the emulation by pressing 'P'
3. Then in Dolphin's main window go to __Emulation>Load State>From File__ and select `start.sav` in `<project directory>\savestates\` . This will load you into the initial state.
4. Load this state into slot 8 by going to __Emulation>Save State>Save State to Slot>Save to Slot 8__
#### Configure Log
1. Go to __View>Show Log Configuration__ and set verbosity to _Info_, then disable all log types apart from _Scripting (Scripting)_
2. Go to __View>Show Log__

## Usage
### Using a Trained Agent
In <project directory>\RL you will find 3 pickle files, each containing the Q-table for the trained agents. If you want to use one of these, change _q_file_ in `q_learning_agent.py` to its path.
### Using an Untrained Agent
To start training your own agent, simply change _q_file_ to a suitable file name and if it doesn't exist then it will initialize an empty Q-table.

Once this is done, open the game in Dolphin and once it loads tick the box next to `dolphin_env_v2.py`. This will run the script and start the agent