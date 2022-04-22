from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtWidgets import QTableWidgetItem

column_headers = {"my_accounts": ['종목명', '손익금액', '손익율', '매입금액', '보유수량', '평균단가', '현재가'],
                  "search_stocks": ['종목명', '현재가', '등락율', '거래량', '거래대비', '유통비율'], }
column_foreground = ('손익금액', '손익율', '현재가', '등락율', '거래대비')


def binding_tableWidget(widget, data, code):
    headers = column_headers[code]
    widget.setColumnCount(len(headers))
    widget.setRowCount(len(data.index))
    widget.setHorizontalHeaderLabels(headers)

    for index, row in data.iterrows():
        cols = 0
        for column_name in headers:
            value = None
            if column_name in ('손익율', '등락율', '거래대비', '유통비율'):
                value = "%.2f" % (float(row[column_name]) * 0.0001) + "%"
            elif column_name not in '종목명':
                value = format(int(row[column_name]), ',')
            else:
                value = str(row[column_name])

            item = QTableWidgetItem(value)

            if column_name in column_foreground:
                if value.startswith("-"):
                    item.setForeground(QBrush(QColor(0, 0, 255)))
                else:
                    item.setForeground(QBrush(QColor(255, 0, 0)))

            if column_name != "종목명":
                item.setTextAlignment(Qt.AlignVCenter | Qt.AlignRight)

            widget.setItem(index, cols, item)
            cols = cols + 1


def binding_combobox(widget, data):
    widget.addItems(data)
