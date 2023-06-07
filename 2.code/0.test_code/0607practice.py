from PIL import ImageFont, ImageDraw, Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import pandas as pd

imgBGR = cv2.imread(r'YearDeam_MAKE/1.data/1.img/prescription.png')
imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)

font = ImageFont.truetype('malgun.ttf', 15)

# 이미지를 PIL Image 객체로 변환
img = Image.fromarray(imgRGB)

# Draw 객체 생성
draw = ImageDraw.Draw(img)

# csv 파일 로드
df = pd.read_csv(r'YearDeam_MAKE/1.data/2.documents/prescription1.csv')

# 'id', 'x1', 'y1', 'y2' 컬럼의 값을 이용해서 텍스트와 좌표값을 가진 딕셔너리 생성
text_dict = {str(row['id']): (row['x1'] + 7.5, row['y1'] -2.5) for _, row in df.iterrows()}

# 텍스트를 추가하는 for loop
for text, position in text_dict.items():
    # .text(위치, 텍스트, 텍스트 색, 폰트)
    draw.text(position, text, (0, 0, 0), font=font)

# PIL Image를 다시 numpy 배열로 변환
img_with_text = np.array(img)

# 텍스트가 추가된 이미지 출력
cv2.imshow('img', cv2.cvtColor(img_with_text, cv2.COLOR_RGB2BGR))
cv2.waitKey()
cv2.destroyAllWindows()