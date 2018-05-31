#!/usr/bin/env python3
# coding:utf-8

from math import sin, cos, tan, pi, atan, sqrt
import sys
import click
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QModelIndex
from PyQt5 import uic


def z_iter(F, T, D, HZ):
    a = ((F - T) // D + 1) * D
    yield a
    while a < HZ:
        a = a + D
        yield a


def calculate(R, F, A1, A2, A3, L, D):
    if not(R and F and A1 and A2 and A3 and L and D):
        mb = QMessageBox()
        mb.setText('文本框不能为空!!')
        mb.exec_()
        return
    R, F, A1, A2, A3, L, D = float(R), float(F), float(A1), float(A2), float(A3), float(L), float(D)
    p = 206265
    A = (A1 * 3600 + A2 * 60 + A3) / 3600
    B = L / (2 * R) * p / 3600
    m = L / 2 - pow(L, 3) / (240 * pow(R, 2))
    P = pow(L, 2) / (24 * R)
    T = m + (R + P) * tan(A / 2 * pi / 180)
    l = pi * R * (A - 2 * B) / 180 + 2 * L
    E = (R + P) * (1 / cos(A / 2 * pi / 180)) - R
    Q = 2 * T - L

    li_list = []
    zb_list = []

    ## 主点里程
    li_ZH = F - T
    li_HY = li_ZH + L
    li_QZ = li_HY + (A / 2 - B) * pi * R / 180
    li_YH = li_HY + (A - 2 * B) * pi * R / 180
    li_HZ = li_ZH + 2 * L + (A - 2 * B) * pi * R / 180

    li_list += [li_ZH, li_HY, li_QZ, li_YH, li_HZ]

    ## 主点坐标
    zb_ZH = (0, 0)
    zb_HY = (L - pow(L, 3) / (40 * pow(R, 2)), pow(L, 2) / 6 / R)
    zb_QZ = (R * sin(A / 2 * pi / 180) + m, R - cos(A / 2 * pi / 180) * R + P)
    zb_YH = (R * sin((A - B) * pi / 180) + m, R * (1 - cos((A - B) * pi / 180)) + P)
    zb_HZ = ((cos(A * pi / 180) + 1) * T, sin(A * pi / 180) * T)

    zb_list += [zb_ZH, zb_HY, zb_QZ, zb_YH, zb_HZ]

    ## 桩点里程
    Z = list(z_iter(F, T, D, li_HZ))
    lis_1 = list(filter(lambda i: i < li_HY, Z))
    lis_2 = list(filter(lambda i: li_HY < i < li_YH, Z))
    lis_3 = list(filter(lambda i: li_YH < i < li_HZ, Z))

    li_list += lis_1 + lis_2 + lis_3

    ## 桩点坐标
    # 第一段, 对应lis_1
    zb_1_list = []
    for li1 in lis_1:
        temp = li1 - (F - T)
        x = temp - pow(temp, 5) / (40 * pow(R, 2) * pow(L, 2))
        y = pow(temp, 3) / (6 * R * L)
        zb_1_list.append((x, y))
    # 偏角
    # painjiao_list1 = [atan(y / x) * 180 / pi for x, y in zb_1_list]
    # 距离
    # juli1 = [sqrt(pow(x, 2) + pow(y, 2)) for x, y in zb_1_list]
    zb_list += zb_1_list

    # 第二段，对应lis_2
    zb_2_list = []
    for li2 in lis_2:
        temp = 180 / (pi * R) * (li2 - F + T - L) + B
        x = R * sin(temp * pi / 180) + m
        y = R * (1 - cos(temp * pi / 180)) + P
        zb_2_list.append((x, y))
    # 偏角
    # painjiao_list2 = [atan(y / x) * 180 / pi for x, y in zb_2_list]
    # 距离
    # juli2 = [sqrt(pow(x, 2) + pow(y, 2)) for x, y in zb_2_list]
    zb_list += zb_2_list

    # 第三段, 对应lis_3
    zb_3_list = []
    for li3 in lis_3:
        temp = li_HZ - li3
        x0 = temp - pow(temp, 5) / (40 * pow(R, 2) * pow(L, 2))
        y0 = pow(temp, 3) / (6 * R * L)
        # 转换坐标系
        x = y0 * sin(-A * pi / 180) - x0 * cos(-A * pi / 180) + zb_HZ[0]
        y = y0 * cos(-A * pi / 180) + x0 * sin(-A * pi / 180) + zb_HZ[1]
        zb_3_list.append((x, y))
    # 偏角
    # painjiao_list3 = [atan(y / x) * 180 / pi for x, y in zb_3_list]
    # 距离
    # juli3 = [sqrt(pow(x, 2) + pow(y, 2)) for x, y in zb_3_list]
    zb_list += zb_3_list

    pj_du_list = [0] + [atan(y / x) * 180 / pi for x, y in zb_list if x != 0]

    # TODO 度转度分秒 °′″
    pj_list = []
    for pj in pj_du_list:
        miao = pj * 3600
        du, yushu1 = miao // 3600, miao % 3600
        fen, yushu2 = yushu1 // 60, yushu1 % 60
        miao = yushu2
        pj_list.append('{:.0f}°{:.0f}′{:.1f}″'.format(du, fen, miao))

    jl_list = [0] + ['{:.3f}'.format(sqrt(pow(x, 2) + pow(y, 2))) for x, y in zb_list if x != 0]

    zb_list = [(float('{:.3f}'.format(x)), float('{:.3f}'.format(y))) for x, y in zb_list]

    li_list = ['{:.3f}'.format(i) for i in li_list]

    data = []
    for i in range(len(li_list)):
        data.append((li_list[i], zb_list[i], pj_list[i], jl_list[i]))
    return data


class CacWidget(QWidget):

    def __init__(self, parent=None):
        super(CacWidget, self).__init__(parent)
        self.ui = uic.loadUi(str(Path(__file__).parent.parent / 'ui' / 'calculate.ui'), self)
        self.set_ui()
        # self.show_in_view([['a', 'b', 'c', 'd'], ['q', 'w', 'e', 'r']])

    def set_ui(self):
        self.setWindowTitle('缓和曲线计算程序')
        self.ui.btn_calc.clicked.connect(self.calculate)
        self.ui.btn_clear.clicked.connect(self.clear)

    def calculate(self):
        R = self.ui.edit_R.text()
        F = self.ui.edit_F.text()
        A1 = self.ui.edit_A1.text()
        A2 = self.ui.edit_A2.text()
        A3 = self.ui.edit_A3.text()
        L = self.ui.edit_L.text()
        D = self.ui.edit_D.text()
        data = calculate(R, F, A1, A2, A3, L, D)
        self.show_in_view(data)
        # self.show_in_view([['c', 'b', 'c', 'e'], ['q', 'w', 'e', 'r']])

    def show_in_view(self, data):
        table_widget = self.ui.table_widget
        table_widget.clear()
        # table = QTableWidget()
        # table.setEditTriggers()
        table_widget.setColumnCount(4)
        table_widget.setRowCount(len(data))
        table_widget.setHorizontalHeaderLabels(['里程', '坐标', '偏角', '弦长'])
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem('{}'.format(value))
                table_widget.setItem(row, col, item)

    def clear(self):
        self.ui.edit_R.clear()
        self.ui.edit_F.clear()
        self.ui.edit_A1.clear()
        self.ui.edit_A2.clear()
        self.ui.edit_A3.clear()
        self.ui.edit_L.clear()
        self.ui.edit_D.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cw = CacWidget()
    cw.show()
    sys.exit(app.exec())
