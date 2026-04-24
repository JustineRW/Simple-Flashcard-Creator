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
from PIL import Image as PilImage
import os.path 
from text_helper import clean_text, get_species_full_name_or_plural

def create_flashcards(df: pd.DataFrame, font: Font, italic_font: Font, pageWidth: int, page_height: int, full_output_file_path: str):
    
    document: Document = Document()
    divided_page: int = int((pageWidth/3))
    image_width = 227
    image_height = 340
    image_border_width = 1
    image_border_colour = X11Color.LIGHT_GRAY
    fromPageEdgeToCardOuterEdgeWidth = int((divided_page - image_width)/2)
    fromPageEdgeToCardOuterEdgeHeight = int((page_height - image_height)/2)
    internal_padding = 23
    bottom_padding = 7   
    top_padding = 35  

    print("Creating cards.")
    
    for index, row in df.iterrows():
        current_page: Page = Page(page_height, divided_page)
        document.append_page(current_page)
        layout: PageLayout = SingleColumnLayout(current_page, margin_left=fromPageEdgeToCardOuterEdgeWidth,margin_right=fromPageEdgeToCardOuterEdgeWidth, margin_bottom=fromPageEdgeToCardOuterEdgeHeight, margin_top=fromPageEdgeToCardOuterEdgeHeight)
        table_row_count = 5

        current_page = paint_background_image(row, current_page, image_width, image_height, image_border_colour, image_border_width)

        if isinstance(row['exampleSpecies'],str):
            table_row_count = table_row_count + 1

        layout_table = FixedColumnWidthTable(number_of_columns=1, number_of_rows=table_row_count)
        layout_table.append_layout_element(add_family_name(internal_padding, font, row, top_padding, bottom_padding, 11))
        layout_table.append_layout_element(add_species_full_name(internal_padding, font, italic_font, row, 4, 17))
        if isinstance(row['exampleSpecies'],str):
                layout_table.append_layout_element(add_examples(internal_padding, italic_font, row, 0, 8))       
        layout_table.append_layout_element(add_common_names(internal_padding, font, row, 9, 12, 13))
        layout_table.append_layout_element(add_quote(internal_padding, font, row, 0, 8))
        layout_table.append_layout_element(add_short_reference(internal_padding, font, italic_font, row, 0, 7))
        layout_table.no_borders()

        try:
            layout.append_layout_element(layout_table)
        except:
            print(f"ERROR: Was unable to create the {str(row['genus'])} back page. Please investigate the data for special characters that might be causing issues.")

        layout.next_page()
        front_image = add_front_image(row, image_width, image_height, image_border_colour, image_border_width)
        layout.append_layout_element(front_image)

    full_output_file_path = "output\\" + full_output_file_path + "_" + datetime.datetime.now().strftime("%H%M%S") + ".pdf"
    print(f"Writing cards to one card per page pdf, at '{full_output_file_path}'")
    PDF.write(what=document, where_to=full_output_file_path)
    return full_output_file_path

def paint_background_image(row, currentPage, image_width, image_height, image_border_colour, image_border_width):
    x: int = currentPage.get_size()[0] // 10
    y: int = currentPage.get_size()[1] // 10
    w: int = currentPage.get_size()[0] - 2 * (currentPage.get_size()[0] // 10)
    h: int = currentPage.get_size()[1] - 2 * (currentPage.get_size()[1] // 10)

    filename_as_png = str(row['imageBack']).split('.')[0] + '.png'
    image_filepath = pathlib.Path("images/back/" + filename_as_png)
    blank_pil_image = PilImage.new(mode="RGB", size=(image_width, image_height), color = (152, 251, 152))

    if os.path.isfile(image_filepath):
      image : Image = create_image_with_file_ref(image_filepath, image_width, image_height, image_border_colour, image_border_width)
    else:
        print(f"Background image for {str(row["genus"])} not found. Background will be left blank.")
        image : Image = create_blank_image(blank_pil_image, image_width, image_height, image_border_colour, image_border_width)

    image.paint(
        available_space=(x, y, w, h),
        page=currentPage,
    )

    return currentPage

def create_image_with_file_ref(image_filepath, image_width, image_height, image_border_colour, image_border_width):
    return Image(
                bytes_path_pil_image_or_url=pathlib.Path(image_filepath),
                size=(image_width, image_height),
                border_width_top=image_border_width,
                border_width_right=image_border_width,
                border_width_bottom=image_border_width,
                border_width_left=image_border_width,
                border_color=image_border_colour,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        )

def create_blank_image(pil_image, image_width, image_height, image_border_colour, image_border_width):
        return Image(
            pil_image,
            size=(image_width, image_height),
            border_width_top=image_border_width,
            border_width_right=image_border_width,
            border_width_bottom=image_border_width,
            border_width_left=image_border_width,
            border_color=image_border_colour,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        )

def add_front_image(row, image_width, image_height, image_border_colour, image_border_width):
    image_filepath = pathlib.Path("images/front/" + str(row['imageFront']))
    blank_pil_image = PilImage.new(mode="RGB", size=(image_width, image_height), color = (152, 251, 152))
    
    if os.path.isfile(image_filepath):
        image : Image = create_image_with_file_ref(image_filepath, image_width, image_height, image_border_colour, image_border_width)
    else:
        print(f"Front image for {str(row["genus"])} not found. Front image will be left blank.")
        image : Image = create_blank_image(blank_pil_image, image_width, image_height, image_border_colour, image_border_width)

    return image        

def add_short_reference(internal_padding, font, italic_font, row, bottom_padding, font_size):
    quoteAuthorFirstName = Chunk(clean_text(str(row['quoteAuthorFirstName'])) + " ", font_size=font_size, font=font)
    quoteAuthorLastName = Chunk( clean_text(str(row['quoteAuthorLastName'])), font_size=font_size, font=font)
    quoteYearPublished = Chunk(" ("+ clean_text(str(row['quoteYearPublished'])) + "), ", font_size=font_size, font=font)
    quotePublicationTitle = Chunk(clean_text(str(row['quotePublicationTitle'])).title(), font_size=font_size, font=italic_font)

    paragraph = HeterogeneousParagraph([quoteAuthorFirstName, quoteAuthorLastName, quoteYearPublished, quotePublicationTitle],
            text_alignment=LayoutElement.TextAlignment.LEFT,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=bottom_padding,padding_left= internal_padding,padding_right = internal_padding,padding_top=0
        )
    
    return paragraph

def add_quote(internal_padding, font, row, bottomPadding, font_size):
    # TODO write a function for splitting quotes so that species names are correctly italised
    open_and_closing_quote_mark = Chunk('"', font=font, font_size= font_size)
    quote = clean_text(str(row['quote']))
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
    commonNames = clean_text("".join(list(str(row['commonNames']))))
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
    example_species_list = str(row['exampleSpecies']).split(",")
    genus_name = str(row['genus'])
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

    full_name = get_species_full_name_or_plural(str(row['genus']), str(row['species']))
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
    family_name = clean_text(str(row['familyName'])).upper()
    exemplar = ('(' + clean_text(str(row['familyExemplar'])) + ' family)').upper()

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
    font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-VariableFont_opsz,wght.ttf")
    italic_font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-Italic-VariableFont_opsz,wght.ttf")
    page_width = 842 #A4 width
    page_height = 595 #A4 height
    create_flashcards(df, font, italic_font, page_width, page_height, output_file_name)



