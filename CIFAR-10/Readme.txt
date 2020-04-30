1、CIFAR-10
该数据集共有60000个彩色图像，这些图像的像素是32*32，分为10个类，
每类6000个图像。这些类完全相互排斥，不会出现包含关系。

2、课程实验数据（CIFAR-10 subset）
选取CIFAR-10的一个子集：cat和dog类，每类100张图像，进行图像
检索任务。选取的图像按照   database:query = 9:1  的比例进行划分。

文件组织：
database文件夹 ------  图库，共180个图像
query文件夹    ------  query，共20个图像
database_label ------  图库中图像的标签（cat-0 dog-1）
query_label    ------  query中图像的标签