# Requirements: 
* Install Tesseract-ocr engine from there: https://github.com/UB-Mannheim/tesseract/wiki
* Python 3.5 or above
* Flask
* MySQL

## How to use?
Follow these steps:
1. Set the appropriate path for the location of Tesseract-OCR engine(tesseract.exe) inside the "ocr.py" script(path in script is the default path).
1. Install packages using pip
1. The format used inside the "customer_template.docx" file should remain the same unless you plan on changing the regex used inside the "app.py" file to a custom one. I recommend that you check out the regex first to learn about the appropriate format before filling in the cutomer_template.
1. To run the app, simply type "python app.py" inside the terminal.



