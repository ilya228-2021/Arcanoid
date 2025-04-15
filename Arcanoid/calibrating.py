# выделение цвета с помощью opencv на статичном изображении
import cv2
import numpy as np


def empty(x):
    pass


# original_img = cv2.imread("car_lamborgini.jpg")
# original_img = cv2.imread("1.jpg")
img1 = cv2.VideoCapture(0)
# img1 = cv2.imread('pics/test1.jpg')
succ, original_img = img1.read()
original_img = cv2.flip(original_img, flipCode=1)

hsv_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2HSV)

cv2.namedWindow("trackbars")
cv2.resizeWindow("trackbars", 500, 250)
cv2.createTrackbar("hue min", "trackbars", 0, 179, empty)
cv2.createTrackbar("hue max", "trackbars", 179, 179, empty)
cv2.createTrackbar("sat min", "trackbars", 0, 255, empty)
cv2.createTrackbar("sat max", "trackbars", 255, 255, empty)
cv2.createTrackbar("val min", "trackbars", 0, 255, empty)
cv2.createTrackbar("val max", "trackbars", 255, 255, empty)

while True:
    h_min = cv2.getTrackbarPos("hue min", "trackbars")
    h_max = cv2.getTrackbarPos("hue max", "trackbars")
    s_min = cv2.getTrackbarPos("sat min", "trackbars")
    s_max = cv2.getTrackbarPos("sat max", "trackbars")
    v_min = cv2.getTrackbarPos("val min", "trackbars")
    v_max = cv2.getTrackbarPos("val max", "trackbars")
    # print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(hsv_img, lower, upper)
    result = cv2.bitwise_and(original_img, original_img, mask=mask)
    # cv2.imshow("hsv_car", hsv_img)

    # cv2.imshow("original_car", original_img)
    cv2.imshow("result", result)
    cv2.waitKey(1)
