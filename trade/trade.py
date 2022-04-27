from config import setting


class Trade:
    def __init__(self, main):

        self.main = main

        self.mystocks = {}

        self.sell_rate = setting.sell_rate  # 목표 수익율
        self.add_buy_rate = setting.add_buy_rate = 10  # 추가 매수 손실율
        self.trade_high = setting.trade_high = 9  # 9%이상 수익 후
        self.trade_stop = setting.trade_stop = 5  # 5%이하로 내려올 때 매도

    def trading(self, stock_info):
        '''
        현재 수익율을 보고 매수 매도 판단
        ['대동스틸', '2,961', '3.78%', '78,400', '10', '7,840', '8,210', '', '', '']
        :param stock_info:
        :return:
        '''
        # print("Trade.trading 실시간 체결 후 거래조건 확인 : %s" % stock_info)
        code = setting.dic_stocks[stock_info["종목명"]]  # 코드
        quantity = int(stock_info["보유수량"])  # 보유수량
        up_rate = float(stock_info["손익율"])  # 손익율
        price = ""
        hoga = "03"

        if self.sell_rate < up_rate and quantity > 0:
            print("목표 수익율 도달 : [종목명 : %s], [손익율 : %s], [수익금 : %s]" %
                  (stock_info["종목명"], str(up_rate)+"%", format(int(stock_info["손익금액"]), ',')))
            # accno, order_type, code, quantity, price, hoga
            self.main.api.sell_send_order(setting.select_accno, "2", code, quantity, price, hoga)

