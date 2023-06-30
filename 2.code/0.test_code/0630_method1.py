# 30~42: 의약품 명칭(db에서 가져오기)
# 85~91: 주사제 명칭(의약품db에서 가져오기)
# 43~81: 투약 횟수(난수로 생성)
# 82, 113: 용법, 참고사항(아무 문자나)

# 입력 : 의약품 갯수, 주사제 갯수
# 출력 : 

import cv2
import pandas as pd
import random

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
       
    return medi_list, amount_list, count_list, duration_list




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
       
    return injection_list, amount_list, count_list, duration_list



cnt, dataPath, positionPath = 4, r'1.data/3.DB/medicine_list.csv' , r'1.data/3.DB/db.csv'

medi_list, amount_list, count_list, duration_list = medicine(cnt, dataPath, positionPath)

print(medi_list)
print()
print(amount_list)
print()
print(count_list)
print()
print(duration_list)