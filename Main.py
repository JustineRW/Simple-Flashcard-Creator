from borb.pdf import (
    TrueTypeFont,
    Font,
)
import pandas as pd
from reference_page import add_reference_pages
from image_manipulation import give_image_rounded_corners, make_images_transparent, add_overlay
from botanical_flashcard_creator import create_flashcards
from pdf_transformer import transform_pdf_into_multiple_pages

print("Initialising fonts.")
font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-VariableFont_opsz,wght.ttf")
italic_font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-Italic-VariableFont_opsz,wght.ttf")
print("Fonts loaded.")

df = pd.read_csv('example_database.csv')
filepath_back = "images/back/"
filepath_front = "images/front/"
filepath_original_images = "images/originals/"
rounded_corners_filepath = "images/originals/cornermask.png"
overlay_filepath = "images/originals/background_image.jpg"
one_card_per_page_output_file_name = "one_card_per_page_flashcards"
cards_per_A4_page = 3
chosen_transparency = 125 # approx half alpha (255 is no transparency at all, 0 is fully transparent)
page_width = 842 #A4 width
page_height = 595 #A4 height

print(f"Giving images rounded corners and making background images transparent.")
for index, row in df.iterrows():
    back_image_filename: str | None = row["imageBack"]
    front_image_filename: str | None = row["imageFront"]
    requires_overlay: bool = row['requiresOverlay']

    if isinstance(back_image_filename,str):
        give_image_rounded_corners(filepath_back, filepath_original_images, rounded_corners_filepath, back_image_filename)
        make_images_transparent(filepath_back, back_image_filename, chosen_transparency) 
    if isinstance(front_image_filename,str):    
        if requires_overlay:
            add_overlay(filepath_front, filepath_original_images, overlay_filepath, front_image_filename, 62)
        give_image_rounded_corners(filepath_front, filepath_front, rounded_corners_filepath, front_image_filename)
            

full_output_filepath : str = create_flashcards(df, font, italic_font, page_width, page_height, one_card_per_page_output_file_name)
transform_pdf_into_multiple_pages(cards_per_A4_page, full_output_filepath)
# add_reference_pages(font, italic_font, page_width, page_height, df)
print('Done!')