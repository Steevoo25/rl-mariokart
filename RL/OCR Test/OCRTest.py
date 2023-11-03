# A short script to test the functionality of text recognition in images
from PIL import Image
import pytesseract

image1 = Image.open('./geckoCropped1.png')
image2 = Image.open('./geckoCropped2.png')

whitelist_characters = '0123456789.'

custom_config = f'tessedit_char_whitelist={whitelist_characters}'


text = pytesseract.image_to_string(image1, config=custom_config)
text2 = pytesseract.image_to_string(image2, config=custom_config)

# Print the extracted text
print(f'Image 1:{text}')
print(f'Image 2:{text2}')