# A short script to test the functionality of text recognition in images
from PIL import Image
import pytesseract

# Pixel coordinates of xz velocity value printed to screen by gecko code in native resolution
XZ_Velocity_Region = (89, 177, 133, 191)

def crop_image(image):
    regions = image.crop(XZ_Velocity_Region)
    return regions

#imagePath = './MkWGeckoCodes.png'
imagePath = './framedump_325.png'
psm_level = 8
whitelist_characters = '0123456789.'
custom_config = f'--psm {psm_level} preserve_interword_spaces=1 textord_dotmatrix_gap=6 classify_bln_numeric_mode=1 rej_alphas_in_number_perm=1'# tessedit_char_whitelist={whitelist_characters}'
image1 = Image.open(imagePath)

# Crop Image
cropped_image = crop_image(image=image1)
cropped_image.save('./cropped_image.png')
# Greyscale Image
# Argument 'L' stands for Luminance
greyed_image = cropped_image.convert('L')
greyed_image.save('./greyscaled_image.png')


text = pytesseract.image_to_string(greyed_image, config=custom_config)

greyed_image.close()

print(f'Image 1: {text}')