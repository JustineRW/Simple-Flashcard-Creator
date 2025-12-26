from borb.pdf import (
    Document,
    Page,
    PageLayout,
    PDF,
    HeterogeneousParagraph,
    Paragraph,
    Chunk,
    TrueTypeFont,
    Font,
    SingleColumnLayout

)
import pandas as pd

from giveImagesRoundedCorners import give_image_rounded_corners
from flashcardCreator import createFlashcards
from makeImagesTransparent import make_images_transparent
from transformPdfIntoPagesPerPage import transformPdfIntoMultiplePages

font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-VariableFont_opsz,wght.ttf")
italicFont: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-Italic-VariableFont_opsz,wght.ttf")

df = pd.read_csv('database.csv')
filepathBack = "images/back/"
filepathFront = "images/front/"
filepathOriginalImages = "images/originals/"
cornerMaskFilepath = "images/originals/cornermask.png"
outputFileName = "flashcards"
pagesPerPage = 3

pageWidth = 842 #A4 width
pageHeight = 595 #A4 height

for index, row in df.iterrows():
    give_image_rounded_corners(filepathBack, filepathOriginalImages, cornerMaskFilepath, row['imageBack'])
    give_image_rounded_corners(filepathFront, filepathOriginalImages, cornerMaskFilepath, row['imageFront'])
    make_images_transparent(filepathBack, row['imageBack'], 75) # approx quarter alpha (255 is no transparency at all, 0 is fully transparent)

fullOutputFilePath : str = createFlashcards(df, font, italicFont, pageWidth, pageHeight, outputFileName)
transformPdfIntoMultiplePages(pagesPerPage, fullOutputFilePath)
# addReferencePage(font, italicFont)