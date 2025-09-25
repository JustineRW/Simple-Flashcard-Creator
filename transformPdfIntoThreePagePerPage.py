from pypdf import PdfReader, PdfWriter, Transformation

# TODO need to refer back to original code for making new pages, or add in a skip for every three pages
thirdA4: int = int((842/3))
pdf_width = thirdA4
pdf_height = 595

pdf_source = PdfReader("flashcards.pdf")
numberOfPages = len(pdf_source.pages)
output = PdfWriter()
output.add_blank_page(pdf_width * numberOfPages, pdf_height)

for index_pdf in range(numberOfPages):
    for index_page, page in enumerate(pdf_source.pages):
        output.pages[0].merge_transformed_page(
            page,
            Transformation().translate(index_page * pdf_width, (numberOfPages - index_pdf - 1) * pdf_height),
        )
output.write('output.pdf')
output.close()
