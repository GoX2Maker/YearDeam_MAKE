from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import pandas as pd


def input_pre2(csvPath, imgPath, moveTxt, txtFont = "NanumSquareOTF_acR", txtSize = 15):
    
    imgBGR = cv2.imread(imgPath)
    imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)

    font = ImageFont.truetype(txtFont, txtSize)

    img = Image.fromarray(imgRGB)

    draw = ImageDraw.Draw(img)

    text_dict = {str(row['id']): (row['x1'] + moveTxt[0], row['y1'] + moveTxt[1]) for _, row in df.iterrows()}

    for text, position in text_dict.items():
        draw.text(position, text, (0, 0, 0), font=font)

    img_with_text = np.array(img)
    result_img2 = cv2.cvtColor(img_with_text, cv2.COLOR_RGB2BGR)

    return text_dict, result_img2


csvPath = r'1.data/3.DB/prescript_labeling2.csv'
imgPath = r'1.data/1.img/prescription.png'
moveTxt = [0, 0]
txtFont = 'NanumSquareOTF_acR'

df = pd.read_csv(csvPath)

text_dict, result_img2 = input_pre2(csvPath, imgPath, moveTxt)
cv2.imshow('result', result_img2)
cv2.waitKey()
cv2.destroyAllWindows()
