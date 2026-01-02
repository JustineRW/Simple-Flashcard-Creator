from pypdf import PdfReader, PdfWriter, Transformation
import datetime

def transform_pdf_into_multiple_pages(pagesPerPage : int, fullOutputFilePath : str):
    print(f"Reading the one card per page pdf file.")
    pdf_source = PdfReader(fullOutputFilePath)
    numberOfPagesInSource = len(pdf_source.pages)
    print(f"There are {numberOfPagesInSource} pages in the one card per page pdf file.")

    if numberOfPagesInSource % 2 > 0:
        print("Flashcard front and back numbers don't match. Please check the source pdf. There should be an even number of pages (providing fronts and backs for the flashcards)")
        return 
    
    pagesToAddToOnePageOfOutput = pagesPerPage
    dividedA4: int = int((842/pagesToAddToOnePageOfOutput))
    pdf_width = dividedA4
    pdf_height = 595

    totalFrontsAndBacksForPagePair = pagesToAddToOnePageOfOutput * 2
    
    # we need to make sure the number of pages in the source pdf are divisible by the number of desired pages per page in our resulting pdf
    numberOfPagesInSourceWithPadding = numberOfPagesInSource
    if numberOfPagesInSourceWithPadding % pagesPerPage > 0:
        while numberOfPagesInSourceWithPadding % pagesPerPage > 0:
            numberOfPagesInSourceWithPadding += 1

    output = PdfWriter()
    outputPageIndex = 0

    print(f"Creating the {pagesPerPage} cards per A4 page pdf file.")
    
    # Put flashcard fronts on one page, and the matching backs on the other page in REVERSE order. This allows double-sided printing by printing with the 'flip on the short side' option
    # Step by the totalFrontsAndBacksForPagePair number (i += totalFrontsAndBacksForPagePair on each loop)
    for i in range(0, numberOfPagesInSource, totalFrontsAndBacksForPagePair): 
        output.add_blank_page(pdf_width * pagesToAddToOnePageOfOutput, pdf_height)
        output.add_blank_page(pdf_width * pagesToAddToOnePageOfOutput, pdf_height)

        for j in range(totalFrontsAndBacksForPagePair):
            if i+j >= numberOfPagesInSource:
                print("Adding a blank space as there aren't sufficient cards to fill all pages.")
            else:
                page = pdf_source.pages[i+j]
                if (i+j) % 2 == 0:
                # back images - reversed order from original source pdf to allow double sided printing
                    output.pages[outputPageIndex + 1].merge_transformed_page(page, Transformation().translate((-1*(j-(totalFrontsAndBacksForPagePair - 2))/2) * pdf_width, 0)) 
                else:
                # front images
                    output.pages[outputPageIndex].merge_transformed_page(page, Transformation().translate(((j/2) - 0.5) * pdf_width, 0))

        outputPageIndex += 2

    final_filepath = "output/final_flashcard_file" + "_" + datetime.datetime.now().strftime("%H%M%S") + ".pdf"
    print(f"Writing the {pagesPerPage} cards per A4 page pdf file to '{final_filepath}'.")
    output.write(final_filepath)
    output.close()

if __name__ == "__main__":
    transform_pdf_into_multiple_pages(3, "output\\[add file name here]")

