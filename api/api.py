from PyQt5.QtGui import QColor, QBrush
from pykiwoom.kiwoom import *

from config import setting
from util import binding_widget


class Api:
    def __init__(self, main):

        self.main = main
        self.fid_list = ["10", "12", "30", "25"]

        self.kw = Kiwoom()
        self.comm_connect()
        self.get_codelist_market()
        self.get_login_info()

        self.kw.ocx.OnReceiveRealData.connect(self._handler_real_data)

    def comm_connect(self):
        '''
        로그인
        :return:
        '''
        self.kw.CommConnect(block=True)

    def get_login_info(self):
        '''
        로그인 정보
          1. 계좌정보
        :return:
        '''
        setting.account_cnt = self.kw.GetLoginInfo("ACCOUNT_CNT")  # 전체 계좌수
        setting.accno = self.kw.GetLoginInfo("ACCNO")  # 전체 계좌 리스트
        setting.select_accno = setting.accno[0]

    def get_mystocks(self, accno):
        '''
        보유 종목 목록
        param accno:
        :return:
        '''
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
        '''
        시장 전체 종목 목록,
        setting.dic_stocks : {'동화약품': '000020', 'KR모터스': '000040',
        :return:
        '''
        kospi_codes = self.kw.GetCodeListByMarket('0')
        kosdaq_codes = self.kw.GetCodeListByMarket('10')

        for code in kospi_codes:
            name = self.kw.GetMasterCodeName(code)
            setting.dic_stocks[name] = code
            setting.dic_stocks_code[code] = name

        for code in kosdaq_codes:
            name = self.kw.GetMasterCodeName(code)
            setting.dic_stocks[name] = code
            setting.dic_stocks_code[code] = name

        print("setting.dic_stocks : %s" % setting.dic_stocks)

    def get_stock_info(self, code):
        '''
        코드에 맞는 종목 현재 종목정보 검색
        :param code:
        :return:
        '''
        df_stock = self.kw.block_request("opt10001",
                                         종목코드=code,
                                         output="주식기본정보",
                                         next=0,
                                         screen=1001)
        return df_stock

    def buy0_send_order(self, code):
        '''
        시장가 매수
        :param code:
        :return:
        '''
        self.kw.SendOrder("시장가매수", "2000", setting.select_accno, 1, code, 10, 0, "03", "")

    def sell_send_order(self, accno, order_type, code, quantity, price, hoga):
        '''
        시장가 매도
        :param code:
        :return:
        '''
        self.kw.SendOrder("시장가매도", "2000", accno, order_type, code, quantity, price, hoga, "")

    def buy0_send_order(self, code):
        '''
        시장가 매수
        :param code:
        :return:
        '''
        self.kw.SendOrder("시장가매수", "2000", setting.select_accno, 1, code, 10, 0, "03", "")

    def set_real_reg_mystocks(self, df_mystocks):
        print("보유종목 실시간 체결 등록")
        self.kw.SetRealRemove("ALL", "ALL");  # 모든 화면에서 모든종목 실시간 해지
        stocks_code = []
        for index, row in df_mystocks.iterrows():
            stocks_code.append(setting.dic_stocks[row['종목명']])

        self.kw.SetRealReg("3001", ";".join(stocks_code), ";".join(self.fid_list), 0)

    def _handler_real_data(self, code, real_type, data):
        '''
        체결 실시간 데이터
        :param code:
        :param real_type:
        :param data:
        :return:
        '''
        if real_type == "주식체결":
            stockname = setting.dic_stocks_code[code]
            mystocks_realdata = [stockname]  # 실시간 종목정보 [종목명, 현재가, 등락율, 거래대비, 전일대비기호]
            for fid in self.fid_list:
                mystocks_realdata.append(self.kw.GetCommRealData(code, int(fid)))

            # print("[실시간 체결 응답 : api._handler_real_data] : %s" % mystocks_realdata)

            binding_widget.binding_mystocks_realdata(self.main.tw_mystocks, mystocks_realdata)

            # 손익율이 목표수익율을 넘으면 시장가 매도
            mystock_data = {}  # 보유 종목 중 체결된 종목의 현재정보 저장
            row_num = setting.dic_mystocks_tablewidget_index[stockname]
            for cols in range(self.main.tw_mystocks.columnCount()):
                column_header = setting.column_headers["my_accounts"][cols]  # 보유종목 테이블 헤더
                item = self.main.tw_mystocks.item(row_num, cols)  # 보유종목 테이블 item
                if item is not None:
                    mystock_data[column_header] = item.text().replace(",", "").replace("%", "")
                else:
                    mystock_data[column_header] = ""
            self.main.tr.trading(mystock_data)

