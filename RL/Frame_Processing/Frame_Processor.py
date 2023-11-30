from PIL import Image
import pytesseract as pt

path_to_framedumps = 'C:/Users/steve/OneDrive/Documents/Dolphin Emulator/Dump/Frames/framedump_'
tesseract_config = '--psm 6 -c tessedit_char_whitelist=0123456789'

# Pixel coordinates of required values printed to screen by gecko code in 2xnative resolution
# Left, Upper, Right, Lower
crop_regions = [(176, 354, 248, 384), (185, 500, 286, 531), (290, 537, 312, 567)]

# Splits screenshot into seperate images:
# [0] = XZ Velocity
# [1] = Race%
# [2] = MT

def crop_image(image: Image):
# Inititalise empty array
    cropped_images = []
    for i,region in enumerate(crop_regions):
        cropped_images.append(image.crop(region))
        cropped_images[i].save(f'{i}.png')
    return cropped_images 

def format_velocity(vel:str):
    # from 0.00 to 999.99
    # as there is no decimal point, convert it to a float and divide by 100
    if vel.isnumeric():
        return float(vel)/100
    # TODO: Add error checking

def format_completion(completion:str):
    # from 1.00000 to 4.00000
    if completion.isnumeric():
        return float(completion) / 100000
    # TODO: Add error checking

def format_mt(mt:str):
    # from 0 to 270
    if mt.isnumeric():
        return int(mt)
    # TODO: Add error checking

def process_frame(frame_index: int):
    # Append index to file name
    imagePath = path_to_framedumps + str(frame_index) + '.png'
    imagePath = './framedump_178.png'
    print(f'read frame {frame_index}')
    raceInfo = []
    # Open image
    frame = Image.open(imagePath)

    # Convert image to black and white
    frame = frame.convert('L')

    # Crop into sections
    cropped_images = crop_image(frame)

    # For each cropped image
    for i, cropped_image in enumerate(cropped_images):
        # Us
        text = pt.image_to_string(cropped_image, config=tesseract_config)
        raceInfo.append(text.strip())
    
    raceInfo[0] = format_velocity(raceInfo[0])
    raceInfo[1] = format_completion(raceInfo[1])
    raceInfo[2] = format_mt(raceInfo[2])
    return raceInfo

print(process_frame(0))

