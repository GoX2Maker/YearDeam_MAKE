from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import pandas as pd


## 입력: csv 파일, 처방전 양식 png, 글자 이동, 글꼴, 글자크기
## 처리: 글자가 있는 곳 박스처리
## 출력: 글자 위치, 처방전 결과 img

def input_labeling(csvPath, imgPath, moveTxt, txtFont = "malgun.ttf", txtSize = 15):
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

    # csv 파일 로드
    df = pd.read_csv(csvPath)

    # 'id', 'x1', 'y1', 'y2' 컬럼의 값을 이용해서 텍스트와 좌표값을 가진 딕셔너리 생성
    position_list = [[row['id'], row['x1'] + moveTxt[0], row['y1'] + moveTxt[1] ,row['x2'] + moveTxt[0] , row['y2'] + moveTxt[1]] for _, row in df.iterrows()]

   
   
    
    #사각형 그리기
    for id, x1, y1, x2, y2 in position_list:
        cv2.rectangle(imgBGR, (x1, y1), (x2, y2), (0, 255, 0), 1)
        

    return imgBGR


csvPath = r'1.data\3.DB\prescript_labeling.csv'
imgPath = r'1.data\1.img\prescription.png'
moveTxt = [0, 0]
# txtFont = "malgun.ttf"
# txtSize = 15

result_img = input_labeling(csvPath, imgPath, moveTxt)

cv2.namedWindow("result", cv2.WINDOW_NORMAL)
cv2.imshow('result', result_img)
cv2.waitKey()
cv2.destroyAllWindows()
