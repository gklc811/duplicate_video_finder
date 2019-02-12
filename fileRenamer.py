import cv2
import imagehash
from PIL import Image
import os
from sqlitedict import SqliteDict
import sqlite3
import time
from PIL import Image
import operator

input_vid_dir = r'F:\demodata\\'
output_vid_dir = r'F:\data\\'

files = next(os.walk(input_vid_dir))[2]
for filename in files:
    newfilename = filename.replace("(", "").replace("[", "").replace("]", "").replace(" ", "").replace(",", "").replace(
        "'",
        "").replace(
        "-", "").replace("_", "").replace(")", "").replace("..", "").replace("&", "").replace("!", "").replace("%",
                                                                                                               "").replace(
        "(", "").replace("}", "").replace("#", "")
    if (os.path.isfile(output_vid_dir + newfilename)):
        os.rename(input_vid_dir + filename, output_vid_dir + "new." + newfilename)
    else:
        os.rename(input_vid_dir + filename, output_vid_dir + newfilename)
