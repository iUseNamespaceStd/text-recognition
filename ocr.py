from cv2 import cv2
import numpy as np
import pytesseract

#path to tesseract-ocr engine
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#read the image
img = cv2.imread("lorem.png")

#convert image to string
text = pytesseract.image_to_string(img)
print(text)

#display the image
cv2.imshow("image", img)