import cv2
import numpy as np
import time
import serial


time.sleep(1)
cap = cv2.VideoCapture(0)
color_ball = [0, 6, 60, 190, 160, 255]
s = ""
s_prev = ""
t1 = 0


def detectcolors(img, colors1):
    # color part ||||||||||||||||||||||||||||||||||||||
    x_ball, y_ball, x, y = None, None, None, None
    global s, s_prev, t1
    s_prev = s

    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower1 = np.array([colors1[0], colors1[2], colors1[4]])
    upper1 = np.array([colors1[1], colors1[3], colors1[5]])
    mask1 = cv2.inRange(hsv_img, lower1, upper1)
    result1 = cv2.bitwise_and(img, img, mask=mask1)
    moments1 = cv2.moments(mask1, 1)
    x_m1 = moments1['m10']
    y_m1 = moments1['m01']
    area1 = moments1['m00']

    # arUco part |||||||||||||||||||||||||||||||||||||||
    imgAruco = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
    parameters_ = cv2.aruco.DetectorParameters()
    det = cv2.aruco.ArucoDetector(dictionary, parameters_)
    corners, ids, _ = det.detectMarkers(img)
    # print(ids)

    # переформирование массива
    try:
        final_array = np.array(corners[0][0], dtype='int16')
        # обводка метки
        cv2.line(img, final_array[0], final_array[1], (0, 255, 0), thickness=2)
        cv2.line(img, final_array[1], final_array[2], (0, 255, 0), thickness=2)
        cv2.line(img, final_array[2], final_array[3], (0, 255, 0), thickness=2)
        cv2.line(img, final_array[3], final_array[0], (0, 255, 0), thickness=2)

        # рассчет координат
        x = (final_array[0][0] + final_array[2][0]) // 2
        y = (final_array[0][1] + final_array[2][1]) // 2
        cv2.putText(img, 'x:' + str(x) + ' ' + 'y:' + str(y), [x, y], 2, 1, (0, 255, 0), 1)
        img = cv2.circle(img, (x, y), radius=2, color=(255, 0, 0), thickness=3)
    except:
        print('No aruco')
        x = None
        y = None

    # вывод шарика
    if area1 > 10:
        x_ball = int(x_m1 / area1)
        y_ball = int(y_m1 / area1)
        cv2.putText(img, 'x:' + str(x_ball) + ' ' + 'y:' + str(y_ball), (x_ball, y_ball), 2, 1, (0, 255, 255), 1)
        img = cv2.circle(img, (x_ball, y_ball), radius=2, color=(255, 0, 0), thickness=3)

    # основные рассчеты и отправка на ардуинку
    if x_ball is not None and y_ball is not None and x is not None and y is not None:

        cv2.line(img, [x_ball, y_ball], [x_ball, y], (255, 100, 0), thickness=2)
        cv2.line(img, [x, y], [x_ball, y], (255, 100, 0), thickness=2)

        # отправка на ардуино x aruco - x ball
        if x_ball is not None and y_ball is not None:
            if abs(y - y_ball) < 45 and y_ball > y:
                s = '1,'
            else:
                s = '0,'
            s += '{0};{1}\n'.format(str(x), str(x_ball))
        else:
            if abs(y - y_ball) < 45 and y_ball > y:
                s = '1,'
            else:
                s = '0,'
            s += '0;0\n'
        # print(s)
    else:
        cv2.rectangle(img, [0, 0], [15, 15], (0, 0, 0), thickness=15)
        s = '0,0;0\n'
        if time.time() - t1 > 0.05:
            t1 = time.time()
            arduinoSerial.write(s.encode())
            print(s)

    if s != s_prev and time.time() - t1 > 0.05:
        t1 = time.time()
        arduinoSerial.write(s.encode())
        print(s)
    s_prev = s

    # показ картинки
    cv2.imshow("Work", img)


while True:
    try:
        arduinoSerial = serial.Serial('COM7', 9600)
        time.sleep(1)
        while True:
            success, image = cap.read()
            # image = cv2.flip(image, flipCode=0)
            # image = cv2.imread('pics/test1.jpg')
            detectcolors(image, color_ball)
            cv2.waitKey(1)
        cap.release()
        cv2.destroyAllWindows()
    except serial.SerialException:
        print("Exception")

