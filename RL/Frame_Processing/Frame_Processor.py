from PIL import Image
import pytesseract as pt

#imagePath = './framedump_325_bitrate_250000.png'

imagePath = './framedump_302_bitrate_10000.png'

# Pixel coordinates of required values printed to screen by gecko code in native resolution
crop_regions = [(89, 177, 133, 191), (98,251,159,264), (149,269, 160,284)]
target_text = ['17.22', '1.01914','0' ]
# Splits screenshot into seperate images:
# [0] = XZ Velocity
# [1] = Race%
# [2] = MT
def crop_image(image):
# Inititalise empty array
    cropped_images = []
    for i in range(len(crop_regions)):
        cropped_images.append(image.crop(crop_regions[i]))
        #cropped_images[i].save(f'{i}.png')
    return cropped_images
    
# Open image
frame = Image.open(imagePath)
# Convert image to black and white
# Loop to check any BW threshold is effective
threshold = 80
while threshold < 120:
    frame = frame.convert('L').point(lambda x: 0 if x < threshold else 255, '1')
    # Crop into sections
    cropped_images = crop_image(frame)
    # Extract text
    #print('pyTesseract')
    text = []
    for i in range(3):
        text.append(pt.image_to_string(cropped_images[i], config='--psm 6 -c tessedit_char_whitelist=0123456789.'))
        #print(f'{i}:{text[i]}')
        if text[i] == target_text[i]:
            print(f'Image{i} with threshold {threshold}')
    threshold=threshold+1

# SYmbol matching
# Use high threshold so only exact matches are accepted
# define all characters 0-9 and .
# 
