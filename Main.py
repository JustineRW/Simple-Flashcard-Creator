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

from reference_page import add_reference_pages
from image_manipulation import give_image_rounded_corners
from flashcard_creator import create_flashcards
from image_manipulation import make_images_transparent
from pdf_transformer import transform_pdf_into_multiple_pages

print("Initialising fonts.")
font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-VariableFont_opsz,wght.ttf")
italicFont: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-Italic-VariableFont_opsz,wght.ttf")
print("Fonts loaded.")

df = pd.read_csv('database.csv')
filepathBack = "images/back/"
filepathFront = "images/front/"
filepathOriginalImages = "images/originals/"
rounded_corners_filepath = "images/originals/cornermask.png"
one_card_per_page_output_file_name = "one_card_per_page_flashcards"
pagesPerPage = 3
chosen_transparency = 75 # approx quarter alpha (255 is no transparency at all, 0 is fully transparent)
pageWidth = 842 #A4 width
pageHeight = 595 #A4 height

print(f"Giving images rounded corners and making background images transparent.")
for index, row in df.iterrows():
    give_image_rounded_corners(filepathBack, filepathOriginalImages, rounded_corners_filepath, row['imageBack'])
    give_image_rounded_corners(filepathFront, filepathOriginalImages, rounded_corners_filepath, row['imageFront'])
    make_images_transparent(filepathBack, row['imageBack'], chosen_transparency) 

fullOutputFilePath : str = create_flashcards(df, font, italicFont, pageWidth, pageHeight, one_card_per_page_output_file_name)
transform_pdf_into_multiple_pages(pagesPerPage, fullOutputFilePath)
add_reference_pages(font, italicFont, pageWidth, pageHeight, df)