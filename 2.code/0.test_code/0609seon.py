from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import pandas as pd

def input_pre2(csvPath, imgPath, moveTxt, txtFont = "NanumSquareOTF_acR", txtSize = 15):
    
    """prescription2 정보처리
    prescription2.csv에 있는 빈칸 고정 위치 데이터가 moveTxt에 의해 이동된다.
    txtFont와 txtSize도 설정값에 맞게 설정된다.
    ==
    Args:
    ---
        `csvPath [string]` : prescription2.csv 경로

        `imgPath [string]` : 처방전 양식 경로

        `moveTxt [int, int]` : 빈칸 고정 위치 이동

        `txtFont [string]` : 글씨체

        `txtSize [int]` : 글자 크기

    Returns:
    ---
        `result_text_position [array]` : moveTxt에 의해 이동된 글자의 위치

        `result_img [img]` : 글자가 삽입된 처방전 이미지.

    """
    
    imgBGR = cv2.imread(imgPath)
    imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)

    font = ImageFont.truetype(txtFont, txtSize)
    
    # 이미지를 PIL Image 객체로 변환    
    img = Image.fromarray(imgRGB)
    
    # Draw 객체 생성
    draw = ImageDraw.Draw(img)
    
    # 'id', 'x1', 'y1', 'y2' 컬럼의 값을 이용해서 텍스트와 좌표값을 가진 딕셔너리 생성
    text_dict = {str(row['id']): (row['x1'] + moveTxt[0], row['y1'] + moveTxt[1]) for _, row in df.iterrows()}
    
    # 텍스트를 추가하는 for loop
    for text, position in text_dict.items():
        # .text(위치, 텍스트, 텍스트 색, 폰트)
        draw.text(position, text, (0, 0, 0), font=font)

    # PIL Image를 다시 numpy 배열로 변환
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
