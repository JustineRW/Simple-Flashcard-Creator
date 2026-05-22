### Overview ###

This code makes simple flashcards, and provides a pdf ready for double-sided printing. The repo contains a small example database that produces four botanical (plant) flashcards.

The code uses data from a `database.csv`, gives each flashcard a front and back image and provides a pdf output with three cards per A4 page, ready for double-sided printing. The pdf is designed to be printed with the **'flip on short edge'** printing option. The resulting pdf can be printed and the flashcards cut out. The images on the back of the cards are semi-transparent and the cards have rounded corners. The code also provides a `references.pdf` which lists text, front image, text and back image references, and a 'one card per page' pdf in case you want to print individual cards separately.

This was a fun personal project using [borb](https://github.com/borb-pdf), a simple pdf creator. I originally wanted some botanical flashcards, so the example database and a number of the `flashcard_creator.py` functions are set up specifically for botanical data (e.g., they include column headers like 'genus'). You could modify the flashcard creator to make whatever kinds of flashcards you needed :). Refer to the borb documentation for examples of working with borb (https://github.com/borb-pdf/borb-examples/tree/master/01).

<img width="1519" height="568" alt="image" src="https://github.com/user-attachments/assets/2e3c12a3-9515-45c9-812d-fa7b16378c3c" />
(Example pdf, with three flashcards per page. This .pdf can be printed with the 'flip on short side' printing option. The fronts and backs of the cards align.)

The code handles up to three flashcards per A4 page. More than three flashcards per page and you'll need to adjust the sizes in the `pdf_transformer.pdf` file.

<h2>Set-up instructions</h2>

1. Create a python virtual environment (e.g `python -m venv path/to/this/project`)
2. In the terminal, run  `pip install -r requirements.txt`
3. Create a `database.csv` file. Add your data to this file. Please refer to the `example_database.csv` for appropriate column names. Note that this repo is currently set up for botanical (plant) flashcards, so you'll find columns like 'genus' and 'species'. When you make changes to the column names, make sure to update the corresponding references in the `flashcard_creator.py` module.
4. Add all named image files to the `/originals` folder. Make sure the names for these files match the names you've indicated for the front and back images in the database.
5. Update all references to `example_database.csv` to your database.csv name.
6. Run `main.py`. This will take a few moments. The terminal will print logs.
7. Flashcards will be provided in a 'final flashcard file' pdf in the `/output` folder. References will be provided in the `references.pdf`. Please note that the reference code is very simple and doesn't follow any specific reference guidelines.

<h2>Examples</h2>
Run main to see example output (will be placed in the output folder). All examples use public domain images and data. The Source Serif 4 font has an open licence (please refer to https://fonts.google.com/specimen/Source+Serif+4/license).

<h2>Troubleshooting</h2>

If you encounter any unexpected errors on pdf creation, this can be due to unusual characters in your data. You'll notice that the `text_helper.py` module contains a clean_text function that strips out ‘ (single quote) characters and replaces them with ' (apostrophe/single quote). The ‘ character was causing odd pdf wrapping failures.

I've also had trouble with using some Google Fonts as borb's TrueTypeFont object. There's an issue with spacing and the text overlays itself (you can see an example of this in the borb documentation, where the Lobster font isn't working correctly: https://github.com/borb-pdf/borb-examples/tree/c0ec5f61e5260b04e0c03abec2fc1ce28b701e0a/02#212-loading-a-font-from-a-ttf-file). I'm not sure why that is. Source Serif 4 appears to work correctly, but this is something to keep an eye out for if you change fonts.


<h2>Acknowledgements</h2>
<ul>
    <li>borb (https://github.com/borb-pdf), a simple pdf creator with good documentation (https://github.com/borb-pdf/borb-examples/tree/master/01).</li>
    <li>The Biodiversity Heritage Library (https://www.biodiversitylibrary.org/) for the public domain digitised books used to create the example database (note references for individual books and images are recorded in the example database).</li>
    <li>Google Fonts, Source Serif 4 (https://fonts.google.com/specimen/Source+Serif+4)></li>
</ul>