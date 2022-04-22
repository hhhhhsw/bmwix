from pykiwoom.kiwoom import *

from config import setting


class Api:
    def __init__(self):
        self.kw = Kiwoom()
        self.comm_connect()
        self.get_codelist_market()
        self.get_login_info()
        setting.mystocks = self.get_mystocks(setting.accno[0])

    def comm_connect(self):
        self.kw.CommConnect(block=True)

    def get_login_info(self):
        setting.account_cnt = self.kw.GetLoginInfo("ACCOUNT_CNT")  # 전체 계좌수
        setting.accno = self.kw.GetLoginInfo("ACCNO")  # 전체 계좌 리스트
        setting.select_accno = setting.accno[0]

    def get_mystocks(self, accno):
        df = self.kw.block_request("OPW00004",
                                   계좌번호=accno,
                                   비밀번호="0000",
                                   상장폐지조회구분="0",
                                   비밀번호입력매체구분="00",
                                   output="종목별계좌평가",
                                   next=0,
                                   screen=1000)

        while self.kw.tr_remained:
            df = self.kw.block_request("OPW00004",
                                       계좌번호=accno,
                                       비밀번호="0000",
                                       상장폐지조회구분="0",
                                       비밀번호입력매체구분="00",
                                       output="종목별계좌평가",
                                       next=2,
                                       screen=1000)
            df.concat(df)
            time.sleep(1)

        return df

    def get_codelist_market(self):
        kospi_codes = self.kw.GetCodeListByMarket('0')
        kosdaq_codes = self.kw.GetCodeListByMarket('10')

        for code in kospi_codes:
            name = self.kw.GetMasterCodeName(code)
            setting.dic_stocks[name] = code

        for code in kosdaq_codes:
            name = self.kw.GetMasterCodeName(code)
            setting.dic_stocks[name] = code

        print("setting.dic_stocks : %s" % setting.dic_stocks)

    def get_stock_info(self, code):
        df_stock = self.kw.block_request("opt10001",
                                         종목코드=code,
                                         output="주식기본정보",
                                         next=0,
                                         screen=1001)
        return df_stock

    def buy_send_order(self, code):
        self.kw.SendOrder("시장가매수", "2000", setting.select_accno, 1, code, 10, 0, "03", "")
