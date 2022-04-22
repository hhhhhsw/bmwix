import math
import sys

from PyQt5.QtGui import QBrush, QColor
from PyQt5 import uic
from api.api import *
from PyQt5.QtCore import *

form_class = uic.loadUiType("ui/main.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.api = Api()
        self.df = self.api.get_mystocks()
        self.set_account_tablewidget_binding()

    def set_account_tablewidget_binding(self):
        column_headers = ['종목명', '손익금액', '손익율', '매입금액', '보유수량', '평균단가', '현재가']
        self.tableWidget.setColumnCount(len(column_headers))
        self.tableWidget.setRowCount(len(self.df.index))
        self.tableWidget.setHorizontalHeaderLabels(column_headers)

        for index, row in self.df.iterrows():
            cols = 0
            for column_name in column_headers:
                value = None
                if column_name == "손익율":
                    value = "%.2f" % (float(row[column_name]) * 0.0001) + "%"
                elif column_name == "손익금액":
                    value = "%.0f" % (float(row[column_name]))
                else:
                    value = str(row[column_name]).lstrip('0')

                item = QTableWidgetItem(value)
                if value.startswith("-"):
                    item.setForeground(QBrush(QColor(0, 0, 255)))
                elif value == "0":
                    item.setForeground(QBrush(QColor(255, 0, 0)))

                if column_name != "종목명":
                    item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

                self.tableWidget.setItem(index, cols, item)
                cols = cols + 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()