
account_cnt = 0
accno = []
mystocks = None

dic_stocks = {}

select_search_stockname = None  # 검색 종목 목록에서 선택한 종목
select_accno = None  # 선택한 계좌번호

sell_rate = 10  # 목표 수익율
add_buy_rate = 10  # 추가 매수 손실율
trade_high = 9  # 9%이상 수익 후
trade_stop = 5  # 5%이하로 내려올 때 매도


buy_amt = 110000  # 종목당 매수 금액


