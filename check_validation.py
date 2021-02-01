from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from num2words import num2words
import pytesseract
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
try:
    from PIL import Image
except ImportError:
    import Image

# digit value
x1, y1 = 550, 120
x2, y2 = 680, 175

# handwritten value
x1hw, y1hw = 10, 150
x2hw, y2hw = 520, 190


def check_validation(expected_value, filename):
    img = Image.open(filename)
    img = np.array(img)
    img = cv2.resize(img, (700, 350))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    cropped_img_words = img[y1hw:y2hw, x1hw:x2hw]
    cropped_img_digits = img[y1:y2, x1:x2]

    numb_in_words = num2words(expected_value)
    numb_arr = numb_in_words.split(" ")

    output_words = pytesseract.image_to_string(cropped_img_words)
    word_arr = output_words.split(" ")

    output_digits = pytesseract.image_to_string(cropped_img_digits)

    total_current = 0
    substring = "check"
    if substring in filename.filename:
        for i in range(len(numb_arr)):
            try:
                total_current += (fuzz.WRatio(word_arr[i+1], numb_arr[i]))
            except IndexError:
                total_current = 0
    else:
        for i in range(len(word_arr)):
            try:
                total_current += (fuzz.WRatio(word_arr[i], numb_arr[i]))
            except IndexError:
                total_current = 0

    total = len(numb_arr) * 100
    total_needed = total * .50

    msg = "Failure, check is not valid"
    if total_current >= total_needed:
        msg = "Success! Check is valid"
    return msg
