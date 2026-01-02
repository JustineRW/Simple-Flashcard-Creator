from borb.pdf import (
    Document,
    Image,
    LayoutElement,
    Page,
    PageLayout,
    PDF,
    SingleColumnLayout,
    X11Color,
    HeterogeneousParagraph,
    Paragraph,
    Chunk,
    TrueTypeFont,
    Font,
    FixedColumnWidthTable
)
import pathlib
import pandas as pd
import datetime

from text_helper import clean_text, get_species_full_name

def create_flashcards(df: pd.DataFrame, font: Font, italic_font: Font, pageWidth: int, pageHeight: int, full_output_file_path: str):
    
    document: Document = Document()
    dividedPage: int = int((pageWidth/3))
    fromPageEdgeToCardOuterEdgeWidth = int((dividedPage - 227)/2)
    fromPageEdgeToCardOuterEdgeHeight = int((pageHeight-340)/2)
    internal_padding = 22
    bottom_padding = 1     
    print("Creating cards.")
    
    for index, row in df.iterrows():
        currentPage: Page = Page(pageHeight, dividedPage)
        document.append_page(currentPage)
        layout: PageLayout = SingleColumnLayout(currentPage, margin_left=fromPageEdgeToCardOuterEdgeWidth,margin_right=fromPageEdgeToCardOuterEdgeWidth, margin_bottom=fromPageEdgeToCardOuterEdgeHeight, margin_top=fromPageEdgeToCardOuterEdgeHeight)
        table_row_count = 5

        currentPage = paint_background_image(row, currentPage)

        if isinstance(row['exampleSpecies'],str):
            table_row_count = 6

        layout_table = FixedColumnWidthTable(number_of_columns=1, number_of_rows=table_row_count, border_color=None)
        layout_table.append_layout_element(add_family_name(internal_padding, font, row, bottom_padding, 11))
        layout_table.append_layout_element(add_species_full_name(internal_padding, italic_font, row, bottom_padding, 17))
        if isinstance(row['exampleSpecies'],str):
                layout_table.append_layout_element(add_examples(internal_padding, italic_font, row, bottom_padding, 10))       
        layout_table.append_layout_element(add_common_names(internal_padding, font, row, bottom_padding, 9))
        layout_table.append_layout_element(add_quote(internal_padding, font, row, bottom_padding, 8))
        layout_table.append_layout_element(add_short_reference(internal_padding, font, italic_font, row, bottom_padding, 7))

        layout.append_layout_element(layout_table)
        layout.next_page()
        layout.append_layout_element(add_front_image(row))

    full_output_file_path = "output\\" + full_output_file_path + "_" + datetime.datetime.now().strftime("%H%M%S") + ".pdf"
    print(f"Writing cards to one card per page pdf, at '{full_output_file_path}'")
    PDF.write(what=document, where_to=full_output_file_path)
    return full_output_file_path


def paint_background_image(row, currentPage):
    x: int = currentPage.get_size()[0] // 10
    y: int = currentPage.get_size()[1] // 10
    w: int = currentPage.get_size()[0] - 2 * (currentPage.get_size()[0] // 10)
    h: int = currentPage.get_size()[1] - 2 * (currentPage.get_size()[1] // 10)

    fileNameAsPng = row['imageBack'].split('.')[0] + '.png'

    Image(
            bytes_path_pil_image_or_url=pathlib.Path("images/back/" + fileNameAsPng),
            size=(227, 340),
            border_width_top=1,
            border_width_right=1,
            border_width_bottom=1,
            border_width_left=1,
            border_color=X11Color.LIGHT_GRAY,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
    ).paint(
    available_space=(x, y, w, h),
    page=currentPage,
    )

    return currentPage

def add_front_image(row):
    image = Image(
            bytes_path_pil_image_or_url=pathlib.Path("images/front/" + row['imageFront']),
            size=(227, 340),
            border_width_top=1,
            border_width_right=1,
            border_width_bottom=1,
            border_width_left=1,
            border_color=X11Color.LIGHT_GRAY,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        )    
    return image
    

def add_short_reference(internal_padding, font, italic_font, row, bottom_padding, font_size):
    quoteAuthorFirstName = Chunk(clean_text(row['quoteAuthorFirstName']) + " ", font_size=font_size, font=font)
    quoteAuthorLastName = Chunk( clean_text(row['quoteAuthorLastName']), font_size=font_size, font=font)
    quoteYearPublished = Chunk(" ("+ clean_text(str(row['quoteYearPublished'])) + "), ", font_size=font_size, font=font)
    quotePublicationTitle = Chunk(clean_text(row['quotePublicationTitle']).title(), font_size=font_size, font=italic_font)

    paragraph = HeterogeneousParagraph([quoteAuthorFirstName, quoteAuthorLastName, quoteYearPublished, quotePublicationTitle],
            text_alignment=LayoutElement.TextAlignment.LEFT,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=bottom_padding,padding_left= internal_padding,padding_right = internal_padding,padding_top=0
        )
    
    return paragraph

def add_quote(internal_padding, font, row, bottomPadding, font_size):
    # TODO write a function for splitting quotes so that species names are correctly italised
    open_and_closing_quote_mark = Chunk('"', font=font, font_size= font_size)
    quote = Chunk(clean_text(row['quote']), font=font, font_color=X11Color.BLACK, font_size = font_size)

    paragraph = HeterogeneousParagraph([open_and_closing_quote_mark, quote,open_and_closing_quote_mark],
            text_alignment=LayoutElement.TextAlignment.LEFT,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=bottomPadding,padding_left= internal_padding,padding_right = internal_padding,padding_top=0
        )

    return paragraph

def add_common_names(internal_padding, font, row, bottomPadding, font_size):
    commonNames = clean_text("".join(list(row['commonNames'])))
    paragraph =  Paragraph(
            commonNames,
            font_color=X11Color.BLACK,
            font=font,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size = font_size,
            padding_bottom=bottomPadding,padding_left= internal_padding,padding_right = internal_padding,padding_top=0
        )
    
    return paragraph

def add_examples(internal_padding, italic_font, row, bottomPadding, font_size):
    # TODO write a function for reducing each genus name to just the first letter e.g. M. instead of Morus
    example_species_names = clean_text("(e.g. " + "".join(list(row['exampleSpecies'])) + ")")
    paragraph = Paragraph(
        example_species_names,
        font_color=X11Color.BLACK,
        font=italic_font,
        text_alignment=LayoutElement.TextAlignment.CENTERED,
        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        font_size = font_size,
        padding_bottom=bottomPadding,padding_left= internal_padding,padding_right = internal_padding,padding_top=0
    )
    return paragraph

def add_species_full_name(internal_padding, italic_font, row, bottom_padding, font_size):

    full_name = get_species_full_name(row['genus'], row['species'])

    paragraph = Paragraph(
            full_name,
            font_color=X11Color.BLACK,
            font=italic_font,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size = font_size,
            padding_bottom=bottom_padding,padding_left= internal_padding,padding_right = internal_padding,padding_top=0
        )

    return paragraph

def add_family_name(internal_padding, font, row, bottomPadding, font_size):
    family_name_and_exemplar = clean_text(row['familyName'] + ' (' + row['familyExemplar'] + ' family)')
      
    paragraph = Paragraph(
            family_name_and_exemplar.upper(),
            font_color=X11Color.BLACK,
            font=font,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size = font_size,
            padding_bottom=bottomPadding,padding_left= internal_padding,padding_right = internal_padding,padding_top=30
        )  

    return paragraph


if __name__ == "__main__":
    df = pd.read_csv('example_database.csv')
    outputFileName = "flashcards"
    # Create a TrueTypeFont
    font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-VariableFont_opsz,wght.ttf")
    italic_font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-Italic-VariableFont_opsz,wght.ttf")
    pageWidth = 842 #A4 width
    pageHeight = 595 #A4 height
    create_flashcards(df, font, italic_font, pageWidth, pageHeight, outputFileName)



