from Frame_Processor import process_frame

movieInfo = []

for i in range(46):
        print(f'Frame: {i}\nData:{process_frame(i)}')