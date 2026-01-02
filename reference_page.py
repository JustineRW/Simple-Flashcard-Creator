from logging import Logger
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
    SingleColumnLayout,

)
import pandas as pd

from text_helper import clean_text, get_species_full_name

def add_reference_pages(font, italicFont, pageWidth, pageHeight, df):
    document: Document = Document()
    refPage = Page(pageHeight, pageWidth)
    document.append_page(refPage)
    refPageLayout: PageLayout = SingleColumnLayout(refPage)
    refPageLayout.append_layout_element(Paragraph("References", font_size=15, font=font))
    chosen_font_size = 10
    output_file_path = "output/references.pdf"

    print("Creating reference page.")

    for index, row in df.iterrows():

        full_name = get_species_full_name(row['genus'],row['species'])
        quote_full_reference = clean_text(row['quoteFullReference'])
        front_image_reference = clean_text(row['frontImageReference'])
        back_image_reference = clean_text(row['backImageReference'])

        refPageLayout.append_layout_element(Paragraph(full_name.capitalize() + " Text:", font_size=chosen_font_size, font=italicFont))
        refPageLayout.append_layout_element(Paragraph(quote_full_reference, font_size=chosen_font_size, font=font))
        refPageLayout.append_layout_element(Paragraph(full_name.capitalize() + " Front Image:", font_size=chosen_font_size, font=italicFont))
        refPageLayout.append_layout_element(Paragraph(front_image_reference, font_size=chosen_font_size, font=font))
        refPageLayout.append_layout_element(Paragraph(full_name.capitalize() + " Back Image:", font_size=chosen_font_size, font=italicFont, word_spacing=0.5))
        refPageLayout.append_layout_element(Paragraph(back_image_reference, font_size=chosen_font_size, font=font))
    
    # Write the PDF
    
    print(f"Writing reference pdf to '{output_file_path}'.")
    PDF.write(what=document, where_to=output_file_path)

if __name__ == "__main__":
    font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-VariableFont_opsz,wght.ttf")
    italicFont: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-Italic-VariableFont_opsz,wght.ttf")

    pageWidth = 842 #A4 width
    pageHeight = 595 #A4 height

    df = pd.read_csv('example_database.csv')

    add_reference_pages(font, italicFont, pageWidth, pageHeight, df)