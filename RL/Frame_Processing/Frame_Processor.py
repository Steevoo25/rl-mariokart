from PIL import Image
import pytesseract as pt
import cv2

#cv2 template matching
# load images in bw
#cv2.imread(path, 0)

#imagePath = './framedump_325_bitrate_25000.png'
imagePath = './framedump_23_cropped.png'

#imagePath = './framedump_302_bitrate_10000.png'

# Pixel coordinates of required values printed to screen by gecko code in native resolution
crop_regions = [(88, 177, 150, 191), (98,251,159,264), (149,269, 160,284)]

# Splits screenshot into seperate images:
# [0] = XZ Velocity
# [1] = Race%
# [2] = MT
def crop_image(image):
# Inititalise empty array
    cropped_images = []
    for i in range(len(crop_regions)):
        cropped_images.append(image.crop(crop_regions[i]))
        cropped_images[i].save(f'{i}.png')
    return cropped_images

# Open image
frame = Image.open(imagePath)
# Convert image to black and white
# Loop to check any BW threshold is effective

frame = frame.convert('L')
# Crop into sections
#cropped_images = crop_image(frame)
# Extract text
#print('pyTesseract')
print(pt.image_to_data(frame, config='--psm 6 -c tessedit_char_whitelist=0123456789.'))

# for i in range(3):
#     print(i)
#     text = pt.image_to_string(cropped_images[i], config='--psm 6 -c tessedit_char_whitelist=0123456789.')
#     print(text)
