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
    MultiColumnLayout

)
import pathlib
import pandas as pd
import math
import datetime

def createFlashcards(df: pd.DataFrame, font: Font, italicFont: Font, pageWidth: int, pageHeight: int, fullOutputFilePath: str):
    
    document: Document = Document()
    dividedPage: int = int((pageWidth/3))
    fromPageEdgeToCardOuterEdgeWidth = int((dividedPage - 227)/2)
    fromPageEdgeToCardOuterEdgeHeight = int((pageHeight-340)/2)
    internalPadding = 22     
    
    for index, row in df.iterrows():
        currentPage: Page = Page(pageHeight, dividedPage)
        document.append_page(currentPage)
        layout: PageLayout = SingleColumnLayout(currentPage, margin_left=fromPageEdgeToCardOuterEdgeWidth,margin_right=fromPageEdgeToCardOuterEdgeWidth, margin_bottom=fromPageEdgeToCardOuterEdgeHeight, margin_top=fromPageEdgeToCardOuterEdgeHeight)

        currentPage = paintBackgroundImage(row, currentPage)
        layout = addFamilyName(internalPadding, font, row, layout)
        layout = addSpeciesFullName(internalPadding, italicFont, row, layout)
        layout = addExamples(internalPadding, italicFont, row, layout)       
        layout = addCommonNames(internalPadding, font, row, layout)
        layout = addQuote(internalPadding, font, row, layout)
        layout = addShortReference(internalPadding, font, italicFont, row, layout)
        layout.next_page()
        layout = addFrontImage(row, layout)

    fullOutputFilePath = "output\\" + fullOutputFilePath + datetime.datetime.now().strftime("%H%M%S") + ".pdf"
    PDF.write(what=document, where_to=fullOutputFilePath)
    return fullOutputFilePath


def paintBackgroundImage(row, currentPage):
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

def addFrontImage(row, layout):
    layout.append_layout_element(
    Image(
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
    )
    return layout
    

def addShortReference(internalPadding, font, italicFont, row, layout):
    quoteAuthorFirstName = Chunk(row['quoteAuthorFirstName'] + " ", font_size=7, font=font)
    quoteAuthorLastName = Chunk( row['quoteAuthorLastName'], font_size=7, font=font)
    quoteYearPublished = Chunk(" ("+ str(row['quoteYearPublished']) + "),", font_size=7, font=font)
    quotePublicationTitle = Chunk(row['quotePublicationTitle'].title(), font_size=7, font=italicFont)

    layout.append_layout_element(
        HeterogeneousParagraph([quoteAuthorFirstName, quoteAuthorLastName, quoteYearPublished, quotePublicationTitle],
            text_alignment=LayoutElement.TextAlignment.LEFT,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=2,padding_left= internalPadding,padding_right = internalPadding,padding_top=0
        )
    )
    return layout

def addQuote(internalPadding, font, row, layout):
    # TODO write a function for splitting quotes
    openAndClosingQuoteMark = Chunk('"', font=font, font_size=8)
    # quoteTextPart1 = Chunk(row['genus'] + ' ' + speciesNameOrPlural, font=italicFont, font_size=8)
    quoteTextPart2 = Chunk(row['quote'], font=font, font_color=X11Color.BLACK, font_size = 8)

    layout.append_layout_element(
        HeterogeneousParagraph([openAndClosingQuoteMark, quoteTextPart2,openAndClosingQuoteMark],
            text_alignment=LayoutElement.TextAlignment.LEFT,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            padding_bottom=2,padding_left= internalPadding,padding_right = internalPadding,padding_top=0
        )
    )
    return layout

def addCommonNames(internalPadding, font, row, layout):
    commonNames = "".join(list(row['commonNames']))
    layout.append_layout_element(
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
    return layout

def addExamples(internalPadding, italicFont, row, layout):
    # TODO write a function for reducing each genus name to just the first letter e.g. M. instead of Morus
    if isinstance(row['exampleSpecies'],str):
        exampleSpeciesNames = "(e.g. " + "".join(list(row['exampleSpecies'])) + ")"
        layout.append_layout_element (  
            Paragraph(
            exampleSpeciesNames,
            font_color=X11Color.BLACK,
            font=italicFont,
            text_alignment=LayoutElement.TextAlignment.CENTERED,
            horizontal_alignment=LayoutElement.HorizontalAlignment.MIDDLE,
            font_size = 7,
            padding_bottom=2,padding_left= internalPadding,padding_right = internalPadding,padding_top=0
        ))
    return layout

def addSpeciesFullName(internalPadding, italicFont, row, layout):
    speciesNameOrPlural = row['species'] if isinstance(row['species'], str) else 'spp.' #empty species cell indicates we just want to use the genus name

    layout.append_layout_element(
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
    return layout

def addFamilyName(internalPadding, font, row, layout):
    layout.append_layout_element(
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

    return layout


if __name__ == "__main__":
    df = pd.read_csv('database.csv')
    outputFileName = "flashcards"
    # Create a TrueTypeFont
    font: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-VariableFont_opsz,wght.ttf")
    italicFont: Font = TrueTypeFont.from_file("fonts\\SourceSerif4-Italic-VariableFont_opsz,wght.ttf")
    pageWidth = 842 #A4 width
    pageHeight = 595 #A4 height
    createFlashcards(df, font, italicFont, pageWidth, pageHeight, outputFileName)



