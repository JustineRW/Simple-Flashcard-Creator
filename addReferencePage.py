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
    MultiColumnLayout

)
import pathlib
import pandas as pd

# TODO make this into a function and pass in the variables

font: Font = TrueTypeFont.from_file("SourceSerif4-VariableFont_opsz,wght.ttf")
italicFont: Font = TrueTypeFont.from_file("SourceSerif4-Italic-VariableFont_opsz,wght.ttf")

pageWidth = 842 #A4 width
pageHeight = 595 #A4 height

df = pd.read_csv('database.csv')
document: Document = Document()

refPage = Page(pageHeight, pageWidth)
refPageLayout: PageLayout = MultiColumnLayout(refPage)
refPageLayout.append_layout_element(Paragraph("References", font_size=15, font=font))

for index, row in df.iterrows():
    refPageLayout.append_layout_element(Paragraph(row['genus'].title() + " Text:", font_size=7, font=italicFont))
    refPageLayout.append_layout_element(Paragraph(row['quoteFullReference'], font_size=7, font=font))
    refPageLayout.append_layout_element(Paragraph(row['genus'].title() + " Front Image:", font_size=7, font=italicFont))
    refPageLayout.append_layout_element(Paragraph(row['frontImageReference'], font_size=7, font=font))
    refPageLayout.append_layout_element(Paragraph(row['genus'].title() + " Back Image:", font_size=7, font=italicFont))
    refPageLayout.append_layout_element(Paragraph(row['backImageReference'], font_size=7, font=font))

# Write the PDF
document.append_page(refPage)
PDF.write(what=document, where_to="output/references.pdf")