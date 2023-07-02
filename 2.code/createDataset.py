import cv2
import pandas as pd
import random




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

    data_list = []

    cnt = random.randint(1, 13)
    data_list += medicine(cnt, medicinePath, dbPath)

    cnt = random.randint(1, 13)
    data_list += injection(cnt, medicinePath, dbPath)

    data_list += checkSquared(dbPath)
    print(data_list)





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
            id += j * 13
            mask = position_df['id'] == id
            position.append(position_df[mask][['x1', 'y1']].values)
        

        medi_list.append([medi_name, position[0]])
        amount_list.append([amount, position[1]])
        count_list.append([count, position[2]])
        duration_list.append([duration, position[3]])
       
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
            id += j * 7
            mask = position_df['id'] == id
            position.append(position_df[mask][['x1', 'y1']].values)
        

        injection_list.append([injection_name, position[0]])
        amount_list.append([amount, position[1]])
        count_list.append([count, position[2]])
        duration_list.append([duration, position[3]])
       
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
        checkSquared_list.append(["■", position_df[mask][['x1', 'y1']].values])
        
        # 글자 삽입
        mask = position_df['id'] == 29
        #일단, A
        checkSquared_list.append(["A", position_df[mask][['x1', 'y1']].values])

    else:
        # 체크  
        mask = position_df['id'] == id
        checkSquared_list.append(["■", position_df[mask][['x1', 'y1']].values])
        
    id = random.randint(83,84)
    mask = position_df['id'] == id
    checkSquared_list.append(["■", position_df[mask][['x1', 'y1']].values])

       
    return checkSquared_list





dbPath = r'1.data\3.DB\db.csv'
medicinePath = r'1.data\3.DB\medicine_list.csv'
imgPath = r'1.data\1.img\prescription.png'


CreateDataset(dbPath = dbPath, medicinePath= medicinePath, imgPath = imgPath)