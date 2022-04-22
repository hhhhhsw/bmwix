from PyQt5 import uic
from api.api import *
from config import setting
from ui.form import FormEventSlot
from util import binding_widget

form_class = uic.loadUiType("ui/main.ui")[0]


class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.api = Api()
        self.fes = FormEventSlot(self)
        # self.api.buy_send_order()

        binding_widget.binding_tableWidget(self.tw_mystocks, setting.mystocks, "my_accounts")
        binding_widget.binding_combobox(self.cb_accounts, setting.accno)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
