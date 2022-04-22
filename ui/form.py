from PyQt5.QtWidgets import QMessageBox

from config import setting
from util import binding_widget


class FormEventSlot:
    def __init__(self, main):
        self.main = main

        self.main.tw_search_stocks.clicked.connect(self.onclick_twsearchstocks)
        self.main.btn_search_stock.clicked.connect(self.onclick_bntsearch)
        self.main.btn_buy0.clicked.connect(self.onclick_btnbuy0)

    def onclick_bntsearch(self):
        setting.select_search_stockname = None
        self.main.tw_search_stocks.clear()
        stock_name = self.main.edt_stockname.text()
        print("종목명 : %s, 종목코드 : %s" % (stock_name, setting.dic_stocks[stock_name]))

        df_stock = self.main.api.get_stock_info(setting.dic_stocks[stock_name])

        binding_widget.binding_tableWidget(self.main.tw_search_stocks, df_stock, "search_stocks")

    def onclick_twsearchstocks(self, clickedIndex):
        row = clickedIndex.row()

        self.main.edt_buy_name.setText(self.main.tw_search_stocks.item(row, 0).text())
        price = self.main.tw_search_stocks.item(row, 1).text().replace(',', '')
        self.main.edt_buy_price.setText(format(int(price), ','))
        buy_count = int(setting.buy_amt / int(price))
        self.main.edt_buy_count.setText(str(buy_count))
        self.main.edt_buy_amt.setText(format(int(price) * buy_count, ','))

    def onclick_btnbuy0(self):
        stockname = self.main.edt_buy_name.text()
        if stockname == "":
            QMessageBox.about(self.main, '알림', '매수할 종목을 선택하세요.')
        else:
            self.main.api.buy_send_order(setting.dic_stocks[stockname])
