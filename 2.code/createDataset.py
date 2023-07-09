import random
import cv2
import pandas as pd
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import json
from tqdm.auto import tqdm
import time

class DataSet():
    def __init__(self, saveIMGPaht, saveJsonPath, dbPath, medicinePath, labelingPath, imgPath):
        self.saveIMGPaht = saveIMGPaht
        self.saveJsonPath = saveJsonPath
        self.medicine_df = pd.read_csv(medicinePath)
        self.position_df = pd.read_csv(dbPath)
        self.labeling_df = pd.read_csv(labelingPath)
        self.prescription_img = cv2.imread(imgPath)

    def CreateDataset(self, nums, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 10, debug =False):
        """

        Args:
        ---
        `nums [int]` : 생성할 이미지 갯수

        `moveTxt [int, int]` : 빈칸 고정 위치 이동

        `txtFont [string]` : 글씨체

        `txtSize [int]` : 글자 크기

        `debug [bool]` : 디버그용(라인 표시)

        Returns:
        ---
        None

        """
        st = time.time()
        for i in tqdm(range(nums)):
            result_img, result_json  = createImg(data_list, labelingPath, imgPath, moveTxt, txtFont, txtSize, debug)

            if debug:
                cv2.namedWindow("result", cv2.WINDOW_NORMAL)
                cv2.imshow('result', result_img)
                cv2.waitKey()
                cv2.destroyAllWindows()
        
            with open(self.saveJsonPath + rf'\{i}.json', 'w', encoding='utf-8') as file:
                file.write(result_json)
                if debug:
                    print(result_json)
            
            cv2.imwrite(self.saveIMGPaht + rf'\{i}.jpg', result_img)

        et = time.time()
        elapsed_time = et - st
        print(f'Execution time: {elapsed_time:.4f} seconds')

    def createData(self):
        data_list = []
        # 의약품
        data_list += self.createMedicineOrInjection(type=0)
        
        # 주사
        data_list += self.createMedicineOrInjection(type=1)

        # 용법
        id = 82
        index = random.randint(0, 40000)
        namesize = random.randint(4, 20)
        instruction_ = self.medicine_df.iloc[index, 2][:namesize]
        
        mask = self.position_df['id'] == id
        position = self.position_df[mask][['x1', 'y1']].values[0]
        data_list.append([instruction_, position])
        
        # 참고사항
        id = 113
        index = random.randint(0, 40000)
        namesize = random.randint(4, 20)
        note = self.medicine_df.iloc[index, 2][:namesize]
        
        mask = self.position_df['id'] == id
        position = self.position_df[mask][['x1', 'y1']].values[0]
        data_list.append([note, position])


        id = random.randint(24,28)
        if id == 28:
            # 체크를 하고 29에 글자 삽입
            mask = self.position_df['id'] == id
            data_list.append(["■", self.position_df[mask][['x1', 'y1']].values[0]])
            
            # 글자 삽입
            mask = self.position_df['id'] == 29
            #일단, A
            data_list.append(["A", self.position_df[mask][['x1', 'y1']].values[0]])

        else:
            # 체크  
            mask = self.position_df['id'] == id
            data_list.append(["■", self.position_df[mask][['x1', 'y1']].values[0]])
            
        id = random.randint(83,84)
        mask = self.position_df['id'] == id
        data_list.append(["■", self.position_df[mask][['x1', 'y1']].values[0]])

    
    def createMedicineOrInjection(self, type):
        """
        Args:
        ---
        `type [int]` : 0 = 의약품, 1 = 주사

        Returns:
        ---
        
        data_list

        """
        maxCNT = 10
        setid = 30
        sumid = 13

        # 주사 세팅
        if type == 1:
            maxCNT = 13
            setid = 85
            sumid = 7

        data_list = []
        cnt = random.randint(1, maxCNT)
        for i in range(cnt):
            index = random.randint(0, 40000) 
            namesize = random.randint(4, 20)
            medi_name = self.medicine_df.iloc[index, 2][:namesize]

            amount = random.randint(1, 10) # 1회 투약량
            count = random.randint(1, 10) # 1회 투약횟수
            duration =  random.randint(1, 14) # 총 투약일수

            id = setid + i
            position = []
            for j in range(4):
                id_ = id + j * sumid
                mask = self.position_df['id'] == id_
                position.append(self.position_df[mask][['x1', 'y1']].values[0])
            

            data_list.append([medi_name, position[0]])
            data_list.append([str(amount), position[1]])
            data_list.append([str(count), position[2]])
            data_list.append([str(duration), position[3]])

        return data_list




