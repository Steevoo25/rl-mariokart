from PIL import Image

allowed_characters = ['1','2','3','4','5','6','7','8','9','0','.']

def load_dictionary():
    for i in range(len(allowed_characters)):
        imagePath = f'./characterDictionary/char_{allowed_characters[i]}.png'
        print(imagePath)
        try:
            image = Image.open(imagePath).resize((11,15)).convert('L')
            image.save(imagePath)
        except FileNotFoundError:
            print(f'File {imagePath} not found')