from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import pandas as pd


## 입력: 1~29번까지의 처방전1 csv 파일, 처방전 양식 png, 글자 이동, 글꼴, 글자크기 [V]
## 처리?
## 출력: 글자 위치, 처방전 결과 img

def input_pre1(csvPath, imgPath, moveTxt, txtFont = "malgun.ttf", txtSize = 15):
    """prescription1 정보처리
    prescription1.csv에 있는 빈칸 고정 위치 데이터가 moveTxt에 의해 이동된다.
    txtFont와 txtSize도 설정값에 맞게 설정된다.
    ==
    Args:
    ---
        `csvPath [string]` : prescription1.csv 경로

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

    # csv 파일 로드
    df = pd.read_csv(csvPath)

    # 'id', 'x1', 'y1', 'y2' 컬럼의 값을 이용해서 텍스트와 좌표값을 가진 딕셔너리 생성
    text_dict = {str(row['id']): (row['x1'] + 7.5 + moveTxt[0], row['y1'] -2.5 + moveTxt[1]) for _, row in df.iterrows()}

    # 텍스트를 추가하는 for loop
    for text, position in text_dict.items():
        # .text(위치, 텍스트, 텍스트 색, 폰트)
        draw.text(position, text, (0, 0, 0), font=font)

    # PIL Image를 다시 numpy 배열로 변환
    img_with_text = np.array(img)
    result_img = cv2.cvtColor(img_with_text, cv2.COLOR_RGB2BGR)

    return text_dict, result_img


csvPath = r'1.data/3.DB/prescription1.csv'
imgPath = r'1.data/1.img/prescription.png'
moveTxt = [10, 10]
# txtFont = "malgun.ttf"
# txtSize = 15

text_dict, result_img = input_pre1(csvPath, imgPath, moveTxt)
print(text_dict)
cv2.imshow('result', result_img)
cv2.waitKey()
cv2.destroyAllWindows()
