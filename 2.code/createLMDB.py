""" a modified version of CRNN torch repository https://github.com/bgshih/crnn/blob/master/tool/create_dataset.py """

#import fire
import os
import lmdb
import cv2

import numpy as np


def checkImageIsValid(imageBin):
    if imageBin is None:
        return False
    imageBuf = np.frombuffer(imageBin, dtype=np.uint8)
    img = cv2.imdecode(imageBuf, cv2.IMREAD_GRAYSCALE)
    imgH, imgW = img.shape[0], img.shape[1]
    if imgH * imgW == 0:
        return False
    return True


def writeCache(env, cache):
    with env.begin(write=True) as txn:
        for k, v in cache.items():
            txn.put(k, v)


def createDataset(inputPath, gtFile, outputPath, map_size=int(1e7), checkValid=True):
    """
    Create LMDB dataset for training and evaluation.
    ARGS:
        inputPath  : input folder path where starts imagePath
        outputPath : LMDB output path
        gtFile     : list of image path and label
        checkValid : if true, check the validity of every image
    """
    os.makedirs(outputPath, exist_ok=True)
    env = lmdb.open(outputPath, map_size=map_size)
    cache = {}
    cnt = 1

    with open(gtFile, 'r', encoding='utf-8') as data:
        datalist = data.readlines()

    nSamples = len(datalist)
    for i in range(nSamples):
        imagePath, label = datalist[i].strip('\n').split('\t')
        imagePath = os.path.join(inputPath, imagePath)

        # # only use alphanumeric data
        # if re.search('[^a-zA-Z0-9]', label):
        #     continue

        if not os.path.exists(imagePath):
            print('%s does not exist' % imagePath)
            continue
        with open(imagePath, 'rb') as f:
            imageBin = f.read()
        if checkValid:
            try:
                if not checkImageIsValid(imageBin):
                    print('%s is not a valid image' % imagePath)
                    continue
            except:
                print('error occured', i)
                with open(outputPath + '/error_image_log.txt', 'a') as log:
                    log.write('%s-th image data occured error\n' % str(i))
                continue

        imageKey = 'image-%09d'.encode() % cnt
        labelKey = 'label-%09d'.encode() % cnt
        cache[imageKey] = imageBin
        cache[labelKey] = label.encode()

        if cnt % 1000 == 0:
            writeCache(env, cache)
            cache = {}
            print('Written %d / %d' % (cnt, nSamples))
        cnt += 1
    nSamples = cnt-1
    cache['num-samples'.encode()] = str(nSamples).encode()
    writeCache(env, cache)
    print('Created dataset with %d samples' % nSamples)


# if __name__ == '__main__':
#     fire.Fire(createDataset)

inputPath = r'1.data\4.dataSet\Resnet\img'
gtFile = r'1.data\4.dataSet\Resnet\label\lable.txt'
outputPath = r'1.data\4.dataSet\Resnet\LMDB\train\MJ'
map_size=int(6e9)
createDataset(inputPath, gtFile, outputPath,map_size = map_size)

inputPath = r'1.data\4.dataSet\Resnet\img2'
gtFile = r'1.data\4.dataSet\Resnet\label2\lable.txt'
outputPath = r'1.data\4.dataSet\Resnet\LMDB\train\ST'
createDataset(inputPath, gtFile, outputPath,map_size = map_size)

inputPath = r'1.data\4.dataSet\Resnet\img3'
gtFile = r'1.data\4.dataSet\Resnet\label3\lable.txt'
outputPath = r'1.data\4.dataSet\Resnet\LMDB\test\MJ'
createDataset(inputPath, gtFile, outputPath,map_size = map_size)

inputPath = r'1.data\4.dataSet\Resnet\img4'
gtFile = r'1.data\4.dataSet\Resnet\label4\lable.txt'
outputPath = r'1.data\4.dataSet\Resnet\LMDB\test\ST'
createDataset(inputPath, gtFile, outputPath,map_size = map_size)