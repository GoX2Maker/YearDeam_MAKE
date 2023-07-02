import cv2
import pandas as pd
import random
from PIL import ImageFont, ImageDraw, Image
import numpy as np


def CreateDataset(dbPath, medicinePath, imgPath, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 15):
    """
    Yolo와 ResNet data set을 만든다.

    Args:
    ---
        `dbPath [string]` : db.csv 경로

        `medicinePath [string]` : medicine_list.csv 경로

        `imgPath [string]` : 처방전 양식 경로

        `moveTxt [int, int]` : 빈칸 고정 위치 이동

        `txtFont [string]` : 글씨체

        `txtSize [int]` : 글자 크기

    Returns:
    ---
       None

    """

    # 처방전 데이터 생성
    data_list = []
    cnt = random.randint(1, 13)
    data_list += medicine(cnt, medicinePath, dbPath)

    cnt = random.randint(1, 13)
    data_list += injection(cnt, medicinePath, dbPath)

    data_list += checkSquared(dbPath)

    # 처방전 이미지 및 Json 생성
    img, img_json  = createImg(data_list, imgPath, moveTxt, txtFont, txtSize)






# 의약품 메서드
def medicine(cnt, dataPath, positionPath):
    # cnt : 1~13
    # dataPath : 의약DB 경로
    # positionPath : 위치DB 경로
    
    medicine_df = pd.read_csv(dataPath)
    position_df = pd.read_csv(positionPath)

    medi_list = []
    amount_list = []
    count_list = []
    duration_list = []


    for i in range(cnt):
        index = random.randint(0, 40000)
        medi_name = medicine_df.iloc[index, 2]

        amount = random.randint(1, 10) # 1회 투약량
        count = random.randint(1, 10) # 1회 투약횟수
        duration =  random.randint(1, 14) # 총 투약일수

        id = 30 + i
        position = []
        for j in range(4):
            id_ = id + j * 13
            mask = position_df['id'] == id_
            position.append(position_df[mask][['x1', 'y1']].values[0])
        

        medi_list.append([medi_name, position[0]])
        amount_list.append([str(amount), position[1]])
        count_list.append([str(count), position[2]])
        duration_list.append([str(duration), position[3]])
       
    return medi_list + amount_list + count_list + duration_list




# 주사 메서드
def injection(cnt, dataPath, positionPath):
    # cnt : 1~7
    # dataPath : 의약DB 경로
    # positionPath : 위치DB 경로

    medicine_df = pd.read_csv(dataPath)
    position_df = pd.read_csv(positionPath)
    

    injection_list = []
    amount_list = []
    count_list = []
    duration_list = []


    for i in range(cnt):
        index = random.randint(0, 40000)
        injection_name = medicine_df.iloc[index, 2]

        amount = random.randint(1, 10) # 1회 투약량
        count = random.randint(1, 10) # 1회 투약횟수
        duration =  random.randint(1, 14) # 총 투약일수

        id = 85 + i
        position = []
        for j in range(4):
            id_ = id + j * 7
            mask = position_df['id'] == id_
            position.append(position_df[mask][['x1', 'y1']].values[0])
        

        injection_list.append([injection_name, position[0]])
        amount_list.append([str(amount), position[1]])
        count_list.append([str(count), position[2]])
        duration_list.append([str(duration), position[3]])
       
    return injection_list + amount_list + count_list + duration_list

# 체크상자 메서드
def checkSquared(positionPath):
    # positionPath : 위치DB 경로
    position_df = pd.read_csv(positionPath)

    checkSquared_list = []
    id = random.randint(24,28)
    
    if id == 28:
        # 체크를 하고 29에 글자 삽입
        mask = position_df['id'] == id
        checkSquared_list.append(["■", position_df[mask][['x1', 'y1']].values[0]])
        
        # 글자 삽입
        mask = position_df['id'] == 29
        #일단, A
        checkSquared_list.append(["A", position_df[mask][['x1', 'y1']].values[0]])

    else:
        # 체크  
        mask = position_df['id'] == id
        checkSquared_list.append(["■", position_df[mask][['x1', 'y1']].values[0]])
        
    id = random.randint(83,84)
    mask = position_df['id'] == id
    checkSquared_list.append(["■", position_df[mask][['x1', 'y1']].values[0]])

       
    return checkSquared_list


def createImg(data, imgPath, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 15):
    """
    처방전 data를 이미지로 제작

    Args:
    ---
        `data [string]` : text위치 및 내용

        `imgPath [string]` : 처방전 양식 경로

        `moveTxt [int, int]` : 빈칸 고정 위치 이동

        `txtFont [string]` : 글씨체

        `txtSize [int]` : 글자 크기

    Returns:
    ---
        `result_img [img]` : 글자가 삽입된 처방전 이미지.

        `result_txt [json]` : 이미지에 있는 글자 위치 및 내용이 담긴 Json 파일

    """

    imgBGR = cv2.imread(imgPath)
    imgRGB = cv2.cvtColor(imgBGR, cv2.COLOR_BGR2RGB)

    font = ImageFont.truetype(txtFont, txtSize)

    # 이미지를 PIL Image 객체로 변환
    img = Image.fromarray(imgRGB)

    # Draw 객체 생성
    draw = ImageDraw.Draw(img)


    text_sizes_list = []
    # 텍스트를 추가하는 for loop    
    for text, position in data:
        # .text(위치, 텍스트, 텍스트 색, 폰트)
        text_width, text_height = draw.textsize(text, font=font)

        position[0] += moveTxt[0]
        position[1] += moveTxt[1]

        x = position[0]  + text_width / 2
        y = position[1]  + text_height / 2
        
        # Calculate the y position to center the text
        draw.text((x, y), text, (0, 0, 0), font=font,anchor='mm')
        
        text_sizes_list.append([position[0], position[1], position[0] + text_width, position[1] + text_height])
        

    # PIL Image를 다시 numpy 배열로 변환
    img_with_text = np.array(img)
    result_img = cv2.cvtColor(img_with_text, cv2.COLOR_RGB2BGR)
    
    #사각형 그리기
    for x1, y1, x2, y2 in text_sizes_list:
        cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 2)


    cv2.imshow('result', result_img)
    cv2.waitKey()
    cv2.destroyAllWindows()
    return result_img




dbPath = r'1.data\3.DB\db.csv'
medicinePath = r'1.data\3.DB\medicine_list.csv'
imgPath = r'1.data\1.img\prescription.png'


CreateDataset(dbPath = dbPath, medicinePath= medicinePath, imgPath = imgPath)