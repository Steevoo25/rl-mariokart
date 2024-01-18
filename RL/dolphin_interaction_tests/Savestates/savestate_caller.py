from load_savestate_naiive import load_using_fkey

from dolphin import event

event.on_frameadvance(load_using_fkey)