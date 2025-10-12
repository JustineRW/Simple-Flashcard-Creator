from PIL import Image 
import pathlib
import pandas as pd

df = pd.read_csv('database.csv')
filePath = "images/back/"

def make_images_transparent(filePath, imageName, alpha : int):
    backImage = Image.open(pathlib.Path(filePath + imageName)) 
    backImage = backImage.convert("RGBA")
    backImage.putalpha(alpha)  
    backImage.save(pathlib.Path(filePath + imageName))

for index, row in df.iterrows():
    make_images_transparent(filePath, row['imageBack'], 63) # quarter alpha (255 is no transparency)
