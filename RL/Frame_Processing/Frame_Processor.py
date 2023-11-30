from PIL import Image
import pytesseract as pt
import re

path_to_framedumps = 'C:/Users/steve/OneDrive/Documents/Dolphin Emulator/Dump/Frames/framedump_'

# Pixel coordinates of required values printed to screen by gecko code in 2xnative resolution
# Left, Upper, Right, Lower
crop_regions = [(176, 354, 248, 384), (185, 500, 286, 531), (290, 537, 312, 567)]

completion_pattern = re.compile(r'^\d\.\d{5}$')
mt_pattern = re.compile(r'^(?:\d{1,2}|1\d{2}|2[0-6]\d|27[0-0])$')

# Splits screenshot into seperate images:
# [0] = XZ Velocity
# [1] = Race%
# [2] = MT

def crop_image(image: Image):
# Inititalise empty array
    cropped_images = []
    for i,region in enumerate(crop_regions):
        cropped_images.append(image.crop(region))
        #cropped_images[i].save(f'{i}.png')
    return cropped_images
    
def format_velocity(vel:str):
    # from 0.00 to 999.99
    # if there is no decimal point, convert it to a float and divide by 100
    if vel.isnumeric():
        vel = float(vel)/100
    return vel

print(format_velocity('3740'))
def format_completion(completion:str):
    return 1
def format_mt(mt:str):
    return 1

def process_frame(frame_index: int):
    # Append index to file name
    imagePath = path_to_framedumps + frame_index
    print(f'read frame {frame_index}')
    # Initialise empty array for storing race values
    raceInfo = []
    # Open image
    frame = Image.open(imagePath)

    # Convert image to black and white
    frame = frame.convert('L')

    # Crop into sections
    cropped_images = crop_image(frame)

    # Extract text from images
    for i in range(3):
        text = pt.image_to_string(cropped_images[i], config='--psm 6 -c tessedit_char_whitelist=0123456789')
        raceInfo[i] = text
    
    return raceInfo
