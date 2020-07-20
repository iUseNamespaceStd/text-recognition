try:
    from PIL import Image
except:
    import Image
import pytesseract

#path to tesseract-ocr engine
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr(filename):
    #convert image to string
    text = pytesseract.image_to_string(Image.open(filename))
    return text

print(ocr('static/test.png'))