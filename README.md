This code makes simple flashcards from a `database.csv`, gives each flashcard a front and back image and provides a pdf output with three cards per A4 page, ready for double-sided printing. The pdf is designed to be printed with the 'flip on short edge' printing option. The resulting pdf can be printed and the flashcards cut out (front and backs should align). The images on the back of the cards are semi-transparent and the cards have rounded corners. The code also provides a references.pdf which lists text, front image and back image references, and a 'one card per page' pdf in case you want to print individual cards separately.

This was a fun personal project using [borb](https://github.com/borb-pdf), a simple pdf creator. I originally wanted some botanical flashcards, so the example database and a number of the `flashcard_creator.py` functions are set up specifically for botanical data (e.g., they include column headers like 'genus'). You could modify the flashcard creator to make whatever kinds of flashcards you needed :). Refer to the borb documentation for examples of working with borb (https://github.com/borb-pdf/borb-examples/tree/master/01).

The code handles up to three flashcards per A4 page. More than three flashcards per page and you'll need to adjust the sizes in the `pdf_transformer.pdf` file.

<h2>Set-up instructions</h2>

1. In the terminal, run  `pip install -r requirements.txt`
2. Add your data to a database.csv file, following the named columns in the example database. Please refer to the example database - note that this repo is currently set up for botanical (plant) flashcards, so you'll find columns like 'genus' and 'species'. If you make changes to the columns, please make sure to update the corresponding references in the flashcard creator module.
3. Add all named image files to the `/originals` folder. Make sure the names for these files match the names you've indicated for the front and back images in the database.
4. Update all references to `example_database.csv` to your database.csv name.
5. Run `main.py`. This will take a few moments. The terminal will print logs.
6. Flashcards will be provided in a 'final flashcard file' pdf in the `/output` folder. References will be provided in the `references.pdf`. Please note that the reference code is very simple and doesn't follow any specific reference guidelines.

<h2>Examples</h2>
Run main to see example output (will be placed in the output folder). All examples use public domain images and data. The Source Serif 4 font has an open licence (please refer to https://fonts.google.com/specimen/Source+Serif+4/license).

<h2>Troubleshooting</h2>

If you encounter any unexpected errors on pdf creation, this can be due to unusual characters in your data. You'll notice that the text helper module contains a clean_text function that strips out ‘ (single quote) characters and replaces them with ' (apostrophe/single quote). The ‘ character was causing odd pdf wrapping failures.

I've also had trouble with using some Google Fonts as borb's TrueTypeFont object. There's an issue with spacing and the text overlays itself (you can see an example of this in the borb documentation, where the Lobster font isn't working correctly: https://github.com/borb-pdf/borb-examples/tree/c0ec5f61e5260b04e0c03abec2fc1ce28b701e0a/02#212-loading-a-font-from-a-ttf-file). I'm not sure why that is. Source Serif 4 appears to work correctly, but this is something to keep an eye out for if you change fonts.


<h2>Acknowledgements</h2>
<ul>
    <li>borb (https://github.com/borb-pdf), a simple pdf creator with good documentation (https://github.com/borb-pdf/borb-examples/tree/master/01).</li>
    <li>The Biodiversity Heritage Library (https://www.biodiversitylibrary.org/) for the public domain digitised books used to create the example database (note references for individual books and images are recorded in the example database).</li>
    <li>Google Fonts, Source Serif 4 (https://fonts.google.com/specimen/Source+Serif+4)></li>
</ul>