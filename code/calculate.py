#!/usr/bin/env python3
# coding:utf-8

from math import sin, cos, tan, pi
import sys
from pathlib import Path
from PyQt5.QtWidgets import *
from PyQt5 import uic


def z_iter(F, T, D, YZ):
    a = ((F - T) // D + 1) * D
    yield a
    while a < YZ:
        a = a + D
        yield a


def calculate(R, F, A1, A2, A3, D):
    if not(R and F and A1 and A2 and A3 and D):
        mb = QMessageBox()
        mb.setText('文本框不能为空!!')
        mb.exec_()
        return
    R, F, A1, A2, A3, D = float(R), float(F), float(A1), float(A2), float(A3), float(D)
    A = (A1 * 3600 + A2 * 60 + A3) / 3600
    T = R * tan(A / 2 * pi / 180)
    L = pi * R * A / 180
    E = R * (1 / cos(A / 2 * pi / 180) - 1)
    Q = 2 * T - L

    li_list = []
    zb_list = []

    ## 主点里程
    li_ZY = F - T
    li_QZ = A / 2 * pi * R / 180 + li_ZY
    li_YZ = F - T + L

    li_list += [li_ZY, li_QZ, li_YZ]

    ## 主点坐标
    zb_ZY = (0, 0)
    zb_QZ = (R * sin((A / 2) * pi / 180), (1 - cos(A / 2 * pi / 180)) * R)
    zb_YZ = (R * sin(A * pi / 180), R * (1 - cos(A * pi / 180)))

    zb_list += [zb_ZY, zb_QZ, zb_YZ]

    ## 桩点里程
    # Z = list(z_iter(F, T, D, li_YZ))
    Z = z_iter(F, T, D, li_YZ)
    lis = list(filter(lambda i: i < li_YZ, Z))

    li_list += lis

    ## 桩点坐标
    for li in lis:
        x = R * sin((li - li_ZY) / R)
        y = R * (1 - cos((li - li_ZY) / R))
        zb_list.append((x, y))

    pj_du_list = [180 / pi / R / 2 * (li - li_ZY) for li in li_list]

    jl_list = ['{:.3f}'.format(2 * R * sin(pj / 2 * pi / 180)) for pj in pj_du_list]

    zb_list = [(float('{:.3f}'.format(x)), float('{:.3f}'.format(y))) for x, y in zb_list]

    li_list = ['{:.3f}'.format(i) for i in li_list]

    # TODO 度转度分秒 °′″
    pj_list = []
    for pj in pj_du_list:
        miao = pj * 3600
        du, yushu1 = miao // 3600, miao % 3600
        fen, yushu2 = yushu1 // 60, yushu1 % 60
        miao = yushu2
        pj_list.append('{:.0f}°{:.0f}′{:.1f}″'.format(du, fen, miao))

    # data = list(zip(li_list, zb_list, pj_list, jl_list))
    data = []
    for i in range(len(li_list)):
        data.append((li_list[i], zb_list[i], pj_list[i], jl_list[i]))
    return data, T, L, E, Q


class CacWidget(QWidget):

    def __init__(self, parent=None):
        super(CacWidget, self).__init__(parent)
        self.ui = uic.loadUi(str(Path(__file__).parent.parent / 'ui' / 'calculate2.ui'), self)
        self.set_ui()
        # self.show_in_view([['a', 'b', 'c', 'd'], ['q', 'w', 'e', 'r']])

    def set_ui(self):
        self.setWindowTitle('圆曲线计算程序')
        self.ui.btn_calc.clicked.connect(self.calculate)
        self.ui.btn_clear.clicked.connect(self.clear)

    def calculate(self):
        R = self.ui.edit_R.text()
        F = self.ui.edit_F.text()
        A1 = self.ui.edit_A1.text()
        A2 = self.ui.edit_A2.text()
        A3 = self.ui.edit_A3.text()
        D = self.ui.edit_D.text()
        data, T, L, E, Q = calculate(R, F, A1, A2, A3, D)
        self.show_in_view(data, T, L, E, Q)
        # self.show_in_view([['c', 'b', 'c', 'e'], ['q', 'w', 'e', 'r']])

    def show_in_view(self, data, T, L, E, Q):
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

        # other input
        self.ui.edit_T.setText(str(T))
        self.ui.edit_L.setText(str(L))
        self.ui.edit_E.setText(str(E))
        self.ui.edit_Q.setText(str(Q))

    def clear(self):
        self.ui.edit_R.clear()
        self.ui.edit_F.clear()
        self.ui.edit_A1.clear()
        self.ui.edit_A2.clear()
        self.ui.edit_A3.clear()
        self.ui.edit_D.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    cw = CacWidget()
    cw.show()
    sys.exit(app.exec())
