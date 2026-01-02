from PIL import Image 
import pathlib
import pandas as pd

def give_image_rounded_corners(filepath, filepathOriginal, cornerMaskFilepath, imageName):

    filename = filepathOriginal + imageName
    image = Image.open(pathlib.Path(filename)) 
    corner_mask = Image.open(pathlib.Path(cornerMaskFilepath))

    image_width, image_height = image.size
    corner_mask = corner_mask.resize((image_width,image_height))

    image.paste(corner_mask, (0,0), mask=corner_mask)
    image.save(pathlib.Path(filepath + imageName))

def make_images_transparent(filePath, imageName, alpha : int):

    backImage = Image.open(pathlib.Path(filePath + imageName)) 
    backImage = backImage.convert("RGBA")
    backImage.putalpha(alpha)  

    if imageName.split('.')[1] != 'png':
        imageName = imageName.split('.')[0] + ".png"
    backImage.save(pathlib.Path(filePath + imageName))


if __name__ == "main":
    df = pd.read_csv('database.csv')
    filePath = "images/back/"
    for index, row in df.iterrows():
        make_images_transparent(filePath, row['imageBack'], 63) # quarter alpha (255 is no transparency)