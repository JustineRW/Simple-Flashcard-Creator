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
    SimpleFont,
    Chunk,
    TrueTypeFont,
    Font
)
import pathlib
import pandas as pd
import math
from PIL import Image as pillowImage


df = pd.read_csv('database.csv')
d: Document = Document()
thirdA4: int = int((842/3))
fromPageEdgeToCardOuterEdgeWidth = int((thirdA4 - 227)/2)
fromPageEdgeToCardOuterEdgeHeight = int((595-340)/2)
internalPadding = 15

# Create a TrueTypeFont
font: Font = TrueTypeFont.from_file("SourceSerif4-VariableFont_opsz,wght.ttf")
italicFont: Font = TrueTypeFont.from_file("SourceSerif4-Italic-VariableFont_opsz,wght.ttf")


for index, row in df.iterrows():

    p: Page = Page(595, thirdA4)
    d.append_page(p)
    l: PageLayout = SingleColumnLayout(p, margin_left=fromPageEdgeToCardOuterEdgeWidth,margin_right=fromPageEdgeToCardOuterEdgeWidth, margin_bottom=fromPageEdgeToCardOuterEdgeHeight, margin_top=fromPageEdgeToCardOuterEdgeHeight)


    # Paint the background on the back of the card
    x: int = p.get_size()[0] // 10
    y: int = p.get_size()[1] // 10
    w: int = p.get_size()[0] - 2 * (p.get_size()[0] // 10)
    h: int = p.get_size()[1] - 2 * (p.get_size()[1] // 10)
 
    img = pillowImage.open(pathlib.Path("images/back/" + row['imageBack']))
    img = img.convert("RGBA")
    img.putalpha(127)  # Half alpha; alpha argument must be an int
    img.save(pathlib.Path("images/back/" + "transparent" + row['imageBack']))

    Image(
            bytes_path_pil_image_or_url=pathlib.Path("images/back/" + row['imageBack']),
            size=(227, 340),
            border_width_top=2,
            border_width_right=2,
            border_width_bottom=2,
            border_width_left=2,
            border_color=X11Color.LIGHT_GRAY,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
       
    ).paint(
    available_space=(x, y, w, h),
    page=p,
    )


    l.append_layout_element(
        Paragraph(
            (row['familyName'] + ' (' + row['familyExemplar'] + ' family)').upper(),
            font_color=X11Color.BLACK,
            font=font,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size = 10,
            padding_bottom=2,padding_left= internalPadding,padding_right = internalPadding,padding_top=30
        )
    )


    speciesNameOrPlural = "spp." if math.isnan(row['species']) else row['species']


    l.append_layout_element(
        Paragraph(
            row['genus'] + ' ' + speciesNameOrPlural,
            font_color=X11Color.BLACK,
            font=italicFont,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size = 10,
            padding_bottom=2,padding_left= internalPadding,padding_right = internalPadding,padding_top=0
        )
    )


# TODO write a function for reducing each genus name to just the first letter e.g. M. instead of Morus
    # need to test with lack of example species
    if row['exampleSpecies']:
        exampleSpeciesNames = "(e.g. " + "".join(list(row['exampleSpecies'])) + ")"
        l.append_layout_element (  
            Paragraph(
            exampleSpeciesNames,
            font_color=X11Color.BLACK,
            font=italicFont,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size = 7,
            padding_bottom=2,padding_left= internalPadding,padding_right = internalPadding,padding_top=0
        ))
       
    commonNames = "".join(list(row['commonNames']))
    l.append_layout_element(
        Paragraph(
            commonNames,
            font_color=X11Color.BLACK,
            font=font,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size = 10,
            padding_bottom=2,padding_left= internalPadding,padding_right = internalPadding,padding_top=0
        )
    )


    # Quote
    # TODO write a function for splitting quotes
    quoteOpenAndClosingQuote = Chunk('"', font=font, font_size=8)
    # quoteTextPart1 = Chunk(row['genus'] + ' ' + speciesNameOrPlural, font=italicFont, font_size=8)
    quoteTextPart2 = Chunk(row['quote'], font=font, font_color=X11Color.BLACK, font_size = 8)


    l.append_layout_element(
        HeterogeneousParagraph([quoteOpenAndClosingQuote, quoteTextPart2,quoteOpenAndClosingQuote],
            text_alignment=LayoutElement.TextAlignment.LEFT,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=2,padding_left= internalPadding,padding_right = internalPadding,padding_top=0


        )
    )


    # Quote mini ref
    quoteAuthorFirstName = Chunk(row['quoteAuthorFirstName'] + " ", font_size=7, font=font)
    quoteAuthorLastName = Chunk( row['quoteAuthorLastName'], font_size=7, font=font)
    quoteYearPublished = Chunk(" ("+ str(row['quoteYearPublished']) + "),", font_size=7, font=font)
    quotePublicationTitle = Chunk(row['quotePublicationTitle'].capitalize(), font_size=7, font=italicFont)


    l.append_layout_element(
        HeterogeneousParagraph([quoteAuthorFirstName, quoteAuthorLastName, quoteYearPublished, quotePublicationTitle],
            text_alignment=LayoutElement.TextAlignment.LEFT,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=2,padding_left= internalPadding,padding_right = internalPadding,padding_top=0


        )
    )


    l.next_page()


    # Front
    l.append_layout_element(
        Image(
            bytes_path_pil_image_or_url=pathlib.Path("images/front/" + row['imageFront']),
            size=(227, 340),
            border_width_top=2,
            border_width_right=2,
            border_width_bottom=2,
            border_width_left=2,
            border_color=X11Color.LIGHT_GRAY,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            vertical_alignment=LayoutElement.VerticalAlignment.MIDDLE,
        )
    )


    # Write the PDF

PDF.write(what=d, where_to="flashcards.pdf")



