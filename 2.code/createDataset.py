import cv2
import pandas as pd
import random
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import json


def CreateDataset(dbPath, medicinePath, labelingPath, imgPath, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 10, debug =False):
    """
    Yolo와 ResNet data set을 만든다.

    Args:
    ---
        `dbPath [string]` : db.csv 경로

        `medicinePath [string]` : medicine_list.csv 경로

        `labelingPath [string]` : prescript_labeling.csv 경로

        `imgPath [string]` : 처방전 양식 경로

        `moveTxt [int, int]` : 빈칸 고정 위치 이동

        `txtFont [string]` : 글씨체

        `txtSize [int]` : 글자 크기

        `debug [bool]` : 디버그용(라인 표시)

    Returns:
    ---
       None

    """

    # 처방전 데이터 생성
    data_list = []
    medicineCNT = random.randint(1, 13)
    data_list += medicine(medicineCNT, medicinePath, dbPath)

    injectionCNT = random.randint(1, 7)
    data_list += injection(injectionCNT, medicinePath, dbPath)
    
    instructionCNT = random.randint(1, 7)
    data_list += instruction(instructionCNT, medicinePath, dbPath)

    data_list += checkSquared(dbPath)

    # 처방전 이미지 및 Json 생성
    result_img, result_json  = createImg(data_list, labelingPath, imgPath, moveTxt, txtFont, txtSize, debug)

    if debug:
        print(result_json)
        cv2.namedWindow("result", cv2.WINDOW_NORMAL)
        cv2.imshow('result', result_img)
        cv2.waitKey()
        cv2.destroyAllWindows()
        



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
        
        namesize = random.randint(20, 25)
        medi_name = medicine_df.iloc[index, 2][:namesize]

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
        namesize = random.randint(20, 25)
        injection_name = medicine_df.iloc[index, 2][:namesize]


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


def instruction(cnt,  dataPath, positionPath):
    medicine_df = pd.read_csv(dataPath)
    position_df = pd.read_csv(positionPath)
    

    instruction_list = []

    
    # 용법
    id = 82
    index = random.randint(0, 40000)
    namesize = random.randint(4, 20)
    instruction_ = medicine_df.iloc[index, 2][:namesize]
    
    mask = position_df['id'] == id
    position = position_df[mask][['x1', 'y1']].values[0]
    instruction_list.append([instruction_, position])
    
    # 참고사항
    id = 113
    index = random.randint(0, 40000)
    namesize = random.randint(4, 20)
    note = medicine_df.iloc[index, 2][:namesize]
    
    mask = position_df['id'] == id
    position = position_df[mask][['x1', 'y1']].values[0]
    instruction_list.append([note, position])


   
    return instruction_list
    
    
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


def createImg(data, labelingPath, imgPath, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 15, debug=False):
    """
    처방전 data를 이미지로 제작

    Args:
    ---
        `data [string]` : text위치 및 내용

        `labelingPath [string]` : prescript_labeling.csv 경로

        `imgPath [string]` : 처방전 양식 경로

        `moveTxt [int, int]` : 빈칸 고정 위치 이동

        `txtFont [string]` : 글씨체

        `txtSize [int]` : 글자 크기

        `debug [bool]` : 디버그용(라인 표시)

    Returns:
    ---
        `result_img [img]` : 글자가 삽입된 처방전 이미지.

        `result_json [json]` : 이미지에 있는 글자 위치 및 내용이 담긴 Json 파일

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

        position[0] += moveTxt[0] + 10
        position[1] += moveTxt[1]

        x = position[0]  + text_width / 2
        y = position[1]  + text_height / 2
        
        # Calculate the y position to center the text
        draw.text((x, y), text, (0, 0, 0), font=font,anchor='mm')
        
        text_sizes_list.append([position[0], position[1], position[0] + text_width, position[1] + text_height, text])
        

    # PIL Image를 다시 numpy 배열로 변환
    img_with_text = np.array(img)
    result_img = cv2.cvtColor(img_with_text, cv2.COLOR_RGB2BGR)
    
    #사각형 그리기
    if debug:
        for x1, y1, x2, y2, txt in text_sizes_list:
            cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 1)



    # 처방전 라벨링 사각형 그리기

    df = pd.read_json(labelingPath)

    # 'id', 'x1', 'y1', 'y2' 컬럼의 값을 이용해서 텍스트와 좌표값을 가진 딕셔너리 생성
    position_list = [[row['id'], row['x1'] + moveTxt[0], row['y1'] + moveTxt[1] ,row['x2'] + moveTxt[0] , row['y2'] + moveTxt[1], row['cont']] for _, row in df.iterrows()]

    
    #사각형 그리기
    if debug:
        for id, x1, y1, x2, y2, txt in position_list:
            cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 1)
            text_sizes_list.append([x1, y1, x2, y2,txt])

    # Json 파일 만들기
    text_sizes_dics = []
    for x1, y1, x2, y2, txt in text_sizes_list:
        text_sizes_dics.append({'x1' : int(x1), 'y1' : int(y1), 'x2' : int(x2), 'y2' : int(y2), 'txt' : str(txt)})
        

    result_json = json.dumps(text_sizes_dics, ensure_ascii=False , indent=4)


    return result_img, result_json




dbPath = r'1.data\3.DB\db.csv'
medicinePath = r'1.data\3.DB\medicine_list.csv'
labelingPath = r'1.data\3.DB\prescript_labeling(Fix).json'
imgPath = r'1.data\1.img\prescription.png'
debug = True

CreateDataset(dbPath = dbPath, medicinePath= medicinePath, labelingPath = labelingPath, imgPath = imgPath, debug = debug)