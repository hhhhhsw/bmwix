from pykiwoom.kiwoom import *


class Api:
    def __init__(self):
        self.account_cnt = 0
        self.accno = []

        self.kw = Kiwoom()
        self.comm_connect()
        self.get_login_info()

    def comm_connect(self):
        self.kw.CommConnect(block=True)

    def get_login_info(self):
        self.account_cnt = self.kw.GetLoginInfo("ACCOUNT_CNT")  # 전체 계좌수
        self.accno = self.kw.GetLoginInfo("ACCNO")  # 전체 계좌 리스트

    def get_mystocks(self):
        df = self.kw.block_request("OPW00004",
                                   계좌번호=self.accno[0],
                                   비밀번호="0000",
                                   상장폐지조회구분="0",
                                   비밀번호입력매체구분="00",
                                   output="종목별계좌평가",
                                   next=0)

        while self.kw.tr_remained:
            df = self.kw.block_request("OPW00004",
                                       계좌번호=self.accno[0],
                                       비밀번호="0000",
                                       상장폐지조회구분="0",
                                       비밀번호입력매체구분="00",
                                       output="종목별계좌평가",
                                       next=2)
            df.concat(df)
            time.sleep(1)

        return df

    def buy_send_order(self):
        self.kw.SendOrder("시장가매수", "2000", self.accounts[0], 1, "000660", 10, 0, "03", "")

    def get_codelist_market(self):
        kospi = self.kw.GetCodeListByMarket('0')
        kosdaq = self.kw.GetCodeListByMarket('10')

        print("코스피 종목 갯수(%s) 목록 : %s" % (len(kospi), kospi))
        print("코스닷 종목 갯수(%s) 목록 : %s" % (len(kosdaq), kosdaq))
