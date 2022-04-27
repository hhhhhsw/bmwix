import threading

from PyQt5 import uic

from api.api import *
from config import setting
from trade.trade import Trade
from ui.form import FormEventSlot
from util import binding_widget

form_class = uic.loadUiType("ui/main.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.api = Api(self)  # 키움api tr 모음
        self.fes = FormEventSlot(self)  # 화면 위젯 이벤트 모음
        self.tr = Trade(self)  # 화면 위젯 이벤트 모음

        self.fes.onclick_btnmystocks()
        binding_widget.binding_combobox(self.cb_accounts, setting.accno)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
