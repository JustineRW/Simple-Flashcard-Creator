import datetime
import pathlib

import pandas as pd
from borb.pdf import (
    PDF,
    Chunk,
    Document,
    FixedColumnWidthTable,
    Font,
    HeterogeneousParagraph,
    Image,
    LayoutElement,
    Page,
    PageLayout,
    Paragraph,
    SingleColumnLayout,
    TrueTypeFont,
    X11Color,
)
from PIL import Image as PilImage

from botanical_flashcard import Botanical_Flashcard
from image_manipulation import get_image_name_with_suffix
from text_helper import clean_text, get_species_full_name_or_plural


def create_flashcards(
    df: pd.DataFrame,
    font: Font,
    italic_font: Font,
    pageWidth: int,
    page_height: int,
    full_output_file_path: str,
):

    document: Document = Document()
    divided_page: int = int(pageWidth / 3)
    image_width: int = 227
    image_height: int = 340
    image_border_width: int = 1
    image_border_colour = X11Color.LIGHT_GRAY
    fromPageEdgeToCardOuterEdgeWidth: int = int((divided_page - image_width) / 2)
    fromPageEdgeToCardOuterEdgeHeight: int = int((page_height - image_height) / 2)
    xy_padding: int = 23
    bottom_padding: int = 10
    top_padding: int = 35

    print("Creating cards.")

    for index, row in df.iterrows():
        botanical_data: Botanical_Flashcard = Botanical_Flashcard(row)

        print(f"Creating card for {botanical_data.genus!s}")
        current_page: Page = Page(page_height, divided_page)
        document.append_page(current_page)
        layout: PageLayout = SingleColumnLayout(
            current_page,
            margin_left=fromPageEdgeToCardOuterEdgeWidth,
            margin_right=fromPageEdgeToCardOuterEdgeWidth,
            margin_bottom=fromPageEdgeToCardOuterEdgeHeight,
            margin_top=fromPageEdgeToCardOuterEdgeHeight,
        )
        table_row_count = 5

        background_image = get_background_image(
            botanical_data.imageBack,
            image_width,
            image_height,
            image_border_colour,
            image_border_width,
        )
        current_page = paint_background_image(current_page, background_image)

        if isinstance(botanical_data.exampleSpecies, str):
            table_row_count = table_row_count + 1

        layout_table = FixedColumnWidthTable(number_of_columns=1, number_of_rows=table_row_count)
        layout_table.append_layout_element(
            add_family_name(xy_padding, font, botanical_data, top_padding, bottom_padding, 11)
        )
        layout_table.append_layout_element(add_species_full_name(xy_padding, font, italic_font, botanical_data, 4, 16))
        if isinstance(botanical_data.exampleSpecies, str):
            layout_table.append_layout_element(add_examples(xy_padding, italic_font, botanical_data, 0, 7))
        layout_table.append_layout_element(add_common_names(xy_padding, font, botanical_data, 9, 13, 13))
        layout_table.append_layout_element(add_quote(xy_padding, font, botanical_data, 1, 7))
        layout_table.append_layout_element(add_short_reference(xy_padding, font, italic_font, botanical_data, 0, 7))
        layout_table.no_borders()

        try:
            layout.append_layout_element(layout_table)
        except:
            print(
                f"ERROR: Was unable to create the {botanical_data.genus!s} back page. Please investigate the data for special characters that might be causing issues."
            )

        layout.next_page()
        front_image = add_front_image(
            botanical_data, image_width, image_height, image_border_colour, image_border_width
        )
        layout.append_layout_element(front_image)

    full_output_file_path = (
        "output\\" + full_output_file_path + "_" + datetime.datetime.now().strftime("%I%M%S_%p") + ".pdf"
    )

    print(f"Writing cards to one card per page pdf, at '{full_output_file_path}'")
    PDF.write(what=document, where_to=full_output_file_path)
    return full_output_file_path


def get_background_image(image_file_name, image_width, image_height, image_border_colour, image_border_width):

    blank_pil_image = PilImage.new(mode="RGB", size=(image_width, image_height), color=(255, 255, 255))
    image: Image = create_blank_image(
        blank_pil_image,
        image_width,
        image_height,
        image_border_colour,
        image_border_width,
    )

    if isinstance(image_file_name, str):
        filename_as_png = image_file_name.split(".")[0] + ".png"
        image_filepath = pathlib.Path("images/back/" + filename_as_png)

        if pathlib.Path(image_filepath).exists():
            image: Image = create_image_via_file_ref(
                image_filepath,
                image_width,
                image_height,
                image_border_colour,
                image_border_width,
            )
        else:
            print(f"Background image for {image_file_name!s} not found. Background will be left blank.")
    else:
        print(f"No background image name listed for {image_file_name!s}. Background will be left blank.")

    return image


def paint_background_image(currentPage : Page, image : Image):

    x: int = currentPage.get_size()[0] // 10
    y: int = currentPage.get_size()[1] // 10
    w: int = currentPage.get_size()[0] - 2 * (currentPage.get_size()[0] // 10)
    h: int = currentPage.get_size()[1] - 2 * (currentPage.get_size()[1] // 10)

    image.paint(
        available_space=(x, y, w, h),
        page=currentPage,
    )

    return currentPage


def create_image_via_file_ref(image_filepath, image_width : int, image_height : int, image_border_colour, image_border_width : int):
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


def add_front_image(
    botanical_data: Botanical_Flashcard, image_width, image_height, image_border_colour, image_border_width
):

    blank_pil_image = PilImage.new(mode="RGB", size=(image_width, image_height), color=(255, 255, 255))
    image: Image = create_blank_image(
        blank_pil_image,
        image_width,
        image_height,
        image_border_colour,
        image_border_width,
    )

    if isinstance(botanical_data.imageFront, str):
        image_filepath = pathlib.Path(
            "images/front/" + get_image_name_with_suffix("images/front/", botanical_data.imageFront)
        )

        if pathlib.Path(image_filepath).exists():
            image: Image = create_image_via_file_ref(
                image_filepath,
                image_width,
                image_height,
                image_border_colour,
                image_border_width,
            )
        else:
            print(f"Front image for {botanical_data.genus!s} not found. Front image will be left blank.")

    return image


def add_short_reference(
    internal_padding, font, italic_font, botanical_data: Botanical_Flashcard, bottom_padding, font_size
):

    quoteAuthorFirstName = Chunk("")
    quoteAuthorLastName = Chunk("")
    quoteYearPublished = Chunk("")
    quotePublicationTitle = Chunk("")
    separating_comma = Chunk(", ")

    if isinstance(botanical_data.quoteAuthorFirstName, str):
        quoteAuthorFirstName = Chunk(
            clean_text(botanical_data.quoteAuthorFirstName) + " ",
            font_size=font_size,
            font=font,
        )
    if isinstance(botanical_data.quoteAuthorLastName, str):
        quoteAuthorLastName = Chunk(
            clean_text(botanical_data.quoteAuthorLastName),
            font_size=font_size,
            font=font,
        )
    if isinstance(botanical_data.quotePublicationTitle, str):
        quotePublicationTitle = Chunk(
            clean_text(botanical_data.quotePublicationTitle),
            font_size=font_size,
            font=italic_font,
        )
    if isinstance(botanical_data.quoteYearPublished, str):
        quoteYearPublished = Chunk(
            " (" + clean_text(botanical_data.quoteYearPublished) + ")",
            font_size=font_size,
            font=font,
        )

    paragraph = HeterogeneousParagraph(
        [
            quoteAuthorFirstName,
            quoteAuthorLastName,
            quoteYearPublished,
            separating_comma,
            quotePublicationTitle,
        ],
        text_alignment=LayoutElement.TextAlignment.LEFT,
        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        padding_bottom=bottom_padding,
        padding_left=internal_padding,
        padding_right=internal_padding,
        padding_top=0,
    )

    return paragraph


def add_quote(internal_padding, font, botanical_data : Botanical_Flashcard, bottomPadding, font_size):
    # TODO write a function for splitting quotes so that species names are correctly italised
    open_and_closing_quote_mark = Chunk('"', font=font, font_size=font_size)
    quote = clean_text(str(botanical_data.quote))
    max_quote_length = 700

    if len(quote) > max_quote_length:  # truncate if too long
        quote = quote[:max_quote_length] + "..."
    quote_chunk = Chunk(quote, font=font, font_color=X11Color.BLACK, font_size=font_size)

    paragraph = HeterogeneousParagraph(
        [open_and_closing_quote_mark, quote_chunk, open_and_closing_quote_mark],
        text_alignment=LayoutElement.TextAlignment.LEFT,
        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        padding_bottom=bottomPadding,
        padding_left=internal_padding,
        padding_right=internal_padding,
        padding_top=0,
    )

    return paragraph


def add_common_names(internal_padding, font, botanical_data : Botanical_Flashcard, top_padding, bottom_padding, font_size):

    if not isinstance(botanical_data.commonNames, str):
        return Paragraph(text="")

    common_names_list: list = botanical_data.commonNames.split(",")
    capitalised_common_names_list: list = []

    for i in range(0, len(common_names_list)):
        common_name: str = common_names_list[i].strip()
        # Capitalise first common name in the list
        if i == 0:
            common_name = common_name[0].upper() + common_name[1:]
        capitalised_common_names_list.append(common_name)

    capitalised_common_names: str = clean_text(", ".join(capitalised_common_names_list))
    paragraph = Paragraph(
        capitalised_common_names,
        font_color=X11Color.BLACK,
        font=font,
        text_alignment=LayoutElement.TextAlignment.CENTERED,
        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        font_size=font_size,
        padding_bottom=bottom_padding,
        padding_left=internal_padding,
        padding_right=internal_padding,
        padding_top=top_padding,
    )

    return paragraph


def add_examples(internal_padding, italic_font, botanical_data : Botanical_Flashcard, bottomPadding, font_size):
    example_species_list = str(botanical_data.exampleSpecies).split(",")
    genus_name = str(botanical_data.genus)
    shortened_species_list = replace_genus_with_initial(example_species_list, genus_name)

    example_species_names = clean_text("e.g. " + ", ".join(shortened_species_list))
    paragraph = Paragraph(
        example_species_names,
        font_color=X11Color.BLACK,
        font=italic_font,
        text_alignment=LayoutElement.TextAlignment.CENTERED,
        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        font_size=font_size,
        padding_bottom=bottomPadding,
        padding_left=internal_padding,
        padding_right=internal_padding,
        padding_top=0,
    )
    return paragraph


def replace_genus_with_initial(example_species_list, genus_name):
    shortened_species_list = []
    genus_name = str(genus_name).lower()

    for example in example_species_list:
        example = str(example).strip()
        full_name: list[str] = example.split(" ")
        if genus_name in full_name[0].lower():
            full_name[0] = full_name[0][:1] + "."
        full_name[0] = str(full_name[0]).title()
        shortened_species_list.append(" ".join(full_name))

    return shortened_species_list


def add_species_full_name(internal_padding, font, italic_font, botanical_data : Botanical_Flashcard, bottom_padding, font_size):

    full_name = get_species_full_name_or_plural(str(botanical_data.genus), str(botanical_data.species))
    chunk_list = [Chunk(full_name, font=italic_font, font_color=X11Color.BLACK, font_size=font_size)]
    full_name_list = full_name.split(" ")

    if full_name_list[1] == "spp.":
        genus = Chunk(
            full_name_list[0],
            font=italic_font,
            font_color=X11Color.BLACK,
            font_size=font_size,
        )
        species_plural = Chunk(" spp.", font=font, font_color=X11Color.BLACK, font_size=font_size)
        chunk_list = [genus, species_plural]

    paragraph = HeterogeneousParagraph(
        chunk_list,
        text_alignment=LayoutElement.TextAlignment.LEFT,
        horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
        padding_bottom=bottom_padding,
        padding_left=internal_padding,
        padding_right=internal_padding,
        padding_top=0,
    )

    return paragraph


def add_family_name(internal_padding, font, botanical_data : Botanical_Flashcard, top_padding, bottom_padding, font_size):

    table_row_count = 1
    table = FixedColumnWidthTable(number_of_columns=1, number_of_rows=table_row_count)
    family_name = clean_text(str(botanical_data.familyName)).upper()
    exemplar = clean_text(str(botanical_data.familyExemplar))
    exemplar = (" (" + exemplar + " family)").upper() if exemplar != "nan" else ""

    family_name_and_exemplar = family_name + exemplar
    table.append_layout_element(
        Paragraph(
            family_name_and_exemplar,
            font_color=X11Color.BLACK,
            font=font,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size=font_size,
            padding_bottom=bottom_padding,
            padding_left=internal_padding,
            padding_right=internal_padding,
            padding_top=top_padding,
        )
    )

    if len(family_name_and_exemplar) > 26:  # put the family example on a new line if it's too long
        table_row_count = table_row_count + 1
        table = FixedColumnWidthTable(number_of_columns=1, number_of_rows=table_row_count)
        table.append_layout_element(
            Paragraph(
                family_name,
                font_color=X11Color.BLACK,
                font=font,
                text_alignment=LayoutElement.TextAlignment.CENTERED,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                font_size=font_size,
                padding_bottom=3,
                padding_left=internal_padding,
                padding_right=internal_padding,
                padding_top=top_padding,
            )
        )
        table.append_layout_element(
            Paragraph(
                exemplar,
                font_color=X11Color.BLACK,
                font=font,
                text_alignment=LayoutElement.TextAlignment.CENTERED,
                horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
                font_size=font_size,
                padding_bottom=bottom_padding,
                padding_left=internal_padding,
                padding_right=internal_padding,
                padding_top=0,
            )
        )

    table.no_borders()
    return table


if __name__ == "__main__":
    df = pd.read_csv("example_database.csv")
    output_file_name = "flashcards"
    # Create a TrueTypeFont
    font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-VariableFont_opsz,wght.ttf")
    italic_font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-Italic-VariableFont_opsz,wght.ttf")
    page_width = 842  # A4 width
    page_height = 595  # A4 height
    create_flashcards(df, font, italic_font, page_width, page_height, output_file_name)
