from PIL import Image
import pytesseract as pt

imagePath = './framedump_325.png'

# Pixel coordinates of required values printed to screen by gecko code in native resolution
crop_regions = [(89, 177, 133, 191), (98,251,159,264), (149,269, 160,284)]

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
# Greyscale image
frame = frame.convert('L')
# Crop into sections
cropped_images = crop_image(frame)