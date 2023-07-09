from random import randint, shuffle
import pandas as pd


def rnd(num):
    
    return randint(0,num)


def xy(id):

    df = pd.read_csv('../../1.data/3.DB/db.csv')
    x1 = df['x1'].values[id]
    y1 = df['y1'].values[id]
    return [x1,y1]


def id0():
    id = 0
    val = str(randint(10000000, 12000000))
    return val,xy(id)


def id1():
    id = 1
    val = str(randint(2000, 2100))
    return val,xy(id)


def id2():
    id = 2
    val = str(randint(1, 12))
    return val,xy(id)


def id3():
    id = 3
    val = str(randint(1, 31))
    return val,xy(id)


def id4():
    id = 4
    val = str(randint(1, 10000))
    return val,xy(id)


# 이름 생성기
def name_maker(id): # 5, 21, 116, 117
    
    last_name=['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '류', '전', '홍', '고', '문', '양', '손', '배', '조', '백', '허', '유', '남', '심', '노', '정', '하', '곽', '성', '차', '주', '우', '구', '신', '임', '라', '전', '민', '유', '진', '지', '엄', '채', '원', '천', '방', '공', '강', '현', '함', '변', '염', '양', '변', '여', '추', '노', '도', '소', '신', '석', '선', '설', '마', '길', '주', '연', '방', '위', '표', '명', '기', '반', '왕', '금', '옥', '육', '인', '맹', '제', '모', '장', '남궁', '탁', '국', '여', '진', '어', '은', '편', '구', '용', '유', '예', '경', '봉', '정', '석', '사', '부', '황보', '가', '복', '태', '목', '진', '형', '계', '최', '피', '두', '지', '감', '장']
    first_name=['서율', '하영', '서은', '도희', '도윤', '서윤', '서준', '은우', '시아', '하진', '다인', '예서', '민재', '시은', '주은', '은서', '시현', '시원', '하늘', '하람', '도영', '은호', '서아', '민규', '예원', '서진', '서영', '지민', '지우', '민하', '은준', '민주', '민서', '윤아', '다연', '주희', '다온', '다원', '은정', '윤재', '예은', '서하', '지현', '민지', '민영', '하은', '승현', '서우', '민혁', '현서', '승주', '시우', '승우', '수아', '수민', '시윤', '지원', '승민', '다은', '주현', '현준', '예빈', '은주', '도현', '지안', '지유', '혜원', '유진', '지아', '민아', '주원', '예준', '지윤', '하윤', '지애', '채원', '예진', '지후', '예나', '진아', '진서', '진우', '소율', '지호', '우진', '정우', '소윤', '재민', '건우', '윤서', '윤호', '수빈','하율','예린','현우','준우','다현','서연','연우','하린','유준','하준','준서','이준','서현','은지','민준','선우','서율', '하영', '서은', '도희', '도윤', '서윤', '서준', '은우', '시아', '하진', '다인', '예서', '민재', '시은']

    i=rnd(len(last_name))
    j=rnd(len(first_name))
    return f'{last_name[i]}{first_name[j]}',xy(id)


def id6(): # 6

    year_full=str(randint(1950,2023))

    year=year_full[2:4]       
    month=str(randint(1,13)).zfill(2)        
    day=str(randint(1,32))    

    gender=randint(1,2) if year_full[0:2]=='19' else randint(3,4)   
    random_number=str(randint(0,999999)).zfill(6)        

    return f'{year}{month}{day}-{gender}{random_number}',xy(6)


def phone_number_maker(id): # 8 ~ 9
    
    area_code_list=['02','032','042','051','052','053','062','064','031','033','041','043','054','055','061','063','010']
    area_code_idx=rnd(len(area_code_list))
    area_code=area_code_list[area_code_idx]
    
    phone_number1=str(randint(0,9999)).zfill(4)
    phone_number2=str(randint(0,9999)).zfill(4)
    
    return f'{area_code}-{phone_number1}-{phone_number2}',xy(id)


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

    return f'{id}{email}',xy(10)


def kcd(id): # Korean Standard Classification of Disease # 11 ~ 20
    
    string='abcdefghijklmnopqrstuvwxyz'
    string_list=list(string.upper())
    kcd_list=string_list.copy()
    
    shuffle(kcd_list)
    
    kcd_num=str(randint(0,9))

    return kcd_list[0]+kcd_num,xy(id)


def id22():
    license_list = ["의사", "치과의사", "한의사"]
    n = randint(0,2)
    return license_list[n],xy(22)


def id23():
    num23 = str(randint(100000,999999))
    return num23,xy(23)


def id114():    
    num114 = randint(1,366)
    return num114,xy(114)


def id118():    
    num118 = randint(1,99)
    return num118,xy(118)


def id119():    
    year_full=str(randint(1950,2023))            
    year=year_full[2:4]        
    month=str(randint(1,13)).zfill(2)        
    day=str(randint(1,32))        
    return f'{year}년 {month}월 {day}일'


def med_name(id): # 7, 115, 120
    
    dataPath='../../1.data/3.DB/medicine_list.csv' # dataPath : 의약DB 경로
    
    df_med=pd.read_csv(dataPath)

    index = randint(0, 40000)
    
    med_name = df_med.iloc[index, 2][:10]

    return med_name,xy(id)