account_cnt = 0
accno = []
mystocks = None


column_headers = {"my_accounts": ['종목명', '손익금액', '손익율', '매입금액', '보유수량', '평균단가', '현재가', '등락율', '거래대비', '전일대비기호'],
                  "search_stocks": ['종목명', '현재가', '등락율', '거래량', '거래대비', '유통비율'], }
column_foreground = ('손익금액', '손익율', '현재가', '등락율', '거래대비')

dic_stocks = {}  # 종목명 : code
dic_stocks_code = {}  # code : 종목명
dic_mystocks_tablewidget_index = {}

select_accno = None  # 선택한 계좌번호

sell_rate = 5.00  # 목표 수익율
add_buy_rate = 10.00  # 추가 매수 손실율
trade_high = 9.00  # 9%이상 수익 후
trade_stop = 5.00  # 5%이하로 내려올 때 매도

buy_amt = 110000  # 종목당 매수 금액
