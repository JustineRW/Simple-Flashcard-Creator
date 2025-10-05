from pypdf import PdfReader, PdfWriter, Transformation

pagesToAddToOnePageOfOutput = 3
dividedA4: int = int((842/pagesToAddToOnePageOfOutput))
pdf_width = dividedA4
pdf_height = 595

pdf_source = PdfReader("flashcards.pdf")
numberOfPagesInSource = len(pdf_source.pages)
cardFrontAndBackCount = pagesToAddToOnePageOfOutput * 2
output = PdfWriter()
outputPageIndex = 0

# Put flashcard fronts on one page, and the matching backs on the other page in REVERSE order. 
# This allows double-sided printing by printing with the 'flip on the short side' option
for i in range(numberOfPagesInSource - (cardFrontAndBackCount - 1)):

    output.add_blank_page(pdf_width * pagesToAddToOnePageOfOutput, pdf_height)
    output.add_blank_page(pdf_width * pagesToAddToOnePageOfOutput, pdf_height)

    for j in range(cardFrontAndBackCount):
        page = pdf_source.pages[i+j]
        if (i+j) % 2 == 0:
            # reversed order from original source pdf
            output.pages[outputPageIndex + 1].merge_transformed_page(page, Transformation().translate((-1*(j-(cardFrontAndBackCount - 1))/2) * pdf_width, 0)) 
        else:
            output.pages[outputPageIndex].merge_transformed_page(page, Transformation().translate((j/2) * pdf_width, 0))

    outputPageIndex += 2
    i += cardFrontAndBackCount

if numberOfPagesInSource - (cardFrontAndBackCount - 1) > 0:   
    output.write('finalFlashcardFileWithMultiplePagesPerPage.pdf')
    output.close()
else:
    print("Flashcard front and back numbers don't match. Please check the source pdf.")
