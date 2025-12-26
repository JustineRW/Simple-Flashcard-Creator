from PIL import Image 
import pathlib

def give_image_rounded_corners(filepath, filepathOriginal, cornerMaskFilepath, imageName):

    filename = filepathOriginal + imageName
    image = Image.open(pathlib.Path(filename)) 
    cornerMask = Image.open(pathlib.Path(cornerMaskFilepath))

    backImage_width, backImage_height = image.size
    cornerMask = cornerMask.resize((backImage_width,backImage_height))

    image.paste(cornerMask, (0,0), mask=cornerMask)
    image.save(pathlib.Path(filepath + imageName))


