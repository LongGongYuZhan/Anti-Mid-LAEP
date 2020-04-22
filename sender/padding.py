#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2

img = cv2.imread(r"C:\Users\Administrator\Desktop\timg.jpg")
height, weight = img.shape[: 2]

if height > weight:
    pad = height - weight
    img_new = cv2.copyMakeBorder(img, 0, 0, 0, pad, cv2.BORDER_CONSTANT)  # 上下左右
else:
    pad = weight - height
    img_new = cv2.copyMakeBorder(img, pad, 0, 0, 0, cv2.BORDER_CONSTANT)  # 上下左右

cv2.namedWindow('test2', cv2.WINDOW_NORMAL)
cv2.imshow('test2', img_new)
cv2.waitKey()
# cv2.imwrite(r'C:\Users\Administrator\Desktop\test.jpg', img_new)
