#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-*-encoding:utf-8-*-
import pytesseract
from PIL import Image

image = Image.open("a.png")
text = pytesseract.image_to_string(image, lang='chi_sim')
print(text)