import cv2 as cv
import numpy as np
import math
import time
import serial

capture = cv.VideoCapture(0)

# video = "http://admin:admin@10.242.200.134:8081/"  # admin是账号:admin是密码 后面是局域网
# capture = cv.VideoCapture(video)


# 获得欧几里距离
def _get_eucledian_distance(vect1, vect2):
    distant = vect1[0] - vect2[0]
    dist = np.sqrt(np.sum(np.square(distant)))
    # 或者用numpy内建方法
    # vect1 = list(vect1)
    # vect2 = list(vect2)
    # dist = np.linalg.norm(vect1 - vect2)
    return dist


def gesture_recognition():

    while True:
        ret, frame = capture.read()  # 读取摄像头
        # frame = cv.flip(frame, 1)
        fgbg = cv.createBackgroundSubtractorMOG2()  # 利用BackgroundSubtractorMOG2算法消除背景
        # fgmask = bgModel.apply(frame)
        fgmask = fgbg.apply(frame)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # res = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        kernel = np.ones((5, 5), np.uint8)
        fgmask = cv.erode(fgmask, kernel, iterations=1)  # 膨胀
        res = cv.bitwise_and(frame, frame, mask=fgmask)
        ycrcb = cv.cvtColor(res, cv.COLOR_BGR2YCrCb)  # 分解为YUV图像,得到CR分量
        (_, cr, _) = cv.split(ycrcb)
        cr1 = cv.GaussianBlur(cr, (5, 5), 0)  # 高斯滤波
        _, skin = cv.threshold(cr1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)  # OTSU图像二值化
        # dst = cv.GaussianBlur(frame, (3, 3), 0)
        # gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
        # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
        # cv.imshow("binary_image", binary)
        # hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)  # hsv 色彩空间 分割肤色
        # ycrcb = cv.cvtColor(frame, cv.COLOR_BGR2YCrCb)  # Ycrcb 色彩空间 分割肤色
        # # lower_hsv = np.array([0, 15, 0])
        # # upper_hsv = np.array([17, 170, 255])
        # lower_ycrcb = np.array([0, 135, 85])
        # upper_ycrcb = np.array([255, 180, 135])
        # # mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)  # hsv 掩码
        # mask = cv.inRange(ycrcb, lowerb=lower_ycrcb, upperb=upper_ycrcb)  # ycrcb 掩码
        # dst = cv.GaussianBlur(mask, (11, 11), 0)  # 高斯去噪
        # gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)

        # edge_output = cv.Canny(gray, 50, 150)  # 图像边缘提取
        # kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))  # 获取图像结构化元素
        # # dst = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)  # 开操作
        # dst = cv.erode(skin, kernel)  # 膨胀操作
        gesture_roi = skin[0:350, 380:700]
        cv.imshow("dst_demo", skin)
        # cv.imshow("gesture_roi", gesture_roi)
        contours, heriachy = cv.findContours(gesture_roi, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 获取轮廓点集(坐标)
        # if contours[0] < [30, 260]:
        #     cnt = contours[0]
        # elif 270 <= contours[0] < [60, 260]:
        #     cnt = contours[1]
        # else:
        #     cnt = contours[2]
        # cnt = contours[0]
        # print(cnt)
        # print(contours)
        # cnt = contours[0]
        for i, contour in enumerate(contours):  # 获取轮廓
            cv.drawContours(frame[0:350, 380:700], contours, i, (255, 0, 0), 1)  # 绘制轮廓
        #  得到面积
        # area = cv.contourArea(contour)
        # 得到外接矩形
        # x, y, w, h = cv.boundingRect(contour)
        # 得到的几何距是字典类型的
        # mm = cv.moments(contour)
        # cx = mm['m10']/mm['m00']
        # cy = mm['m01']/mm['m00']
        # center, radius = cv.minEnclosingCircle(contour)
        # center = (int(x), int(y))
        # radius = int(radius)
        # cv.circle(frame, center, radius, (0, 255, 255), 2)
        # cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        # print(i)
        # cv.imshow("measure_contures", frame)
            x, y, w, h = cv.boundingRect(contour)
            # center = (int(x), int(y))
            cv.rectangle(frame[0:350, 380:700], (x, y), (x + w, y + h), (100, 100, 0), 1)
        # approxcurve = cv.approxPolyDP(contour, 4, False)
        # if approxcurve.shape[0] < 5:
        #     cv.drawContours(frame, contours, -1, (0, 255, 0), 3)

        hull = cv.convexHull(contour, True, returnPoints=False)  # 获得凸包点 x, y坐标
        defects = cv.convexityDefects(contour, hull)  # 计算轮廓的凹点
        # print(hull, defects)
        # cv.polylines(frame[0:350, 380:700], [hull], True, (0, 255, 0), 3)
        """
        defect反馈的是Nx4的数组，
        第一列表示的是起点（轮廓集合中点的编号）
        第二列表示的是终点（轮廓集合中点的编号）
        第三列表示的是最远点（轮廓集合中点的编号）
        第四列表示的是最远点到凸轮廓的最短距离
        """
        # cv.drawContours(frame[0:350, 380:700], hull, -1, (255, 0, 0), 5, 8)  # 绘制凸包

        # dist = np.sqrt(np.sum(np.square(vect1 - vect2)))
        ndefects = 0
        if defects is not None:  # 重要!

            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                # float(s)
                # float(e)
                # float(f)
                # float(d)
                start = tuple(contour[s][0])  # 起点
                end = tuple(contour[e][0])  # 终点
                far = tuple(contour[f][0])  # 最远点
                a = _get_eucledian_distance(start, end)
                b = _get_eucledian_distance(start, far)
                c = _get_eucledian_distance(end, far)
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
                cv.line(frame[0:350, 380:700], start, end, [255, 255, 0], 2)
                cv.circle(frame[0:350, 380:700], far, 5, [0, 0, 255], -1)
                if angle <= math.pi / 5:  # <30度:
                    ndefects = ndefects + 1
                print("数字 = %f" % ndefects)


        # cv.polylines(frame[50:350, 380:700], [hull], True, (0, 255, 0), 2)
        # retval = cv.pointPolygonTest(contour, center, True)
        # cv.drawContours(frame, defects, -1, (0, 255, 0), 3)
        # cv.imshow("defects", defects)
        cv.imshow("video", frame)
        c = cv.waitKey(50)
        if c == 27:

            break


def gesture_recognition_two():
    img = cv.imread("E:/pictureprocessing/practice/picture/practice_one.png")
    img = cv.flip(img, 1)
    # dst = cv.GaussianBlur(frame, (3, 3), 0)
    # gray = cv.cvtColor(dst, cv.COLOR_BGR2GRAY)
    # ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    # cv.imshow("binary_image", binary)
    # hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # 通过hsv将颜色过滤出来
    # lower_hsv = np.array([100, 43, 46])
    # upper_hsv = np.array([124, 255, 255])
    # mask = cv.inRange(hsv, lowerb=lower_hsv, upperb=upper_hsv)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)
    dst = cv.GaussianBlur(binary, (1, 1), 0)  # 高斯去噪
    # cv.imshow("dst_demo", dst)
    contours, heriachy = cv.findContours(dst, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)  # 获取轮廓本身
    for i, contour in enumerate(contours):  # 获取轮廓
        cv.drawContours(img, contours, i, (0, 255, 0), 3)  # 绘制轮廓
        print(i)

    cv.imshow("img_demo", img)


cv.namedWindow("video")
gesture_recognition()
# gesture_recognition_two()

cv.waitKey(0)
capture.release()
cv.destroyAllWindows()