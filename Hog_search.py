import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter


def read_data(path):
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    os.chdir(os.path.join("CIFAR-10", path))


def get_hog(im):
    # 如果图像维数是3维，则转换成灰度图
    if im.ndim == 3:
        image = np.dot(im[..., :3], [0.299, 0.587, 0.144])
    else:
        image = np.at_least_2d(im)

    sx, sy = image.shape  # 图片尺寸
    orientations = 9  # 梯度直方图的数量
    cx, cy = (8, 8)  # 一个单元的像素个数

    gx = np.zeros(image.shape)
    gy = np.zeros(image.shape)
    gx[:, :-1] = np.diff(image, n=1, axis=1)  # compute gradient on x-direction
    gy[:-1, :] = np.diff(image, n=1, axis=0)  # compute gradient on y-direction
    grad_mag = np.sqrt(gx ** 2 + gy ** 2)  # gradient magnitude
    grad_ori = np.arctan2(gy, (gx + 1e-15)) * (180 / np.pi) + 90  # gradient orientation

    n_cellsx = int(np.floor(sx / cx))  # number of cells in x
    n_cellsy = int(np.floor(sy / cy))  # number of cells in y
    # compute orientations integral images
    orientation_histogram = np.zeros((n_cellsx, n_cellsy, orientations))
    for i in range(orientations):
        # create new integral image for this orientation
        # isolate orientations in this range
        temp_ori = np.where(grad_ori < 180 / orientations * (i + 1),
                            grad_ori, 0)
        temp_ori = np.where(grad_ori >= 180 / orientations * i,
                            temp_ori, 0)
        # select magnitudes for those orientations
        cond2 = temp_ori > 0
        temp_mag = np.where(cond2, grad_mag, 0)
        orientation_histogram[:, :, i] = uniform_filter(temp_mag, size=(cx, cy))[int(cx / 2)::cx, int(cy / 2)::cy].T

    return orientation_histogram.ravel()


def get_list(data, num):
    read_data(data)
    img_feature_list = []
    for i in range(num):
        img_name = data + ' (' + str(i + 1) + ').png'
        img = plt.imread(img_name)
        img_feature_list.append(get_hog(img))
    return img_feature_list


def main():
    database = 'database'
    database_num = 180
    database_feature_list = get_list(database, database_num)
    # print(database_feature_list)

    query = 'query'
    query_num = 20
    query_feature_list = get_list(query, query_num)
    # print(query_feature_list)

    # 初始化变量
    rightNum1 = 0
    rightNum2 = 0
    AP1 = 0
    AP2 = 0
    i = 1
    for query_img in query_feature_list:
        img_name = query + ' (' + str(i) + ').png: '
        print(img_name)
        label_q = 0

        if i > 10:
            label_q = 1

        distance = {}
        j = 1
        for database_img in database_feature_list:
            d = 0
            for m in range(database_img.shape[0]):
                if (query_img[m] + database_img[m]) != 0:
                    d = d + ((query_img[m] - database_img[m]) ** 2 / (query_img[m] + database_img[m]))
            distance[str(j)] = d
            j = j + 1
        distance_order = sorted(distance.items(), key=lambda x: x[1], reverse=False)

        # mAP
        for n in range(20):
            print(database + ' (' + distance_order[n][0] + ').png' )
            label_d = 0
            if int(distance_order[n][0]) > 90:
                label_d = 1

            if label_d == label_q and label_q == 0:
                # 计算准确率mAP
                rightNum1 = rightNum1 + 1
                AP1 = AP1 + (1 * (rightNum1 / (n + 1))) / 20
            if label_d == label_q and label_q == 1:
                rightNum2 = rightNum2 + 1
                AP2 = AP2 + (1 * (rightNum2 / (n + 1))) / 20
        i = i + 1

    mAP = AP1 + AP2
    mAP = mAP / 2
    print(mAP)


if __name__ == '__main__':
    main()