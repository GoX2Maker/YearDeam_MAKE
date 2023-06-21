'''
1.약 이름
/1.data/3.DB/medicine_list.csv

0607practice.py
0609seon.py
파일을 참고
'''



import cv2
import pandas as pd
from practice_0607 import input_pre1


df1 = pd.read_csv(r'1.data\3.DB\prescription1.csv')
df2 = pd.read_csv(r'1.data\3.DB\prescription2.csv')

df2["id"] = df2["id"] + 30

df = pd.concat([df1, df2], ignore_index=True)

df.to_csv(r'1.data\3.DB\db.csv', index=False)

#1. 데이터를 읽고 name 컬럼을 만든다. ,df3 name컬럼에 임의의(a~z) 데이터를 넣기
df3 = pd.read_csv(r'1.data\3.DB\db.csv')

name = []
str = 'abcdefghijklmnopqrstuvwxyz'
    
for i in range(len(df3.index)):
    name.append(str[i % len(str)])
    
#print(name)
df3["name"] = name

df3.to_csv(r'1.data\3.DB\db_name.csv', index=False)

csvPath = r'1.data\3.DB\db_name.csv'
imgPath = r'1.data\1.img\prescription.png'
moveTxt = [0, 0]
txtFont = "malgun.ttf"
txtSize = 15

text_list, result_img = input_pre1(csvPath, imgPath, moveTxt)
print(text_list)
cv2.imshow('result', result_img)
cv2.waitKey()
cv2.destroyAllWindows()