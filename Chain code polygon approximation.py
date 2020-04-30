import numpy as np
from collections import Counter


code = [0, 0, 0, 0, 7, 0, 0, 7, 7, 7, 7, 7, 7, 6, 6, 7, 6, 6, 6, 6, 6, 6, 6, 6, 5, 7, 6, 7, 6, 6, 5, 6, 4, 5, 4, 4, 3,
        4, 3, 6, 6, 6, 6, 5, 6, 5, 5, 4, 5, 4, 4, 4, 4, 3, 4, 3, 3, 2, 3, 2, 2, 2, 2, 5, 4, 5, 4, 4, 3, 4, 2, 3, 2, 2,
        1, 2, 1, 3, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0]
print(len(code))

x = 0
y = 0
pointList = [(x, y)]
for i in code:
    # 输出此多边形的坐标
    if i == 0:
        x = x + 1
        pointList.append((x, y))
        print((x, y))
    if i == 1:
        x = x + 1
        y = y + 1
        pointList.append((x, y))
        print((x, y))
    if i == 2:
        y = y + 1
        pointList.append((x, y))
        print((x, y))
    if i == 3:
        x = x - 1
        y = y + 1
        pointList.append((x, y))
        print((x, y))
    if i == 4:
        x = x - 1
        pointList.append((x, y))
        print((x, y))
    if i == 5:
        x = x - 1
        y = y - 1
        pointList.append((x, y))
        print((x, y))
    if i == 6:
        y = y - 1
        pointList.append((x, y))
        print((x, y))
    if i == 7:
        x = x + 1
        y = y - 1
        pointList.append((x, y))
        print((x, y))
print(pointList)
print(len(pointList))
# 随机选出27个初始点表示
# 空数组中，为1表示被选中
ifChose = np.random.randint(0, 1, len(pointList))
for i in range(0, len(pointList), 3):
    ifChose[i] = 1
print(Counter(ifChose))
for i in range(3, 46, 6):
    ifChose[i] = 0
print(Counter(ifChose))
print(ifChose)


# 新老数组已经生成,计算误差
def calDistance(x1, y1, x2, y2, x0, y0):
    # 点到直线距离
    distance = ((y2 - y1) * x0 + (x1 - x2) * y0 + (x2 * y1 - x1 * y2)) / ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    if distance < 0:
        distance = -distance
    return distance


ifChose = ifChose.tolist()
# d1 = calDistance()
maxDistance = 0
nowDistance = 0
minDistance = 1000
maxNum = 0
minNum = 0
index = 0
# 第一轮的总误差
totalError = 35.19067448629661
# 新的总误差
newError = 0
# split and merge
while newError != 35.19067448629661:
    for i in range(0, len(ifChose) - 4):
        if ifChose[i] == 1:
            index = ifChose.index(1, i + 1, len(ifChose))
            (x1, y1) = pointList[i]
            (x2, y2) = pointList[index]
        if ifChose[i] == 0:
            (x0, y0) = pointList[i]
            nowDistance = calDistance(x1, y1, x2, y2, x0, y0)
            # totalError = totalError + nowDistance
            newError = newError + nowDistance
            if newError < 35.19067448629661:
                totalError = newError
            if nowDistance > maxDistance:
                maxDistance = nowDistance
                maxNum = i
            if nowDistance < minDistance:
                if nowDistance != 0:
                    minDistance = nowDistance
                    minNum = i
    print(minDistance)
    print(maxDistance)
    print(minNum)
    print(maxNum)
    # split and merge
    ifChose[minNum] = 0
    ifChose[maxNum] = 1
theEndList = []
print(totalError)
for i in range(0, len(ifChose) - 1):
    if ifChose[i] == 1:
        (x, y) = pointList[i]
        theEndList.append((x, y))
# 封闭整个图形
theEndList.append((0, 0))
print(theEndList)
