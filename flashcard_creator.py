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

from text_helper import clean_text, get_species_full_name_or_plural

def create_flashcards(df: pd.DataFrame, font: Font, italic_font: Font, pageWidth: int, page_height: int, full_output_file_path: str):
    
    document: Document = Document()
    divided_page: int = int((pageWidth/3))
    fromPageEdgeToCardOuterEdgeWidth = int((divided_page - 227)/2)
    fromPageEdgeToCardOuterEdgeHeight = int((page_height-340)/2)
    internal_padding = 23
    bottom_padding = 7   
    top_padding = 33  
    print("Creating cards.")
    
    for index, row in df.iterrows():
        curren_page: Page = Page(page_height, divided_page)
        document.append_page(curren_page)
        layout: PageLayout = SingleColumnLayout(curren_page, margin_left=fromPageEdgeToCardOuterEdgeWidth,margin_right=fromPageEdgeToCardOuterEdgeWidth, margin_bottom=fromPageEdgeToCardOuterEdgeHeight, margin_top=fromPageEdgeToCardOuterEdgeHeight)
        table_row_count = 5

        curren_page = paint_background_image(row, curren_page)

        if isinstance(row['exampleSpecies'],str):
            table_row_count = table_row_count + 1

        layout_table = FixedColumnWidthTable(number_of_columns=1, number_of_rows=table_row_count)
        layout_table.append_layout_element(add_family_name(internal_padding, font, row, top_padding, bottom_padding, 11))
        layout_table.append_layout_element(add_species_full_name(internal_padding, font, italic_font, row, 3, 17))
        if isinstance(row['exampleSpecies'],str):
                layout_table.append_layout_element(add_examples(internal_padding, italic_font, row, 0, 8))       
        layout_table.append_layout_element(add_common_names(internal_padding, font, row, 9, 12, 13))
        layout_table.append_layout_element(add_quote(internal_padding, font, row, 0, 8))
        layout_table.append_layout_element(add_short_reference(internal_padding, font, italic_font, row, 0, 6))
        layout_table.no_borders()

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
    quote = clean_text(row['quote'])
    if len(quote) > 800: #truncate if too long
        quote = quote[:800] + "..."
    quote_chunk = Chunk(quote, font=font, font_color=X11Color.BLACK, font_size = font_size)

    paragraph = HeterogeneousParagraph([open_and_closing_quote_mark,quote_chunk,open_and_closing_quote_mark],
            text_alignment=LayoutElement.TextAlignment.LEFT,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=bottomPadding,padding_left= internal_padding,padding_right = internal_padding,padding_top=0
        )

    return paragraph

def add_common_names(internal_padding, font, row, top_padding, bottom_padding, font_size):
    commonNames = clean_text("".join(list(row['commonNames'])))
    paragraph =  Paragraph(
            commonNames,
            font_color=X11Color.BLACK,
            font=font,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size = font_size,
            padding_bottom=bottom_padding,padding_left= internal_padding,padding_right = internal_padding,padding_top=top_padding
        )
    
    return paragraph

def add_examples(internal_padding, italic_font, row, bottomPadding, font_size):
    example_species_list = row['exampleSpecies'].split(",")
    genus_name = row['genus']
    shortened_species_list = replace_genus_with_initial(example_species_list, genus_name)

    example_species_names = clean_text("(e.g. " + ", ".join(shortened_species_list) + ")")
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

def replace_genus_with_initial(example_species_list, genus_name):
    shortened_species_list = []
    genus_name = str(genus_name).lower()

    for example in example_species_list:
            example = str(example).lower().strip()
            full_name : list[str] = example.split(' ')
            if genus_name in full_name[0]:
                full_name[0] = full_name[0][:1] + '.'
            full_name[0] = str(full_name[0]).title()
            shortened_species_list.append(" ".join(full_name))

    return shortened_species_list

def add_species_full_name(internal_padding, font, italic_font, row, bottom_padding, font_size):

    full_name = get_species_full_name_or_plural(row['genus'], row['species'])
    chunk_list = [Chunk(full_name, font=italic_font, font_color=X11Color.BLACK, font_size = font_size)]
    full_name_list = full_name.split(' ')

    if full_name_list[1] == 'spp.':
        genus = Chunk(full_name_list[0], font=italic_font, font_color=X11Color.BLACK, font_size = font_size)
        species_plural = Chunk(' spp.', font=font, font_color=X11Color.BLACK, font_size = font_size)
        chunk_list = [genus, species_plural]

    paragraph = HeterogeneousParagraph(chunk_list,
            text_alignment=LayoutElement.TextAlignment.LEFT,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=bottom_padding, padding_left= internal_padding,padding_right = internal_padding,padding_top=0
    )

    return paragraph

def add_family_name(internal_padding, font, row, top_padding, bottom_padding, font_size):

    table_row_count = 1
    table = FixedColumnWidthTable(number_of_columns=1, number_of_rows=table_row_count)
    family_name = clean_text(row['familyName']).upper()
    exemplar = ('(' + clean_text(row['familyExemplar']) + ' family)').upper()

    family_name_and_exemplar = family_name + ' ' + exemplar
    table.append_layout_element(Paragraph(
        family_name_and_exemplar,
        font_color=X11Color.BLACK,
        font=font,
        text_alignment=LayoutElement.TextAlignment.CENTERED,
        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        font_size = font_size,
        padding_bottom=bottom_padding,padding_left= internal_padding,padding_right = internal_padding,padding_top=top_padding
    ))

    if len(family_name_and_exemplar) > 26: #put the family example on a new line if it's too long
        table_row_count = table_row_count + 1
        table = FixedColumnWidthTable(number_of_columns=1, number_of_rows=table_row_count)
        table.append_layout_element(Paragraph(
        family_name,
        font_color=X11Color.BLACK,
        font=font,
        text_alignment=LayoutElement.TextAlignment.CENTERED,
        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        font_size = font_size,
        padding_bottom=3,padding_left= internal_padding,padding_right = internal_padding,padding_top=top_padding
    ))
        table.append_layout_element(Paragraph(
        exemplar,
        font_color=X11Color.BLACK,
        font=font,
        text_alignment=LayoutElement.TextAlignment.CENTERED,
        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        font_size = font_size,
        padding_bottom=bottom_padding,padding_left= internal_padding,padding_right = internal_padding,padding_top=0
    ))

    table.no_borders()
    return table


if __name__ == "__main__":
    df = pd.read_csv('example_database.csv')
    output_file_name = "flashcards"
    # Create a TrueTypeFont
    font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-Light.ttf")
    italic_font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-LightItalic.ttf")
    page_width = 842 #A4 width
    page_height = 595 #A4 height
    create_flashcards(df, font, italic_font, page_width, page_height, output_file_name)



