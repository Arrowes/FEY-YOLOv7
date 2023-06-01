# 导入必要的库
import cv2  # 用于图像处理的OpenCV库
import glob  # 用于查找匹配某个模式的文件路径
import os  # 用于与操作系统交互

# 设置输入和输出文件夹
input_folder = "mydata/Guide/"  # 存储输入图像的文件夹
output_folder = "mydata/Guide/1/"  # 存储输出图像的文件夹
if not os.path.exists(output_folder):  # 如果输出文件夹不存在，则创建它
    os.makedirs(output_folder)

# 循环处理每张图像，并应用引导滤波器
for img_path in glob.glob(os.path.join(input_folder, "*.png")):  # 查找输入文件夹中所有的PNG图像文件
    try:
        # 读取输入图像
        img = cv2.imread(img_path)  # 使用OpenCV将图像加载为NumPy数组

        # 转换为灰度图像
        input_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 使用OpenCV将图像转换为灰度图像

        # 应用引导滤波器
        filtered = cv2.ximgproc.guidedFilter(guide=input_gray, src=input_gray, radius=64, eps=400)
        # 使用OpenCV的ximgproc模块应用引导滤波器以增强图像。
        # “guide”是输入图像，“src”是灰度图像。
        # “radius”控制滤波时考虑的邻域的大小。
        # “eps”是一个正则化参数，控制滤波的强度。

        # 增强细节
        details = cv2.subtract(input_gray, filtered)  # 从输入图像中减去滤波后的图像，得到细节图像。
        details = cv2.normalize(details, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)  # 对细节图像进行归一化。
        details = cv2.convertScaleAbs(details, alpha=1.5, beta=0)  # 使用缩放因子增强细节。
        details_bgr = cv2.cvtColor(details, cv2.COLOR_GRAY2BGR)  # 将细节图像转换为BGR颜色空间，以与原始图像合并。

        # 合并原始图像和增强细节
        output_image = cv2.addWeighted(img, 0.7, details_bgr, 0.3, 0)  # 使用OpenCV的addWeighted函数将原始图像和增强细节图像合并。
        # 前两个参数是输入图像，后面是每个图像的权重参数，最后是gamma值。

        # 将输出图像保存到输出文件夹
        output_path = os.path.join(output_folder, os.path.basename(img_path))  # 获取输出文件路径。
        cv2.imwrite(output_path, filtered)  # 将滤波后的图像写入

        print("+1")  # Print a success message for each image processed.
    except Exception as e:  # Handle errors gracefully.
        print(f"Error processing {img_path}: {e}")

print("Done!")  # Print a message when all images have been processed.