from pypdf import PdfReader, PdfWriter, Transformation
import datetime

def transformPdfIntoMultiplePages(pagesPerPage : int, fullOutputFilePath : str):
    pagesToAddToOnePageOfOutput = pagesPerPage
    dividedA4: int = int((842/pagesToAddToOnePageOfOutput))
    pdf_width = dividedA4
    pdf_height = 595

    pdf_source = PdfReader(fullOutputFilePath)
    numberOfPagesInSource = len(pdf_source.pages)
    cardFrontAndBackCount = pagesToAddToOnePageOfOutput * 2
    output = PdfWriter()
    numberOfPagesInOutput = int(numberOfPagesInSource / cardFrontAndBackCount)
    outputPageIndex = 0

# TODO improve error handling - just add blanks if there aren't enough cards
    if numberOfPagesInSource % 2 > 0:
        print("Flashcard front and back numbers don't match. Please check the source pdf.")
    # print("Not enough cards to distribute correctly on the page")
    else:
    # Put flashcard fronts on one page, and the matching backs on the other page in REVERSE order. 
    # This allows double-sided printing by printing with the 'flip on the short side' option
    # Step by the cardFrontAndBack number (i += cardFrontAndBackCount on each loop)
        for i in range(0, numberOfPagesInSource, cardFrontAndBackCount): 
            output.add_blank_page(pdf_width * pagesToAddToOnePageOfOutput, pdf_height)
            output.add_blank_page(pdf_width * pagesToAddToOnePageOfOutput, pdf_height)

            for j in range(cardFrontAndBackCount):
                page = pdf_source.pages[i+j]
                if (i+j) % 2 == 0:
                # back images - reversed order from original source pdf to allow double sided printing
                    output.pages[outputPageIndex + 1].merge_transformed_page(page, Transformation().translate((-1*(j-(cardFrontAndBackCount - 2))/2) * pdf_width, 0)) 
                else:
                # front images
                    output.pages[outputPageIndex].merge_transformed_page(page, Transformation().translate(((j/2) - 0.5) * pdf_width, 0))

            outputPageIndex += 2

        output.write("output/finalFlashcardFile" + datetime.datetime.now().strftime("%H%M%S") + ".pdf")
        output.close()

if __name__ == "__main__":
    transformPdfIntoMultiplePages(3, "output\\flashcards.pdf")

