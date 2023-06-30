import cv2
import pandas as pd
import random

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

       
    return checkSquared_list, id

cnt, dataPath, positionPath = 4, r'1.data/3.DB/medicine_list.csv' , r'1.data/3.DB/db.csv'

for i in range(20):
    list_, id = checkSquared(positionPath)
    print(f"\n==================\n id : {id}\n, list_ : {list_}  \n==================\n")
