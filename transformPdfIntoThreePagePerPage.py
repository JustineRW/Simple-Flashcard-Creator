from pypdf import PdfReader, PdfWriter, Transformation

# TODO need to refer back to original code for making new pages, or add in a skip for every three pages
thirdA4: int = int((842/3))
pdf_width = thirdA4
pdf_height = 595

pdf_source = PdfReader("flashcards.pdf")
numberOfPagesInSource = len(pdf_source.pages)
numberOfPagesToAddToOnePageOfOutput = 3
output = PdfWriter()

output.add_blank_page(pdf_width * numberOfPagesToAddToOnePageOfOutput, pdf_height)
outputPageIndex = 0

for i in range(numberOfPagesInSource - numberOfPagesToAddToOnePageOfOutput):
    for j in range(numberOfPagesToAddToOnePageOfOutput):
        page = pdf_source.pages[i+j]
        output.pages[outputPageIndex].merge_transformed_page(page, Transformation().translate(j * pdf_width, 0))
    outputPageIndex += 1
    output.add_blank_page(pdf_width * numberOfPagesToAddToOnePageOfOutput, pdf_height)
    i += 3

    
output.write('finalFlashcardFileWithMultiplePagesPerPage.pdf')
output.close()
