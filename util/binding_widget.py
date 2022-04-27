from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QTableWidgetItem

from config import setting


def binding_tableWidget(widget, data, code):
    print("보유종목 테이블 바인딩")
    widget.clear()
    headers = setting.column_headers[code]
    widget.setColumnCount(len(headers))
    widget.setRowCount(len(data.index))
    widget.setHorizontalHeaderLabels(headers)

    for index, row in data.iterrows():
        cols = 0
        for column_name in headers:
            if column_name not in data.columns:
                continue

            qcolor = QColor(0, 0, 0)
            value = None
            if column_name in ('손익율'):
                value = "%.2f" % (float(row[column_name]) * 0.0001) + "%"
            elif column_name in ( '등락율', '거래대비', '유통비율'):
                value = "%.2f" % float(row[column_name]) + "%"
            elif column_name not in '종목명':
                value = format(int(row[column_name]), ',')
            else:
                value = str(row[column_name])

            # 등락 font 색
            if column_name in setting.column_foreground:
                if value.startswith("-"):
                    qcolor = QColor(0, 0, 255)
                else:
                    qcolor = QColor(255, 0, 0)

            # 현재가 -+ 제거
            if column_name == "현재가":
                value = value.replace("-", "").replace("+", "")

            item = QTableWidgetItem(value)  # item 생성
            item.setForeground(QBrush(qcolor))  # font 색

            # text 정렬
            if column_name != "종목명":
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)
            else:
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignCenter)
                setting.dic_mystocks_tablewidget_index[value] = index

            widget.setItem(index, cols, item)
            cols = cols + 1


def binding_combobox(widget, data):
    widget.addItems(data)


def binding_mystocks_realdata(widget, datas):

    row_num = setting.dic_mystocks_tablewidget_index[datas[0]]

    # 현재가
    for i in range(6, 10):
        value = datas[1]

        if value.startswith("-"):
            qcolor = QColor(0, 0, 255)
        else:
            qcolor = QColor(255, 0, 0)

        if i == 6:  # 현재가
            value = datas[1].replace("-", "").replace("+", "")
            value = format(int(value), ',')
        elif i == 7 or i == 8:  # 등락율
            value = datas[2] + "%"
        else:
            value = datas[4]

        item = QTableWidgetItem(value)
        item.setForeground(QBrush(qcolor))
        item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

        widget.setItem(row_num, i, QTableWidgetItem(item))  # 현재가
