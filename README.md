# thresholdValueSegmentation
图像阈值分割方法实现及演示系统，基于python Qt5
阐述三种阈值分割方法的思路，并将读取显示图像、不同阈值手动设置、统计最佳阈值、大津阈值法、显示分割图像等功能集成到一个GUI软件

界面主要采用PyQt5编写， 主要由两个QLabel组成，一个显示原图，一个显示阈值分割后的图像。以及4个按钮，分别实现选择图片、手动设置阈值分割、迭代法设置分割、Otsu法阈值分割。
![image](https://user-images.githubusercontent.com/39619550/230754492-11bf39e4-bd5e-463c-9faf-e2d930ddd91c.png)
