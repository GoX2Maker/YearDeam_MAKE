import cv2
import pandas as pd
import random
from random import randint, shuffle
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import json
from tqdm.auto import tqdm


def CreateDataset(nums, saveIMGPaht, saveJsonPath, dbPath, medicinePath, labelingPath, imgPath, moveTxt = [0,0], txtFont = "malgun.ttf", txtSize = 10, debug =False):
    """
    Yolo와 ResNet data set을 만든다.

    Args:
    ---
        `nums [int]` : 생성할 이미지 갯수

        `saveIMGPaht [string]` : 이미지 저장 경로
        
        `saveJsonPath [string]` : Json 저장 경로

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

    for i in tqdm(range(nums)):
        # 처방전 데이터 생성
        data_list = []
        medicineCNT = random.randint(1, 13)
        data_list += medicine(medicineCNT, medicinePath, dbPath)

        injectionCNT = random.randint(1, 7)
        data_list += injection(injectionCNT, medicinePath, dbPath)
        
        instructionCNT = random.randint(1, 7)
        data_list += instruction(instructionCNT, medicinePath, dbPath)

        data_list += checkSquared(dbPath)

        data_list += id0()
        data_list += id1()
        data_list += id2()
        data_list += id3()
        data_list += id4()
        data_list += name_maker(5)
        data_list += id6()
        data_list += med_name(7)
        data_list += phone_number_maker(8)
        data_list += phone_number_maker(9)
        data_list += email_maker()
        for i in range(11,21):
            data_list += kcd(i)
        data_list += name_maker(21)
        data_list += id22()
        data_list += id23()
        data_list += id114()
        data_list += med_name(115)
        data_list += name_maker(116)
        data_list += name_maker(117)
        data_list += id118()
        data_list += id119()
        data_list += med_name(120)

        # 처방전 이미지 및 Json 생성
        result_img, result_json  = createImg(data_list, labelingPath, imgPath, moveTxt, txtFont, txtSize, debug)

        if debug:
            cv2.namedWindow("result", cv2.WINDOW_NORMAL)
            cv2.imshow('result', result_img)
            cv2.waitKey()
            cv2.destroyAllWindows()
        
        with open(saveJsonPath + rf'\{i}.json', 'w', encoding='utf-8') as file:
            file.write(result_json)
            if debug:
                print(result_json)
        
        cv2.imwrite(saveIMGPaht + rf'\{i}.jpg', result_img)



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


def rnd(num):
    
    return randint(0,num)


def xy(id):

    df = pd.read_csv(r'1.data\3.DB\db.csv')
    mask = df['id'] == id
    df[mask][['x1', 'y1']].values[0]
    return df[mask][['x1', 'y1']].values[0]


def id0():
    id = 0
    val = str(randint(10000000, 12000000))
    return [[str(val),xy(id)]]


def id1():
    id = 1
    val = str(randint(2000, 2100))
    return [[str(val),xy(id)]]


def id2():
    id = 2
    val = str(randint(1, 12))
    return [[str(val),xy(id)]]


def id3():
    id = 3
    val = str(randint(1, 31))
    return [[str(val),xy(id)]]


def id4():
    id = 4
    val = str(randint(1, 10000))
    return [[str(val),xy(id)]]


# 이름 생성기
def name_maker(id): # 5, 21, 116, 117
    
    last_name=['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '류', '전', '홍', '고', '문', '양', '손', '배', '조', '백', '허', '유', '남', '심', '노', '정', '하', '곽', '성', '차', '주', '우', '구', '신', '임', '라', '전', '민', '유', '진', '지', '엄', '채', '원', '천', '방', '공', '강', '현', '함', '변', '염', '양', '변', '여', '추', '노', '도', '소', '신', '석', '선', '설', '마', '길', '주', '연', '방', '위', '표', '명', '기', '반', '왕', '금', '옥', '육', '인', '맹', '제', '모', '장', '남궁', '탁', '국', '여', '진', '어', '은', '편', '구', '용', '유', '예', '경', '봉', '정', '석', '사', '부', '황보', '가', '복', '태', '목', '진', '형', '계', '최', '피', '두', '지', '감', '장']
    first_name=['서율', '하영', '서은', '도희', '도윤', '서윤', '서준', '은우', '시아', '하진', '다인', '예서', '민재', '시은', '주은', '은서', '시현', '시원', '하늘', '하람', '도영', '은호', '서아', '민규', '예원', '서진', '서영', '지민', '지우', '민하', '은준', '민주', '민서', '윤아', '다연', '주희', '다온', '다원', '은정', '윤재', '예은', '서하', '지현', '민지', '민영', '하은', '승현', '서우', '민혁', '현서', '승주', '시우', '승우', '수아', '수민', '시윤', '지원', '승민', '다은', '주현', '현준', '예빈', '은주', '도현', '지안', '지유', '혜원', '유진', '지아', '민아', '주원', '예준', '지윤', '하윤', '지애', '채원', '예진', '지후', '예나', '진아', '진서', '진우', '소율', '지호', '우진', '정우', '소윤', '재민', '건우', '윤서', '윤호', '수빈','하율','예린','현우','준우','다현','서연','연우','하린','유준','하준','준서','이준','서현','은지','민준','선우','서율', '하영', '서은', '도희', '도윤', '서윤', '서준', '은우', '시아', '하진', '다인', '예서', '민재', '시은']

    i=rnd(len(last_name)-1)
    j=rnd(len(first_name) -1)
    return [[f'{last_name[i]}{first_name[j]}',xy(id)]]


def id6(): # 6

    year_full=str(randint(1950,2023))

    year=year_full[2:4]       
    month=str(randint(1,13)).zfill(2)        
    day=str(randint(1,32))    

    gender=randint(1,2) if year_full[0:2]=='19' else randint(3,4)   
    random_number=str(randint(0,999999)).zfill(6)        

    return [[f'{year}{month}{day}-{gender}{random_number}',xy(6)]]


def phone_number_maker(id): # 8 ~ 9
    
    area_code_list=['02','032','042','051','052','053','062','064','031','033','041','043','054','055','061','063','010']
    area_code_idx=rnd(len(area_code_list) - 1)
    area_code=area_code_list[area_code_idx]
    
    phone_number1=str(randint(0,9999)).zfill(4)
    phone_number2=str(randint(0,9999)).zfill(4)
    
    return [[f'{area_code}-{phone_number1}-{phone_number2}',xy(id)]]


def email_maker(): # 10
    
    string='abcdefghijklmnopqrstuvwxyz'
    string_list=list(string)

    id_list=string_list.copy()
    shuffle(id_list)

    id_length=randint(6,12+1)
    id=''.join(id_list[:id_length])

    email_idx=rnd(2)
    email_list=['@gmail.com','@naver.com','@daum.net']
    email=email_list[email_idx]

    return [[f'{id}{email}',xy(10)]]


def kcd(id): # Korean Standard Classification of Disease # 11 ~ 20
    
    string='abcdefghijklmnopqrstuvwxyz'
    string_list=list(string.upper())
    kcd_list=string_list.copy()
    
    shuffle(kcd_list)
    
    kcd_num=str(randint(0,9))

    return [[kcd_list[0]+kcd_num,xy(id)]]


def id22():
    license_list = ["의사", "치과의사", "한의사"]
    n = randint(0,2)
    return [[license_list[n],xy(22)]]


def id23():
    num23 = str(randint(100000,999999))
    return [[num23,xy(23)]]


def id114():    
    num114 = str(randint(1,366))
    return [[num114,xy(114)]]


def id118():    
    num118 = str(randint(1,99))
    return [[num118,xy(118)]]


def id119():    
    year_full=str(randint(1950,2023))            
    year=year_full[2:4]        
    month=str(randint(1,13)).zfill(2)        
    day=str(randint(1,32))        
    return [[f'{year}년 {month}월 {day}일',xy(119)]]


def med_name(id): # 7, 115, 120
    
    dataPath=r'1.data\3.DB\medicine_list.csv' # dataPath : 의약DB 경로
    
    df_med=pd.read_csv(dataPath)

    index = randint(0, 40000)
    
    med_name = df_med.iloc[index, 2][:10]

    return [[med_name,xy(id)]]

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
    # if debug:
    #     for x1, y1, x2, y2, txt in text_sizes_list:
    #         cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 1)



    # 처방전 라벨링 사각형 그리기

    df = pd.read_json(labelingPath)

    # 'id', 'x1', 'y1', 'y2' 컬럼의 값을 이용해서 텍스트와 좌표값을 가진 딕셔너리 생성
    position_list = [[row['id'], row['x1'] + moveTxt[0], row['y1'] + moveTxt[1] ,row['x2'] + moveTxt[0] , row['y2'] + moveTxt[1], row['cont']] for _, row in df.iterrows()]

    
    #사각형 그리기
    # if debug:
    #     for id, x1, y1, x2, y2, txt in position_list:
    #         cv2.rectangle(result_img, (x1, y1), (x2, y2), (0, 255, 0), 1)
    #         text_sizes_list.append([x1, y1, x2, y2,txt])

    # Json 파일 만들기
    text_sizes_dics = []
    for x1, y1, x2, y2, txt in text_sizes_list:
        text_sizes_dics.append({'x1' : int(x1), 'y1' : int(y1), 'x2' : int(x2), 'y2' : int(y2), 'txt' : str(txt)})
        

    result_json = json.dumps(text_sizes_dics, ensure_ascii=False , indent=4)


    return result_img, result_json



nums = 1
saveIMGPaht = r'1.data\4.dataSet\img'
saveJsonPath = r'1.data\4.dataSet\json'
dbPath = r'1.data\3.DB\db.csv'
medicinePath = r'1.data\3.DB\medicine_list.csv'
labelingPath = r'1.data\3.DB\prescript_labeling(Fix).json'
imgPath = r'1.data\1.img\prescription.png'
debug = True

CreateDataset(nums=nums, saveIMGPaht = saveIMGPaht, saveJsonPath = saveJsonPath, dbPath = dbPath, medicinePath= medicinePath, labelingPath = labelingPath, imgPath = imgPath, debug = debug)