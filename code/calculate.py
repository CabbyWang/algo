#!/usr/bin/env python3
# coding:utf-8

from math import sin, cos, tan, pi, atan, sqrt
import sys
import click
from PyQt5.QtWidgets import *


def z_iter(F, T, D, HZ):
    a = ((F - T) // D + 1) * D
    yield a
    while a < HZ:
        a = a + D
        yield a


def main():
    F = 1
    R = 2
    A1 = 3
    A2 = 3
    A3 = 3
    L = 4
    D = 5
    p = 206265
    A = (A1 * 3600 + A2 * 60 + A3) / 3600
    B = L / (2 * R) * p
    m = L / 2 - pow(L, 3) / (240 * pow(R, 2))
    P = pow(L, 2) / (24 * R)
    T = (R + P) * m * tan(A / 2)
    l = pi * R * (A - 2 * B) / 180 + 2 * L
    E = (R + P) * (1 / cos(A / 2)) - R
    Q = 2 * T - L

    ## 主点里程
    li_ZH = F - T
    li_HY = li_ZH + L
    li_QZ = li_HY + (A / 2 - B) * pi * R / 180
    li_YH = li_HY + (A - 2 * B) * pi * R / 180
    li_HZ = li_ZH + 2 * L + (A - 2 * B) * pi * R / 180

    ## 主点坐标
    zb_ZH = (0, 0)
    zb_HY = (L - pow(L, 3) / (40 * pow(R, 2)), pow(L, 2) / 6 / R)
    zb_QZ = (R * sin(A) + m, R - cos(A / 2) * R + P)
    zb_YH = (sin(180 - A) + m, cos(180 - A) + R + P)
    zb_HZ = ((cos(A) + 1) * T, sin(A) * T)

    ## 桩点里程
    Z = list(z_iter(F, T, D, li_HZ))
    lis_1 = list(filter(lambda x: x < li_HY, Z))
    lis_2 = list(filter(lambda x: x > li_HY and x < li_YH, Z))
    lis_3 = list(filter(lambda x: x < li_YH and x < li_HZ, Z))

    ## 桩点坐标
    # 第一段, 对应lis_1
    zb_1_list = []
    for li1 in lis_1:
        temp = li1 - (F - T)
        x = temp - pow(temp, 5) / (40 * pow(R, 2) * pow(L, 2))
        y = pow(temp, 3) / (6 * R * L)
        zb_1_list.append((x, y))
    # 偏角
    painjiao_list1 = [atan(y / x) * 180 / pi for x, y in zb_1_list]
    # 距离
    juli1 = [sqrt(pow(x, 2) + pow(y, 2)) for x, y in zb_1_list]

    # 第二段，对应lis_2
    zb_2_list = []
    for li2 in lis_2:
        temp = 180 / (pi * R) * (li2 - F + T - L) + B
        x = R * sin(temp) + m
        y = R * (1 - cos(temp)) + P
        zb_2_list.append((x, y))
    # 偏角
    painjiao_list2 = [atan(y / x) * 180 / pi for x, y in zb_2_list]
    # 距离
    juli2 = [sqrt(pow(x, 2) + pow(y, 2)) for x, y in zb_2_list]

    # 第三段, 对应lis_3
    zb_3_list = []
    for li3 in lis_3:
        temp = li_HZ - li3
        x0 = temp - pow(temp, 5) / (40 * pow(R, 2) * pow(L, 2))
        y0 = pow(temp, 3) / (6 * R * L)
        # 转换坐标系
        xi = y0 * sin(-A) - x0 * cos(-A) + zb_HZ[0]
        yi = y0 * cos(-A) + x0 * sin(-A) + zb_HZ[1]
    # 偏角
    painjiao_list3 = [atan(y / x) * 180 / pi for x, y in zb_3_list]
    # 距离
    juli3 = [sqrt(pow(x, 2) + pow(y, 2)) for x, y in zb_3_list]


class CacWidget(QWidget):

    def __init__(self, parent=None):
        self.setWindowTitle('缓和曲线计算程序')
        self.set_ui()

    def set_ui(self):
        main_layout = QHBoxLayout()
        cal_groupbox = QGroupBox('输入')
        label1 = QLabel('交点里程（F）：( K + ')
        f_edit = QLineEdit()
        label11 = QLabel('m)')
        label2 = QLabel('圆曲线半径（R）')
        r_edit = QLineEdit()
        label22 = QLabel('(m)')
        label3 = QLabel('转角（a）')




if __name__ == "__main__":
    # main()
    a = z_iter(1, 2, 3)
    print(list(a))
    print(list(a))
    print(list(a))
    print(list(a))
