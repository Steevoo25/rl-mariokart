from Frame_Processor import process_frame
# A short script that gets frame data from every framedump in the dolphin framedumps folder
movieInfo = []

for i in range(90, 200):
        print(f'Frame: {i}\nData:{process_frame(i)}')#
