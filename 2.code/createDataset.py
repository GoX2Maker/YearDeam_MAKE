 # -*- coding: utf-8 -*-
import random
import cv2
import pandas as pd
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import json
from tqdm.auto import tqdm
import time
import os
import shutil
import re
import glob
from natsort import natsorted

class DataSet():
    def __init__(self, saveIMGPath, saveJsonPath,savepathConvertIMG_Resnet, savepathConvertLBL_Resnet,dbPath, medicinePath, labelingPath, imgPath):
        self.saveIMGPath = saveIMGPath
        self.saveJsonPath = saveJsonPath
        self.savepathConvertIMG_Resnet = savepathConvertIMG_Resnet
        self.savepathConvertLBL_Resnet = savepathConvertLBL_Resnet
        self.medicine_df = pd.read_csv(medicinePath)
        self.position_df = pd.read_csv(dbPath)
        self.labeling_df = pd.read_json(labelingPath)
        self.prescription_img = cv2.imread(imgPath)

    def CreateDataset(self, nums, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 10, debug = False):
        """
        Dataset을 만든다.

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
            data_list = self.createData()
            result_img, result_json  = self.createImg(data_list, moveTxt, txtFont, txtSize, debug)

            if debug:
                cv2.namedWindow("result", cv2.WINDOW_NORMAL)
                cv2.imshow('result', result_img)
                cv2.waitKey()
                cv2.destroyAllWindows()
        
            with open(self.saveJsonPath + rf'\{i}.json', 'w', encoding='utf-8') as file:
                file.write(result_json)
                if debug:
                    print(result_json)
            
            cv2.imwrite(self.saveIMGPath + rf'\{i}.jpg', result_img)

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
        data_list.append(self.crateIDdata(id = 82, valueType=1))
        
        # 참고사항
        data_list.append(self.crateIDdata(id = 113, valueType=1))


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


        # id 0~4
        data_list.append(self.crateIDdata(id = 0, valueType=0, intRange=[10000000, 12000000]))
        data_list.append(self.crateIDdata(id = 1, valueType=0, intRange=[2000, 2100]))
        data_list.append(self.crateIDdata(id = 2, valueType=0, intRange=[1, 12]))
        data_list.append(self.crateIDdata(id = 3, valueType=0, intRange=[1, 31]))
        data_list.append(self.crateIDdata(id = 4, valueType=0, intRange=[1, 10000]))

        #이름 생성
        data_list.append(self.name_maker(id=5))
        data_list.append(self.name_maker(id=21))
        data_list.append(self.name_maker(id=116))
        data_list.append(self.name_maker(id=117))

        # id 6~10
        data_list.append(self.crateIDdata(id = 6, valueType=2))
        data_list.append(self.crateIDdata(id = 7, valueType=1))
        data_list.append(self.crateIDdata(id = 8, valueType=3))
        data_list.append(self.crateIDdata(id = 9, valueType=3))
        data_list.append(self.crateIDdata(id = 10, valueType=4))

        # id 11 ~ 21
        # for i in range(11,21):  
        #     data_list.append(self.kcd(i))
        data_list += self.kcd_generator(11)
        temp_ = random.randint(0,2)
        if temp_ ==1 :
            data_list += self.kcd_generator(16)

        # id 22~23, 114~115, 118~120
        data_list.append(self.crateIDdata(id = 22, valueType=5))
        data_list.append(self.crateIDdata(id = 23, valueType=0, intRange=[100000, 999999]))
        data_list.append(self.crateIDdata(id = 114, valueType=0, intRange=[1, 366]))
        data_list.append(self.crateIDdata(id = 115, valueType=1))

        data_list.append(self.crateIDdata(id = 118, valueType=0, intRange=[1, 99]))
        data_list.append(self.crateIDdata(id = 119, valueType=6, intRange=[100000, 999999]))

        data_list.append(self.crateIDdata(id = 120, valueType=1))

        return data_list


    def createMedicineOrInjection(self, type):
        """
        의약품 또는 주사 데이터를 만든다.

        Args:
        ---
        `type [int]` : 0 = 의약품, 1 = 주사

        Returns:
        ---
        
        data_list

        """
        maxCNT = 13
        setid = 30
        sumid = 13

        # 주사 세팅
        if type == 1:
            maxCNT = 7
            setid = 85
            sumid = 7

        data_list = []
        cnt = random.randint(1, maxCNT)
        for i in range(cnt):
            index = random.randint(0, 40000) 
            namesize = random.randint(4, 20)
            medi_name = self.medicine_df.iloc[index, 2][:namesize]
            medi_name = re.sub("\n", "", medi_name)

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
    
    def crateIDdata(self, id, valueType = 0, strRange = [0,40000], intRange = [0,40000]):
        """
        id에 해당하는 값을 생성한다.

        Args:
        ---
        `id [int]` : id

        `valueType [int]` : 0 = int, 1 = str, 2 =  f'{year}{month}{day}-{gender}{random_number}', 3 = phoneNum, 4 = email, 5 = 의사 종류
                            6 = {year}{month}{day}

        `strRange [min, max]` : str value 범위

        `intRange [min, max]` : int value 범위

        Returns:
        ---
        
        data list

        """
        


        # value
        val = random.randint(intRange[0], intRange[1])
        if valueType == 1:
            # 의약품 이름 중 가져오기
            index = random.randint(0, 40000)
            namesize = random.randint(4, 15)
            val = self.medicine_df.iloc[index, 2][:namesize]
            val = re.sub('\n','',val)
        elif valueType == 2:
            # 날짜생성
            year_full=str(random.randint(1950,2023))
            year=year_full[2:4]       
            month=str(random.randint(1,13)).zfill(2)        
            day=str(random.randint(1,32))    

            gender=random.randint(1,2) if year_full[0:2]=='19' else random.randint(3,4)   
            random_number=str(random.randint(0,999999)).zfill(6)
            val = f'{year}{month}{day}-{gender}{random_number}'

        elif valueType == 3:
            # 전화번호
            area_code_list=['02','032','042','051','052','053','062','064','031','033','041','043','054','055','061','063','010']
            area_code_idx=random.randint(0,len(area_code_list) - 1)
            area_code=area_code_list[area_code_idx]
            
            phone_number1=str(random.randint(0,9999)).zfill(4)
            phone_number2=str(random.randint(0,9999)).zfill(4)
            val = f'{area_code}-{phone_number1}-{phone_number2}'

        elif valueType == 4:
            string='abcdefghijklmnopqrstuvwxyz'
            string_list=list(string)

            id_list=string_list.copy()
            random.shuffle(id_list)

            id_length=random.randint(6,12+1)
            id_=''.join(id_list[:id_length])

            email_idx=random.randint(0,2)
            email_list=['@gmail.com','@naver.com','@daum.net']
            email=email_list[email_idx]
            val = f'{id_}{email}'
        elif valueType == 5:
            license_list = ["의사", "치과의사", "한의사"]
            n = random.randint(0,2)
            val = license_list[n]
        elif valueType == 6:
            year_full=str(random.randint(1950,2023))            
            year=year_full[2:4]        
            month=str(random.randint(1,13)).zfill(2)        
            day=str(random.randint(1,32)).zfill(2)  
            val = f'{year}년 {month}월 {day}일'

        
        # id에 해당하는 위치
        mask = self.position_df['id'] == id
        position = self.position_df[mask][['x1', 'y1']].values[0]

        return [str(val), position]
    
    def name_maker(self,id):
        """
        id에 해당하는 이름을 생성

        Args:
        ---

        `id [int]` : id

        Returns:
        ---
        
        data list

        """
        data_list = []
        last_name=['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '류', '전', '홍', '고', '문', '양', '손', '배', '조', '백', '허', '유', '남', '심', '노', '정', '하', '곽', '성', '차', '주', '우', '구', '신', '임', '라', '전', '민', '유', '진', '지', '엄', '채', '원', '천', '방', '공', '강', '현', '함', '변', '염', '양', '변', '여', '추', '노', '도', '소', '신', '석', '선', '설', '마', '길', '주', '연', '방', '위', '표', '명', '기', '반', '왕', '금', '옥', '육', '인', '맹', '제', '모', '장', '남궁', '탁', '국', '여', '진', '어', '은', '편', '구', '용', '유', '예', '경', '봉', '정', '석', '사', '부', '황보', '가', '복', '태', '목', '진', '형', '계', '최', '피', '두', '지', '감', '장']
        first_name=['서율', '하영', '서은', '도희', '도윤', '서윤', '서준', '은우', '시아', '하진', '다인', '예서', '민재', '시은', '주은', '은서', '시현', '시원', '하늘', '하람', '도영', '은호', '서아', '민규', '예원', '서진', '서영', '지민', '지우', '민하', '은준', '민주', '민서', '윤아', '다연', '주희', '다온', '다원', '은정', '윤재', '예은', '서하', '지현', '민지', '민영', '하은', '승현', '서우', '민혁', '현서', '승주', '시우', '승우', '수아', '수민', '시윤', '지원', '승민', '다은', '주현', '현준', '예빈', '은주', '도현', '지안', '지유', '혜원', '유진', '지아', '민아', '주원', '예준', '지윤', '하윤', '지애', '채원', '예진', '지후', '예나', '진아', '진서', '진우', '소율', '지호', '우진', '정우', '소윤', '재민', '건우', '윤서', '윤호', '수빈','하율','예린','현우','준우','다현','서연','연우','하린','유준','하준','준서','이준','서현','은지','민준','선우','서율', '하영', '서은', '도희', '도윤', '서윤', '서준', '은우', '시아', '하진', '다인', '예서', '민재', '시은']

        i=random.randint(0,len(last_name)-1)
        j=random.randint(0,len(first_name) -1)
        val = f'{last_name[i]}{first_name[j]}'

        # id에 해당하는 위치
        mask = self.position_df['id'] == id
        position = self.position_df[mask][['x1', 'y1']].values[0]

        return [str(val), position]
    
    def kcd_generator(self,id = 11):
        alphabet_list=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        alphabet_idx=random.randint(0,len(alphabet_list)-1)
        alphabet=alphabet_list[alphabet_idx]        

        kcd_list=[]
        mask = self.position_df['id'] == id
        position = self.position_df[mask][['x1', 'y1']].values[0]
        kcd_list.append([alphabet,position])

        num=random.randint(1,4)
        for n in range(num):
            id += 1
            number=random.randint(1,9)     
            mask = self.position_df['id'] == id
            position = self.position_df[mask][['x1', 'y1']].values[0]
            kcd_list.append([str(number),position])            

        return kcd_list

    
    # def kcd(self,id):
    #     string='abcdefghijklmnopqrstuvwxyz'
    #     string_list=list(string.upper())
    #     kcd_list=string_list.copy()
        
    #     random.shuffle(kcd_list)
        
    #     kcd_num=str(random.randint(0,9))

    #      # id에 해당하는 위치
    #     mask = self.position_df['id'] == id
    #     position = self.position_df[mask][['x1', 'y1']].values[0]

    #     return [kcd_list[0]+kcd_num,position]
    

    def createImg(self, data, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 15, debug=False):
        imgRGB = cv2.cvtColor(self.prescription_img, cv2.COLOR_BGR2RGB)

        font = ImageFont.truetype(txtFont, txtSize)

        # 이미지를 PIL Image 객체로 변환
        img = Image.fromarray(imgRGB)

        # Draw 객체 생성
        draw = ImageDraw.Draw(img)


        text_sizes_list = []
        # 텍스트를 추가하는 for loop    
        for text, position in data:
            # .text(위치, 텍스트, 텍스트 색, 폰트)
            text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:4]

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
        # 'id', 'x1', 'y1', 'y2' 컬럼의 값을 이용해서 텍스트와 좌표값을 가진 딕셔너리 생성
        position_list = [[row['id'], row['x1'] + moveTxt[0], row['y1'] + moveTxt[1] ,row['x2'] + moveTxt[0] , row['y2'] + moveTxt[1], row['cont']] for _, row in self.labeling_df.iterrows()]

        
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

    def convertDataSetForResnet(self):
        print('\nconvertDataSetForResnet')
        st = time.time()
        dataSetIMG_list = glob.glob(fr"{self.saveIMGPath}\*.jpg")
        dataSetJson_list = glob.glob(fr"{self.saveJsonPath}\*.json")
        
        dataSetIMG_list = natsorted(dataSetIMG_list)
        dataSetJson_list = natsorted(dataSetJson_list)
        
        txt_content = ""
        for imgPath, jsonPath in tqdm(zip(dataSetIMG_list, dataSetJson_list),total=len(dataSetIMG_list)):
            # 이미지 자르기(각 이미지별로 Json을 읽어서 글자별로 자르기)
            ## 이미지 읽기
            img = cv2.imread(imgPath)
            imgname = os.path.splitext(os.path.basename(imgPath))[0]
            
            
            #Json 읽기
            json = pd.read_json(jsonPath)
            cnt = 0
            
            
            for _, row in json.iterrows():
                x1 = row['x1']
                x2 = row['x2']
                y1 = row['y1']
                y2 = row['y2']
                content = row['txt']
                imgPath_ = f'{self.savepathConvertIMG_Resnet}\{imgname}_{cnt}.jpg'
                cv2.imwrite(imgPath_, img[y1:y2, x1:x2])
                
                txt_content += f'{imgPath_}\t{content}\n'
                cnt+=1
                        
                        
        with open(f'{self.savepathConvertLBL_Resnet}\lable.txt', 'w', encoding='utf-8') as f:
                f.write(txt_content)
        
        et = time.time()
        elapsed_time = et - st
        print(f'Execution time: {elapsed_time:.4f} seconds')



def makePath(path):
       
    if not os.path.isdir(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)
        

createPath = r'1.data\4.dataSet'   
saveIMGPath = r'1.data\4.dataSet\img'
saveJsonPath = r'1.data\4.dataSet\json'

createResnetPath = r'1.data\4.dataSet\Resnet'   
savepathConvertIMG_Resnet = r'1.data\4.dataSet\Resnet\img'
savepathConvertLBL_Resnet = r'1.data\4.dataSet\Resnet\label'  

makePath(createPath)
makePath(createResnetPath)
makePath(saveIMGPath)
makePath(saveJsonPath)
makePath(savepathConvertIMG_Resnet)
makePath(savepathConvertLBL_Resnet)

dbPath = r'1.data\3.DB\db.csv'
medicinePath = r'1.data\3.DB\medicine_list.csv'
labelingPath = r'1.data\3.DB\prescript_labeling(Fix).json'
imgPath = r'1.data\1.img\prescription.png'

dataset =  DataSet(saveIMGPath= saveIMGPath,savepathConvertIMG_Resnet= savepathConvertIMG_Resnet,savepathConvertLBL_Resnet = savepathConvertLBL_Resnet, saveJsonPath = saveJsonPath, dbPath = dbPath, medicinePath = medicinePath, labelingPath = labelingPath, imgPath=imgPath)

nums = 100
debug = False
dataset.CreateDataset(nums=nums, debug=debug)
dataset.convertDataSetForResnet()


