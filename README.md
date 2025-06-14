# DIP_Final_Proj
本项目基于UESTC数字图像处理课程进行, 具体要求如下:

## 题  目
* 将图像的灰度级分辨率调整至 ，并在同一个figure窗口上将它们显示出来。（15分）
* 往图像中叠加不同类型的噪声，并设计一个频域低通滤波器来去除之（20分）。
* 举例说明顶帽变换在图像阴影校正方面的应用。（源图像为“rice.bmp”）（12分）
* 利用Hough变换来检测图像中的直线，与变换过程相关的系列约束条件（线段的最小长度等）可自行叠加。（源图像为“bank.bmp”）（13分）
* 对图像执行阈值分割操作并统计出每一个区域块的属性，然后，将每个区域的中心和外接矩形给标注出来。（提示：如果分割后的区域块数太多，建议采用Matlab下的bwareaopen函数来筛选掉一部分区域块）（15分）
* 设计一个简易的Matlab GUI界面程序，要求其具有如下的功能：①打开与保存图像时均打开文件名设置对话框；②当下拉菜单中的条目被选中时，列表框之中实时的记录下当前的选择；③通过编辑框来实现相关参数的交互式输入；④将输入图像及处理后的结果显示在相应的坐标轴之上；⑤含有工具栏和菜单栏，当选择其下的组件成分时，要有相应的图像处理行为发生；⑥将figure窗口的“Name”属性修改为自己的姓名和学号；⑦将所设计的GUI程序编译为“.exe”形式的可执行文件（25分）。

## 简介
最后一题的GUI程序采用 python 进行开发, 主要运用了tkinter, skimage 以及 numpy 等库进行制作, 最后用 pyinstaller 打包成可执行文件.

这段代码实现了一个 图像处理图形界面（GUI）应用程序，其主要目的是：
	•	提供一个用户友好的图形界面，用于加载和操作图像；
	•	支持多种图像处理功能，例如图像增强、滤波、翻转等；
	•	集成了 skimage 和 PIL 等图像处理库进行图像转换与处理；
	•	提供历史记录功能（如图像列表记录）以便用户回溯处理过的图像。

 <img width="300" alt="image" src="https://github.com/user-attachments/assets/a260c823-95fc-405b-86d2-9fd44ab4ba26" />


## 图像处理功能概括

* 图像读取与显示
*	图像翻转
*	图像增强（Exposure Adjustment）:均衡化直方图, 调整 gamma, log 以及对比度调整操作。
*	图像滤波（Filtering）:巴特沃斯滤波器, 索贝尔滤波器, 高斯滤波器以及OTSU法；
*	形态学处理（Morphology）:支持基本的形态学操作，如腐蚀（Erosion）、膨胀（Dilation）、开运算（Opening）等；


具体实现原理及细节可见文档 `期末课程设计.docx` .
