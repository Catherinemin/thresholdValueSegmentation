from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QFileDialog,QLabel
from PySide2.QtGui import QPixmap
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2
from PIL import Image
import os


class ThresholdUI:

    def __init__(self, fname=''):
        object.__init__(self)

        self.fname = fname  # fname为所选图片路径

        # 从 UI 定义中动态 创建一个相应的窗口对象
        self.ui = QUiLoader().load('main.ui')
        self.ui.setWindowTitle('图像阈值分割')

        self.ui.pushButton.clicked.connect(self.loadImage1)
        self.ui.pushButton_2.clicked.connect(self.setT)
        self.ui.pushButton_4.clicked.connect(self.optimalTthreshold)
        self.ui.pushButton_3.clicked.connect(self.ostu1)

    def setBasicImage(self):
        # 原图
        # self.image = cv2.imread(self.fname)
        self.image = Image.open(self.fname)  # 打开原图

        # 灰度图
        # self.grayImage = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.grayImage = self.image.convert('L')  # 转化为灰度图像

    def loadImage1(self):
        # fname为所选图片路径
        self.fname, _ = QFileDialog.getOpenFileName(self.ui, '打开文件', '.', '图像文件(*.jpg *.png)')
        self.ui.label_4.setPixmap(QPixmap(self.fname))
        self.ui.spinBox.setValue(0)  # 设置数字
        try:
            self.ui.label_5.setPixmap(QPixmap(None))  # 每次打开一个新的图片都将阈值分割 图像label显示为空
        except:
            pass
        # return fname

    def setT(self):
        """手动设置阈值"""
        try:
            os.remove('./output_images/st.png')  # 每次执行前删除上一次运行的结果
        except:
            pass
        self.setBasicImage()
        tValue = self.ui.spinBox.value()  # 获取数字
        # self.ui.box.setValue(number)  # 设置数字
        gray= np.array(self.grayImage)

        ret1, thresh1 = cv2.threshold(gray, tValue, 255, cv2.THRESH_BINARY)
        # ret1是设置的阈值，thresh1是仅包含黑白色的阈值图像。源图像 gray_image 中灰色强度小于 50 的像素为黑色，强度大于 50 的像素为白色。
        # return ret1, thresh1
        cv2.imwrite('./output_images/st.png', thresh1)
        self.ui.label_5.setPixmap(QPixmap('./output_images/st.png'))  # 在界面中显示阈值后的图像
        # label_7 存放当前阈值
        self.ui.label_7.setNum(ret1)


    def optimalTthreshold(self):
        # 统计最佳阈值, 迭代法
        # 读入图片并转化为矩阵
        # img = cv2.imread(r'./images/Lenna.png', 0)
        self.ui.spinBox.setValue(0)  # 设置数字
        try:
            os.remove('./output_images/op.png')  # 每次执行前删除上一次运行的结果
        except:
            pass


        self.setBasicImage()
        im = np.array(self.grayImage)

        # 矩阵大小
        l = len(im)
        w = len(im[0])

        # 求初始阈值
        zmin = np.min(im)
        zmax = np.max(im)
        t0 = int((zmin+zmax)/2)
        # t0 = (zmin + zmax) // 2

        # 初始化相关变量初始化
        t1 = 0
        res1 = 0
        res2 = 0
        s1 = 0
        s2 = 0

        # 迭代法计算最佳阈值
        while abs(t0 - t1) > 0:
            for i in range(0, l - 1):
                for j in range(0, w - 1):
                    if im[i, j] < t0:
                        res1 = res1 + im[i, j]
                        s1 = s1 + 1
                    elif im[i, j] > t0:
                        res2 = res2 + im[i, j]
                        s2 = s2 + 1
            if s1 != 0:
                avg1 = res1 / s1
            else:
                avg1 = 0
            avg2 = res2 / s2
            res1 = 0
            res2 = 0
            s1 = 0
            s2 = 0
            t1 = t0  # 旧阈值储存在t1中
            t0 = int((avg1 + avg2) / 2)  # 计算新阈值
            # print(t0)

        # 阈值化分割,t0最佳阈值
        # 像素点灰度值小于最佳阈值t0用0填充，其余用255填充
        im = np.where(im[..., :] < t0, 0, 255)

        # 绘制原图直方图并显示最佳阈值
        # plt.figure()
        # plt.hist(img.ravel(), 256)
        # plt.title('hist')
        # plt.axvline(t0)  # 绘制最佳阈值分割线
        # plt.text(25, 6100, "Best Threshold:{}".format(t0), size=15, alpha=0.8)

        # 绘制阈值化分割后图像
        plt.figure()
        im1=Image.fromarray(np.uint8(im))

        # im1.resize(400,400)
        plt.imshow(im1, cmap='gray')

        plt.axis('off')
        fig = plt.gcf()
        fig.set_size_inches(4.0 / 3, 4.0 / 3)  # dpi = 300, output = 400*400 pixels
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
        plt.margins(0, 0)
        fig.savefig('./output_images/op.png', format='png', transparent=True, dpi=300, pad_inches=0)

        self.ui.label_5.setPixmap(QPixmap('./output_images/op.png'))  # 在界面中显示阈值后的图像
        self.ui.label_7.setNum(t0)


    def ostu1(self):
        self.ui.spinBox.setValue(0)  # 设置数字
        try:
            os.remove('./output_images/ostu.png')  # 每次执行前删除上一次运行的结果
        except:
            pass

        self.setBasicImage()
        gray= np.array(self.grayImage)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret, otsu = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        cv2.imwrite('./output_images/ostu.png', otsu)

        self.ui.label_5.setPixmap(QPixmap('./output_images/ostu.png'))  # 在界面中显示阈值后的图像
        self.ui.label_7.setNum(ret)



app = QApplication([])
# 加载 icon
app.setWindowIcon(QIcon('icon.jpg'))
tClient = ThresholdUI()
tClient.ui.show()
app.exec_()

