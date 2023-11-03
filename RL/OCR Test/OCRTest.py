from PIL import Image
import pytesseract

# Open the image file
image = Image.open('./MkWGeckoCodes.jpg')

# Use pytesseract to do OCR on the image
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)