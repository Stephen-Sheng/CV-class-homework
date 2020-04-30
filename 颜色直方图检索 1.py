import cv2 as cv
import os

# database图片路径
project_dir = os.path.dirname(os.path.abspath(__file__))
myInput = os.path.join(project_dir, 'CIFAR-10')
myInput1 = os.path.join(myInput, 'database')
os.chdir(myInput1)

# 初始化一些列表和变量
allFeature = [[0] * 72 for _ in range(180)]
feature = [0] * 72
feature1 = [0] * 72
h1 = 0
s1 = 0
v1 = 0
picNum = 0

# 循环读取database中的图片，转换为HSV格式并提取其颜色直方图特征放入allFeature列表中
for image_name in os.listdir(os.getcwd()):
    picNum = image_name.split('(')[1]
    picNum = picNum.split(')')[0]
    img = cv.imread(os.path.join(myInput1, image_name))
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    height = img_hsv.shape[0]
    weight = img_hsv.shape[1]
    channels = img_hsv.shape[2]
    for row in range(height):
        for col in range(weight):
            h = img_hsv[row, col][0]
            s = img_hsv[row, col][1]
            v = img_hsv[row, col][2]
            if 316 <= h <= 360 or 0 <= h <= 20:
                h1 = 0
            if 21 <= h <= 40:
                h1 = 1
            if 41 <= h <= 75:
                h1 = 2
            if 76 <= h <= 155:
                h1 = 3
            if 156 <= h <= 190:
                h1 = 4
            if 191 <= h <= 270:
                h1 = 5
            if 271 <= h <= 295:
                h1 = 6
            if 296 <= h <= 315:
                h1 = 7
            if 0 <= s < 0.2:
                s1 = 0
            if 0.2 <= s < 0.7:
                s1 = 1
            if 0.7 <= s <= 1:
                s1 = 2
            if 0 <= v < 0.2:
                v1 = 0
            if 0.2 <= v < 0.7:
                v1 = 1
            if 0.7 <= v <= 1:
                v1 = 2
            hist = h1 * 9 + s1 * 3 + v1
            feature[hist] = feature[hist] + 1

    allFeature[int(picNum)-1] = feature
    feature = [0] * 72
# query图片路径
myInput2 = os.path.join(myInput, 'query')
os.chdir(myInput2)

# 初始化一些变量
picNum = 0
d = 0
num = 1
rightNum1 = 0
rightNum2 = 0
AP1 = 0
AP2 = 0
mAP = 0
distance = []
label_q = 0
label_d = 0

# 读取每一张待对比图片，计算出其颜色直方图特征并与allFeature中的每一张图片的特征进行对比
for queryImage_name in os.listdir(os.getcwd()):
    print(queryImage_name+'最相似的20张图片为：')
    m = 0
    n = 0
    picNum = queryImage_name.split('(')[1]
    picNum = picNum.split(')')[0]
    if 1 <= int(picNum) <= 10:
        label_q = 0
    if 11 <= int(picNum) <= 20:
        label_q = 1
    img = cv.imread(os.path.join(myInput2, queryImage_name))
    img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    height = img_hsv.shape[0]
    weight = img_hsv.shape[1]
    channels = img_hsv.shape[2]
    for row in range(height):
        for col in range(weight):
            h = img_hsv[row, col][0]
            s = img_hsv[row, col][1]
            v = img_hsv[row, col][2]
            if 316 <= h <= 360 or 0 <= h <= 20:
                h1 = 0
            if 21 <= h <= 40:
                h1 = 1
            if 41 <= h <= 75:
                h1 = 2
            if 76 <= h <= 155:
                h1 = 3
            if 156 <= h <= 190:
                h1 = 4
            if 191 <= h <= 270:
                h1 = 5
            if 271 <= h <= 295:
                h1 = 6
            if 296 <= h <= 315:
                h1 = 7
            if 0 <= s < 0.2:
                s1 = 0
            if 0.2 <= s < 0.7:
                s1 = 1
            if 0.7 <= s <= 1:
                s1 = 2
            if 0 <= v < 0.2:
                v1 = 0
            if 0.2 <= v < 0.7:
                v1 = 1
            if 0.7 <= v <= 1:
                v1 = 2
            hist = h1 * 9 + s1 * 3 + v1
            feature1[hist] = feature1[hist] + 1

    # 计算相似度，使用chi-square distance
    for m in range(180):
        for n in range(72):
            if (feature1[n] + allFeature[m][n]) != 0:
                d = ((feature1[n] - allFeature[m][n]) ** 2 / (feature1[n] + allFeature[m][n])) + d
        distance.append(d)
        d = 0
    newDistance = [None] * len(distance)

    # 对相似度高低进行排列并输入最相似前二十张图片的索引
    for i in range(len(distance)):
        newDistance[i] = distance[i]
    distance.sort()
    for i in range(20):
        print('database('+str(newDistance.index(distance[i])+1)+').png')
        if 1 <= (newDistance.index(distance[i])+1) <= 90:
            label_d = 0
        if 91 <= (newDistance.index(distance[i])+1) <= 180:
            label_d = 1
        if label_d == label_q and label_q == 0:
            # 计算准确率mAP
            rightNum1 = rightNum1 + 1
            AP1 = AP1 + (1 * (rightNum1/num))/10
        if label_d == label_q and label_q == 1:
            rightNum2 = rightNum2 + 1
            AP2 = AP2 + (1 * (rightNum2/num))/10
        num = num + 1
    feature1 = [0] * 72
    distance = []
    num = 1
mAP = AP1 + AP2
mAP = mAP / 2
print(mAP)

