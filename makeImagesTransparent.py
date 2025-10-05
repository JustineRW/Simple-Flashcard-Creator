from PIL import Image 
import pathlib
import pandas as pd

df = pd.read_csv('database.csv')

for index, row in df.iterrows():
    fileNameIncludingTransparent = "images/back/" + "transparent " + str.split(row['imageBack'],".")[0] + ".png"
    if not pathlib.Path(fileNameIncludingTransparent).is_file():        
        backImage = Image.open(pathlib.Path("images/back/" + row['imageBack'] )) 
        backImage = backImage.convert("RGBA")
        backImage.putalpha(63)  # quarter alpha; alpha argument must be an int
        backImage.save(pathlib.Path(fileNameIncludingTransparent))
