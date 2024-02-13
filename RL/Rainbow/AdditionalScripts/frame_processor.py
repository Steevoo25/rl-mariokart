from PIL import Image, ImageOps
import pytesseract as pt
import os
import numpy as np

#TODO : Path will be different for different systems, get default path from dolphin
# For my laptop
path_to_framedumps = 'C:/Users/steve/OneDrive/Documents/Dolphin Emulator/Dump/Frames/framedump_'
# For my PC
#path_to_framedumps = 'Z:/Users/Harry Stevenson/Documents/OneDrive - University of Birmingham/Documents/Dolphin Emulator/Dump/Frames/framedump_'
tesseract_config = '--psm 6 -c tessedit_char_whitelist=0123456789'

# Pixel coordinates of required values printed to screen by gecko code in 2xnative resolution
# Left, Upper, Right, Lower
crop_regions = [(176, 354, 248, 384), (185, 500, 286, 531), (290, 537, 312, 567)]

# Splits screenshot into seperate images:
# [0] = XZ Velocity
# [1] = Race%
# [2] = MT

def process_image(image: Image):
# Inititalise empty array
    cropped_images = []
    for i,region in enumerate(crop_regions):
        # This line crops the frame
        # then converts to true BW using the lambda
        # and appends to list
        cropped_images.append(image.crop(region).point(lambda x: 0 if x > 200 else 255))
        # Save cropped and processed images locally
        #cropped_images[i].save(f'{i}.png')
    return cropped_images 
    
# Wrapper function for value formatting
def format_race_info(index:int, info:str):
    if index == 0:
        return format_velocity(info)
    elif index == 1:
        return format_completion(info)
    elif index == 2:
        return format_mt(info)
    else:
        raise IndexError("Race Info index out of range")

def format_velocity(vel:str):
    # from 0.00 to 999.99
    # as there is no decimal point, convert it to a float and divide by 100
    vel = float(vel)/100
    if vel > 120:
        raise ValueError(f"Error in Speed value :{vel}")
    else:
        return vel

def format_completion(completion:str):
    # from 1.00000 to 4.00000
    if completion.isnumeric():
        return float(completion) / 100000
    else:
        raise ValueError(f"Error in race% value: {completion}")

def format_mt(mt:str):
    # from 0 to 270
    if mt.isnumeric():
        return int(mt)
    else:
        raise ValueError(f"Error in miniturbo value: {mt}")

def process_frame(frame_index: int):
    # Append index to file name
    imagePath = path_to_framedumps + str(frame_index) + '.png'
    # imagePath = './framedump_178.png'
    raceInfo = []
    # Open image
    try:
        frame = Image.open(imagePath)
    except FileNotFoundError:
        print(f'Could not find file {imagePath}')
        return
    
    # Crop into sections and BW
    cropped_images = process_image(frame)
    
    # For each cropped image
    for i, cropped_image in enumerate(cropped_images):
        # Use tesseract to extract strings from each cropped image
        text = pt.image_to_string(cropped_image, config=tesseract_config).strip()
        # add the formatted info to the array
        try:
            raceInfo.append(format_race_info(i,text))
        except ValueError:
            print(f"Error in frame {i}")
    # Delete image after extracting data so no warning popup for next episode
    #os.remove(imagePath)
    return raceInfo
    
# A function that returns the downsampled and grayscaled pixel data of a given framedump by index
def dump_pixel_data(frame_index: int) :
    # Append frame index to framedumps path
    imagePath = path_to_framedumps + str(frame_index) + '.png'
    # Open Image    
    try:
        frame = Image.open(imagePath)
    except FileNotFoundError:
        print(f'Could not find file {imagePath}')
        return []

    # -- Downsample Image --
    DOWNSAMPLE_FACTOR = 4
    width, height = frame.size
    downsampled_width = width // DOWNSAMPLE_FACTOR
    downsampled_height = height // DOWNSAMPLE_FACTOR
    frame = frame.resize((downsampled_width, downsampled_height))
    # -- Greyscale Image --
    frame = frame.convert("L")
    # -- Get Raw Data --
    frame_data = np.array(frame.getdata())
    return frame_data