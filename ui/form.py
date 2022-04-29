from PyQt5.QtWidgets import QMessageBox, QCompleter

from config import setting
from util import binding_widget


class FormEventSlot:
    def __init__(self, main):
        self.main = main

        self.main.btn_buy0.clicked.connect(self.onclick_btnbuy0)  # 매수 버튼 클릭
        self.main.btn_mystocks.clicked.connect(self.onclick_btnmystocks)  # 보유종목 검색 버튼 클릭
        self.main.tw_search_stocks.cellClicked.connect(self.onclick_twsearchstocks)  # 종목 현황 테이블 클릭

        self.main.buy_count.valueChanged.connect(self.onchange_buycount)  # 매수 수량 변경

        self.main.edt_stockname.returnPressed.connect(self.onenter_edtstockname)  # 검색 종목명 변경
        self.main.lw_search_stocks.itemClicked.connect(self.onitemclick_lwsearchstocks)  # 종목 리스트 클릭

    def onenter_edtstockname(self):
        '''
        검색할 종목명 엔터
        :return: 
        '''
        self.main.lw_search_stocks.clear()
        search_word = self.main.edt_stockname.text()
        print("search_word : %s, len(search_word) : %s" % (search_word, len(search_word)))
        if len(search_word) > 1:
            search_stock_list = [stock for stock in setting.dic_stocks if search_word in stock]
            print("search_stock_list : %s" % search_stock_list)
            if len(search_stock_list) > 0:
                self.main.lw_search_stocks.addItems(search_stock_list)

                if len(search_stock_list) == 1:
                    self.main.lw_search_stocks.setCurrentRow(0)
                    self.onitemclick_lwsearchstocks()

    def onitemclick_lwsearchstocks(self):
        '''
        종목 검색 리스트 클릭
        :return: 
        '''
        self.main.tw_search_stocks.clear()

        stockname = self.main.lw_search_stocks.currentItem().text()
        code = setting.dic_stocks[stockname]
        df_stock = self.main.api.get_stock_info(code)  # 종목 정보 검색
        binding_widget.binding_tableWidget(self.main.tw_search_stocks, df_stock, "search_stocks")  # 검새된 종목 바인딩

    def onchange_buycount(self):
        '''
        매수 수량 수정
        :return: 
        '''
        count = int(self.main.buy_count.value())
        price = int(self.main.edt_buy_price.text().replace(',', ''))

        self.main.edt_buy_amt.setText(format(count * price, ','))

    def onclick_btnmystocks(self):
        '''
        보유 종목 검색 버튼 클릭
        :return: 
        '''
        print("보유종목 검색 클릭")
        df_mystocks = self.main.api.get_mystocks(setting.accno[0])
        binding_widget.binding_tableWidget(self.main.tw_mystocks, df_mystocks, "my_accounts")
        self.main.api.set_real_reg_mystocks(df_mystocks)

        ### 실시간 체결에 있어야함.

    def onclick_twsearchstocks(self, row):
        '''
        검색한 종목의 현재가 table을 클릭
        :param row: 
        :return: 
        '''
        stockname = self.main.tw_search_stocks.item(row, 0).text()
        price = self.main.tw_search_stocks.item(row, 1).text().replace(',', '')
        cnt = int(setting.buy_amt / int(price))
        amt = int(price) * cnt

        self.main.edt_buy_name.setText(stockname)
        self.main.edt_buy_price.setText(format(int(price), ','))
        self.main.buy_count.setValue(cnt)
        self.main.edt_buy_amt.setText(format(amt, ','))

    def onclick_btnbuy0(self):
        '''
        시장가 매수 버튼 클릭
        :return: 
        '''
        stockname = self.main.edt_buy_name.text()
        if stockname == "":
            QMessageBox.about(self.main, '알림', '매수할 종목을 선택하세요.')
        else:
            self.main.api.buy0_send_order(setting.dic_stocks[stockname], self.main.buy_count.text())
