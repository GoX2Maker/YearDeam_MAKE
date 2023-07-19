import os
import glob
from natsort import natsorted
import cv2
import pandas as pd
from tqdm.auto import tqdm

import shutil

# 폴더 만들기
# 1.data\4.dataSet\Resnet\img
# 1.data\4.dataSet\Resnet\label

def makePath(pathIMG, pathLBL):
    
    if not os.path.isdir(r'1.data\4.dataSet\Resnet'):
        os.mkdir(r'1.data\4.dataSet\Resnet')
    else:
        shutil.rmtree(r'1.data\4.dataSet\Resnet')
        os.mkdir(r'1.data\4.dataSet\Resnet')
        
    if not os.path.isdir(pathIMG):
        os.mkdir(pathIMG)
    if not os.path.isdir(pathLBL):
        os.mkdir(pathLBL)


def test(dataSetIMG, dataSetJson, save_IMGPath, save_LBLPath):
    dataSetIMG_list = glob.glob(fr"{dataSetIMG}\*.jpg")
    dataSetJson_list = glob.glob(fr"{dataSetJson}\*.json")
    
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
            imgPath_ = f'{save_IMGPath}\{imgname}_{cnt}.jpg'
            cv2.imwrite(imgPath_, img[y1:y2, x1:x2])
            
            txt_content += f'{imgPath_}\t{content}\n'
            cnt+=1
                       
                       
    with open(f'{save_LBLPath}\lable.txt', 'w') as f:
            f.write(txt_content) 

    
savepathIMG = r'1.data\4.dataSet\Resnet\img'
savepathLBL = r'1.data\4.dataSet\Resnet\label'    
makePath(savepathIMG, savepathLBL) 
    
dataSetIMG = r'1.data\4.dataSet\img'
dataSetJson_list = r'1.data\4.dataSet\json'
test(dataSetIMG,dataSetJson_list, savepathIMG, savepathLBL)


# 테스트 구조
# {filename}\t{label}\n