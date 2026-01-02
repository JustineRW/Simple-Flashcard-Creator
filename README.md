This code makes simple flashcards from a `database.csv`, gives each flashcard a front and back image, and provides a pdf output with three cards per A4 page, ready for double-sided printing. The pdf is designed to be printed with the 'flip on short edge' printing option, and should allow you to simply print the pdf and cut out the flashcards (front and backs should align). The images on the back of the cards are semi-transparent and the cards have rounded corners. The code also provides a references.pdf which lists text, front image and back image references, and a one card per page pdf.

This was a fun personal project using [borb](https://github.com/borb-pdf), a simple pdf creator. I originally wanted some botanical flashcards, so the example database and a number of the `flashcard_creator.py` functions are set up specifically for botanical data (e.g., they include column headers like 'genus'). You could modify this to make whatever kinds of flashcards you needed :).

The code handles up to three flashcards per A4 page. More than three flashcards per page and you'll need to adjust the sizes in the `pdf_transformer.pdf` file.

<h2>Set-up instructions</h2>

1. In the terminal, run  `pip install -r requirements.txt`
2. Add your data to the database.csv file, following the named columns. Please refer to the example database.
3. Add all named image files to the `/originals` folder. Make sure the names for these files match the names you've indicated for the front and back images in the database 
4. Run `main.py`. This will take a few moments.
5. Flashcards will be provided in a 'final flashcard file' pdf in the `/output` folder. References will be provided in the `references.pdf`. Please note that the reference code is very simple and doesn't follow any specific reference guidelines.

<h3>Acknowledgements</h3>
Thanks to [borb](https://github.com/borb-pdf), for providing a simple pdf creator with [great documentation](https://github.com/borb-pdf/borb-examples/tree/master/01). And a big thanks to the Biodiversity Heritage Library for the digitised books used to create the example database (note references for individual books and images are recorded in the example database).
<!-- Add ack for the fonts -->