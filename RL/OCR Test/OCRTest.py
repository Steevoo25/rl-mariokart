# A short script to test the functionality of text recognition in images
from PIL import Image
import pytesseract

#imagePath = './MkWGeckoCodes.png'
imagePath = './geckoCropped2.png'
psm_level = 8
whitelist_characters = '0123456789.'
custom_config = f'--psm {psm_level} preserve_interword_spaces=1 textord_dotmatrix_gap=6 classify_bln_numeric_mode=1 rej_alphas_in_number_perm=1'# tessedit_char_whitelist={whitelist_characters}'

image1 = Image.open(imagePath)
text = pytesseract.image_to_string(image1, config=custom_config)

image1.close()

print(f'Image 1: {text}with config: {custom_config}')