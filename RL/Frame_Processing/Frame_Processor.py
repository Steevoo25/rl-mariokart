from PIL import Image
import pytesseract as pt
import cv2

# Resolution: Native 640x528, bitrate:10,000, png compression: 6
#imagePath = 'framedump_228.png'
# Resolution: 2x Native - 720p, bitrate:10,000, png compression: 6
imagePath = 'framedump_178.png'

# Left, Upper, Right, Lower
# Pixel coordinates of required values printed to screen by gecko code in native resolution
#crop_regions = [(88, 177, 150, 191), (98,251,159,264), (149,269, 160,284)]

# Pixel coordinates of required values printed to screen by gecko code in 2xnative resolution
crop_regions = [(176, 354, 248, 384), (185, 500, 286, 531), (290, 537, 312, 567)]

# Splits screenshot into seperate images:
# [0] = XZ Velocity
# [1] = Race%
# [2] = MT

def crop_image(image):
# Inititalise empty array
    cropped_images = []
    for i,region in enumerate(crop_regions):
        cropped_images.append(image.crop(region))
        cropped_images[i].save(f'{i}.png')
    return cropped_images

# Open image
frame = Image.open(imagePath)
# Convert image to black and white
# Loop to check any BW threshold is effective

frame = frame.convert('L')
# Crop into sections
cropped_images = crop_image(frame)
# Extract text
#print('pyTesseract')
#print(pt.image_to_string(frame, config='-c tessedit_char_whitelist=0123456789.'))

for i in range(3):
    print(i)
    text = pt.image_to_string(cropped_images[i], config='--psm 6 -c tessedit_char_whitelist=0123456789.')
    print(text)
