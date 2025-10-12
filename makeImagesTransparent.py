from PIL import Image 
import pathlib
import pandas as pd

df = pd.read_csv('database.csv')
filePath = "images/back/"

def make_images_transparent(filePath, imageName):
    resultFileName = filePath + "transparent " + str.split(imageName,".")[0] + ".png"
    if not pathlib.Path(resultFileName).is_file():        
        backImage = Image.open(pathlib.Path(filePath + imageName)) 
        backImage = backImage.convert("RGBA")
        backImage.putalpha(63)  # quarter alpha; alpha argument must be an int
        backImage.save(pathlib.Path(resultFileName))

for index, row in df.iterrows():
    make_images_transparent(filePath, row['imageBack'])
