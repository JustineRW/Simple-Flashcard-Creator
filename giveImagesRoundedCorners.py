from PIL import Image 
import pathlib
import pandas as pd

df = pd.read_csv('database.csv')
filepathBack = "images/back/"
filepathFront = "images/front/"
filepathOriginalImages = "images/originals/"
cornerMaskFilepath = "images/originals/cornermask.png"

def give_image_rounded_corners(filepath, filepathOriginal, cornerMaskFilepath, imageName):
    filename = filepathOriginal + imageName
    image = Image.open(pathlib.Path(filename)) 
    cornerMask = Image.open(pathlib.Path(cornerMaskFilepath))

    backImage_width, backImage_height = image.size
    cornerMask = cornerMask.resize((backImage_width,backImage_height))

    image.paste(cornerMask, (0,0), mask=cornerMask)
    image.save(pathlib.Path(filepath + imageName))

for index, row in df.iterrows():
    give_image_rounded_corners(filepathBack, filepathOriginalImages, cornerMaskFilepath, row['imageBack'])
    give_image_rounded_corners(filepathFront, filepathOriginalImages, cornerMaskFilepath, row['imageFront'])
