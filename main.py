#! /usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import pytesseract
import cv2
import glob
import time


def prepro(src, bin_thresh):
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    a, dst = cv2.threshold(src, bin_thresh, 255, cv2.THRESH_BINARY)
    dst = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 20)
    return dst


def ocr(im):
    im.load()
    return pytesseract.image_to_string(im).strip()


# search in all JPG files for school bus image
def search(jpg, imgname):
    start_time = time.clock()
    for i in range(45, 90, 10):
        print "bin_thresh=", i
        dst = prepro(jpg, i)
        dst = Image.fromarray(dst)
        cv2.waitKey()
        word = ocr(dst)
        if 'School' in word or 'Bus' in word:
            print 'Image', imgname, 'is a school bus'
            print time.clock() - start_time, "seconds"
            break

# list all jpg files in the folder
filelist = glob.glob("*.j")

for i in filelist:
    img = cv2.imread(i)
    search(img, i)
