from PIL import Image
import pytesseract as pt
# Possible Solution-
# Dict containing images of each character and corresponding value, essentially mapping font to value

#imagePath = './framedump_325_bitrate_250000.png'

imagePath = './framedump_302_bitrate_10000.png'

# Pixel coordinates of required values printed to screen by gecko code in native resolution
crop_regions = [(88, 177, 145, 191), (98,251,159,264), (149,269, 160,284)]

allowed_characters = ['1','2','3','4','5','6','7','8','9','0','.']
font_dict = {}
def load_dictionary():
    for i in range(len(allowed_characters)):
        imagePath = f'./characterDictionary/chars_{allowed_characters[i]}.png'
        print(imagePath)
        try:
            font_dict[allowed_characters[i]] = Image.open(imagePath).resize((11,15))
        except FileNotFoundError:
            print(f'File {imagePath} not found')
            
load_dictionary()
print(font_dict)
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
cropped_images = crop_image(frame)
# Extract text
#print('pyTesseract')
text = []
for i in range(3):
    text = pt.image_to_string(cropped_images[i], config='--psm 6 -c tessedit_char_whitelist=0123456789.')
    print(text)

# SYmbol matching
# Use high threshold so only exact matches are accepted
# define all characters 0-9 and .

