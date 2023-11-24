# A short script to test the functionality of text recognition in images
from PIL import Image
import pytesseract

#imagePath = './MkWGeckoCodes.png'
imagePath = '../framedump_325.png'
psm_level = 8
whitelist_characters = '0123456789.'
custom_config = f'--psm {psm_level} preserve_interword_spaces=1 textord_dotmatrix_gap=6 classify_bln_numeric_mode=1 rej_alphas_in_number_perm=1'# tessedit_char_whitelist={whitelist_characters}'
image1 = Image.open(imagePath)

# Greyscale Image
# Argument 'L' stands for Luminance
greyed_image = image1.convert('L')
greyed_image.save('./greyscaled_image.png')


text = pytesseract.image_to_string(greyed_image, config=custom_config)

greyed_image.close()

print(f'Image 1: {text}')