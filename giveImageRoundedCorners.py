from PIL import Image, ImageDraw
import pandas as pd

def make_image_transparent_with_rounded_corners(image, radius, size, washedOutAlpha):
    circle = Image.new('L', (radius * 2, radius * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=washedOutAlpha)

    alpha = Image.new('L', size, washedOutAlpha)
    w, h = size
    alpha.paste(circle.crop((0, 0, radius, radius)), (0, 0))
    alpha.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
    alpha.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
    alpha.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    image.putalpha(alpha)
    return image

# def make_corner_mask(radius, size):
#     circle = Image.new('L', (radius * 2, radius * 2), 0)
#     draw = ImageDraw.Draw(circle)
#     draw.ellipse((0, 0, radius * 2 - 1, radius * 2 - 1), fill=64)

#     cornerMask = Image.new('L', size, 64)
#     background = Image.new('L', size, 64)

#     w, h = size    
#     cornerMask.paste(circle.crop((0, 0, radius, radius)), (0, 0))
#     cornerMask.paste(circle.crop((0, radius, radius, radius * 2)), (0, h - radius))
#     cornerMask.paste(circle.crop((radius, 0, radius * 2, radius)), (w - radius, 0))
#     cornerMask.paste(circle.crop((radius, radius, radius * 2, radius * 2)), (w - radius, h - radius))
    
#     background.putalpha(cornerMask)
#     background.save("images/back/cornermask.png")


df = pd.read_csv('database.csv')

for index, row in df.iterrows():
    filePathToFetch = "images/originals/"
    filePathToSave = "images/back/"
    backImage = Image.open(filePathToFetch + row['imageBack']).convert("RGBA")
    fileNamePNG = filePathToSave + str.split(row['imageBack'],".")[0] + ".png"

    imageSize = backImage.width, backImage.height
    cornerRadius = int(backImage.width / 6)
    backImage = make_image_transparent_with_rounded_corners(backImage, cornerRadius, imageSize, 63) # quarter Alpha
    backImage.save(fileNamePNG, quality=90)
    # make_corner_mask(cornerRadius,imageSize)


