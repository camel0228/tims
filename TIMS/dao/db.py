import pymssql, pyodbc, datetime
from model import trade,security,fund,currency,counterparty,config,frontQuery,tradeBlotter, \
    report,priceHistory,openPosition,frontSummary,tradeClose,realizedGL,accountHistory, \
    investHistory, frontInvestPNL, riskManagement, message

class DbConn:
    def __init__(self):
#         self.__con = pymssql.connect(host="127.0.0.1:1433", user="sa", password="Heron7056", database="CCM", charset="UTF-8")
        self.__con = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=127.0.0.1;PORT=1433;DATABASE=CCM;UID=sa;PWD=Heron7056;TDS_Version=7.0')
        self.__cur = self.__con.cursor()
        settleList = self.qTradeBySettleDt()
        if len(settleList) != 0:
            for i in settleList:
                self.dTrade(i)

    def __del__(self):
        self.__cur.close()
        self.__con.close()
    
    def commitment(self):
        self.__con.commit()

    def qISINFromTradeHistory(self):
        listResult = list()
        sql = "select distinct ISIN from dbo.tradehistory"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = i[0]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryBySecurityName(self, securityName):
        listResult = list()
        sql = "select * from dbo.tradehistory where securityName = ?"
        self.__cur.execute(sql, securityName)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByISIN(self, ISIN, tranType):
        listResult = list()
        sql = "select * from dbo.tradehistory where ISIN = ? and tranType = ? and reserve4 != 'CLOSED'"
        self.__cur.execute(sql, ISIN, tranType)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByDate(self, ISIN, tranType, tradeDate):
        listResult = list()
        sql = "select * from dbo.tradehistory where ISIN = ? and tranType = ? and reserve4 != 'CLOSED' and tradeDate = ?" 
        self.__cur.execute(sql, ISIN, tranType, tradeDate)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryBeforeDate(self, tradeDate):
        listResult = list()
        sql = "select * from dbo.tradehistory where tradeDate <= ?" 
        self.__cur.execute(sql, tradeDate)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByFundName(self, fundName):
        listResult = list()
        sql = "select * from tradehistory where fundName = ? order by tradeDate desc"
        self.__cur.execute(sql, fundName)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = round(i[11], 2)
            result.y = i[12]
            result.quantity = format(int(i[13]), ',')
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = format(round(i[19], 2), ',')
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            
            tempDate = datetime.datetime.strptime(str(i[26]), '%Y-%m-%d')
            year = str(tempDate.year)
            month = str(tempDate.month)
            day = str(tempDate.day)
            result.tradeDate = month + '/' + day + '/' + year
            
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByDateRange(self, fundName, startDate, endDate):
        listResult = list()
        sql = "select * from tradehistory where fundName = ? and tradeDate >= ? and tradeDate <= ? order by tradeDate desc"
        self.__cur.execute(sql, fundName, startDate, endDate)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = round(i[11], 2)
            result.y = i[12]
            result.quantity = format(int(i[13]), ',')
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = format(round(i[19], 2), ',')
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            
            tempDate = datetime.datetime.strptime(str(i[26]), '%Y-%m-%d')
            year = str(tempDate.year)
            month = str(tempDate.month)
            day = str(tempDate.day)
            result.tradeDate = month + '/' + day + '/' + year
            
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qFuzzyTradeHistory(self, criteria):
        listResult = list()
        sql = "select * from tradehistory where tranType like '%%%s%%' or ISIN like '%%%s%%' or securityName like '%%%s%%' \
                or quantity like '%%%s%%' or price like '%%%s%%' or currType like '%%%s%%' \
                or brokerName like '%%%s%%' order by tradeDate desc" \
                % (criteria, criteria, criteria, criteria, criteria, criteria, criteria)
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = round(i[11], 2)
            result.y = i[12]
            result.quantity = format(int(i[13]), ',')
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = format(round(i[19], 2), ',')
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            
            tempDate = datetime.datetime.strptime(str(i[26]), '%Y-%m-%d')
            year = str(tempDate.year)
            month = str(tempDate.month)
            day = str(tempDate.day)
            result.tradeDate = month + '/' + day + '/' + year
            
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByCriteria(self, t):
        listResult = list()
        sql = "select * from dbo.tradehistory where securityName = ? and fundName = ?"
        self.__cur.execute(sql, t.securityName, t.fundName)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByCriteria2(self, t):
        listResult = list()
        sql = "select * from dbo.tradehistory where ISIN = ? and fundName = ? and tranType = ? and side = ? \
                and reserve4 != 'CLOSED' order by tradeDate asc"
        self.__cur.execute(sql, t.ISIN, t.fundName, t.tranType, t.side)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = str(i[26])
            result.issueDate = str(i[27])
            result.settleDate = str(i[28])
            result.matureDate = str(i[29])
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByCriteria3(self, t):
        listResult = list()
        sql = "select * from TRADEHISTORY where ISIN = ? and tranType = ? and fundName = ? \
                and side = ? and reserve4 != 'CLOSED' and datediff(DAY, tradeDate, ?) < 365 \
                and (? - net) < 0 order by tradeDate desc"
        self.__cur.execute(sql, t.ISIN, t.tranType, t.fundName, t.side, t.tradeDate,t.net)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = str(i[26])
            result.issueDate = str(i[27])
            result.settleDate = str(i[28])
            result.matureDate = str(i[29])
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByCriteria4(self, t):
        listResult = list()
        sql = "select * from TRADEHISTORY where ISIN = ? and tranType = ? and fundName = ? and side = ? \
                and reserve1 = ? and tradeDate = ?"
        self.__cur.execute(sql, t.ISIN, t.tranType, t.fundName, t.side, t.quantity, t.tradeDate)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = str(i[26])
            result.issueDate = str(i[27])
            result.settleDate = str(i[28])
            result.matureDate = str(i[29])
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByCriteria5(self, tranType):
        listResult = list()
        sql = "select * from dbo.tradehistory where tranType = ? and reserve4 != 'CLOSED'"
        self.__cur.execute(sql, tranType)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = str(i[26])
            result.issueDate = str(i[27])
            result.settleDate = str(i[28])
            result.matureDate = str(i[29])
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryByCriteria6(self, ISIN, tranType):
        listResult = list()
        sql = "select * from dbo.tradehistory where ISIN = ? and tranType = ? and reserve4 != 'CLOSED'"
        self.__cur.execute(sql, ISIN, tranType)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = str(i[26])
            result.issueDate = str(i[27])
            result.settleDate = str(i[28])
            result.matureDate = str(i[29])
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryForCREPO(self, t):
        listResult = list()
        sql = "select * from TRADEHISTORY where ISIN = ? and tranType = 'REPO' and fundName = ? and tradeDate = ? \
                and reserve3 = ? and reserve4 != 'CLOSED'"
        self.__cur.execute(sql, t.ISIN, t.fundName, t.tradeDate, t.reserve3)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = str(i[26])
            result.issueDate = str(i[27])
            result.settleDate = str(i[28])
            result.matureDate = str(i[29])
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeHistoryForCREPO2(self, t):
        listResult = list()
        sql = "select * from dbo.tradehistory where ISIN = ? and fundName = ? and tranType = 'REPO' \
                and reserve3 = ? and reserve4 != 'CLOSED' order by tradeDate asc"
        self.__cur.execute(sql, t.ISIN, t.fundName, t.reserve3)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = str(i[26])
            result.issueDate = str(i[27])
            result.settleDate = str(i[28])
            result.matureDate = str(i[29])
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qISINFromTradeHistoryForFut(self):
        listResult = list()
        sql = "select distinct ISIN from TRADEHISTORY where tranType = 'FUT' and reserve4 != 'CLOSED'"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = i[0]
            listResult.append(result)
        return listResult

    def qTradeBySecurityName(self, securityName):
        listResult = list()
        sql = "select * from dbo.trade where securityName = ?"
        self.__cur.execute(sql, securityName)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeByCriteria(self, t):
        listResult = list()
        sql = "select * from dbo.trade where securityName = ? and fundName = ?"
        self.__cur.execute(sql, t.securityName, t.fundName)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeByCriteria2(self, t):
        listResult = list()
        sql = "select * from dbo.trade where ISIN = ? and fundName = ? and tranType= ? order by tradeDate asc" 
        self.__cur.execute(sql, t.ISIN, t.fundName, t.tranType)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = str(i[26])
            result.issueDate = str(i[27])
            result.settleDate = str(i[28])
            result.matureDate = str(i[29])
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeBySettleDt(self):
        listResult = list()
        sql = "select * from TRADE where settleDate < GETDATE() and tranType = 'FX'"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeByFundName(self, fundName, tradeDate):
        listResult = list()
        sql = "select * from TRADEHISTORY where tradeDate >= ? and fundName = ?"
        self.__cur.execute(sql, tradeDate, fundName)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeByCUSIP(self, cusip):
        listResult = list()
        sql = "select * from TRADE where CUSIP = ?"
        self.__cur.execute(sql, cusip)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeByTranType(self, tranType):
        listResult = list()
        sql = "select * from TRADE where tranType = ?"
        self.__cur.execute(sql, tranType)
        for i in self.__cur.fetchall():
            result = trade.Trade()
            result.seqNo = i[0]
            result.tranType = i[1]
            result.CUSIP = i[2]
            result.ISIN = i[3]
            result.securityName = i[4]
            result.brokerName = i[5]
            result.fundName = i[6]
            result.customerName = i[7]
            result.traderName = i[8]
            result.side = i[9]
            result.currType = i[10]
            result.price = i[11]
            result.y = i[12]
            result.quantity = i[13]
            result.principal = i[14]
            result.coupon = i[15]
            result.accruedInt = i[16]
            result.repoRate = i[17]
            result.factor = i[18]
            result.net = i[19]
            result.principalInUSD = i[20]
            result.commission = i[21]
            result.tax = i[22]
            result.fee = i[23]
            result.charge = i[24]
            result.settleLocation = i[25]
            result.tradeDate = i[26]
            result.issueDate = i[27]
            result.settleDate = i[28]
            result.matureDate = i[29]
            result.dlrAlias = i[30]
            result.remarks = i[31]
            result.status = i[32]
            result.settled = i[33]
            result.custody = i[34]
            result.fxAccount1 = i[35]
            result.fxAccount2 = i[36]
            result.fxCurrType1 = i[37]
            result.fxCurrType2 = i[38]
            result.reserve1 = i[39]
            result.reserve2 = i[40]
            result.reserve3 = i[41]
            result.reserve4 = i[42]
            result.source = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeCloseByISIN(self, ISIN):
        listResult = list()
        sql = "select * from dbo.tradeClose where ISIN = ? and tranType != 'CREPO'"
        self.__cur.execute(sql, ISIN)
        for i in self.__cur.fetchall():
            result = tradeClose.TradeClose()
            result.seqNo1 = i[0]
            result.seqNo2 = i[1]
            result.tranType = i[2]
            result.CUSIP = i[3]
            result.ISIN = i[4]
            result.securityName = i[5]
            result.fundName = i[6]
            result.side1 = i[7]
            result.side2 = i[8]
            result.currType1 = i[9]
            result.currType2 = i[10]
            result.price1 = i[11]
            result.price2 = i[12]
            result.quantity1 = i[13]
            result.quantity2 = i[14]
            result.principal1 = i[15]
            result.principal2 = i[16]
            result.coupon = i[17]
            result.accruedInt1 = i[18]
            result.accruedInt2 = i[19]
            result.fxRate1 = i[20]
            result.fxRate2 = i[21]
            result.repoRate = i[22]
            result.factor1 = i[23]
            result.factor2 = i[24]
            result.net1 = i[25]
            result.net2 = i[26]
            result.principalInUSD1 = i[27]
            result.principalInUSD2 = i[28]
            result.commission1 = i[29]
            result.commission2 = i[30]
            result.tradeDate1 = i[31]
            result.tradeDate2 = i[32]
            result.settleDate1 = i[33]
            result.settleDate2 = i[34]
            result.matureDate = i[35]
            result.fxAccount1 = i[36]
            result.fxAccount2 = i[37]
            result.fxCurrType1 = i[38]
            result.fxCurrType2 = i[39]
            result.reserve1 = i[40]
            result.reserve2 = i[41]
            result.reserve3 = i[42]
            result.reserve4 = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeCloseByISIN2(self, ISIN):
        listResult = list()
        sql = "select * from dbo.tradeClose where ISIN = ? and tranType = 'CREPO'"
        self.__cur.execute(sql, ISIN)
        for i in self.__cur.fetchall():
            result = tradeClose.TradeClose()
            result.seqNo1 = i[0]
            result.seqNo2 = i[1]
            result.tranType = i[2]
            result.CUSIP = i[3]
            result.ISIN = i[4]
            result.securityName = i[5]
            result.fundName = i[6]
            result.side1 = i[7]
            result.side2 = i[8]
            result.currType1 = i[9]
            result.currType2 = i[10]
            result.price1 = i[11]
            result.price2 = i[12]
            result.quantity1 = i[13]
            result.quantity2 = i[14]
            result.principal1 = i[15]
            result.principal2 = i[16]
            result.coupon = i[17]
            result.accruedInt1 = i[18]
            result.accruedInt2 = i[19]
            result.fxRate1 = i[20]
            result.fxRate2 = i[21]
            result.repoRate = i[22]
            result.factor1 = i[23]
            result.factor2 = i[24]
            result.net1 = i[25]
            result.net2 = i[26]
            result.principalInUSD1 = i[27]
            result.principalInUSD2 = i[28]
            result.commission1 = i[29]
            result.commission2 = i[30]
            result.tradeDate1 = i[31]
            result.tradeDate2 = i[32]
            result.settleDate1 = i[33]
            result.settleDate2 = i[34]
            result.matureDate = i[35]
            result.fxAccount1 = i[36]
            result.fxAccount2 = i[37]
            result.fxCurrType1 = i[38]
            result.fxCurrType2 = i[39]
            result.reserve1 = i[40]
            result.reserve2 = i[41]
            result.reserve3 = i[42]
            result.reserve4 = i[43]
            listResult.append(result)
        return listResult
    
    def qTradeClose(self):
        listResult = list()
        sql = "select * from dbo.tradeClose"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = tradeClose.TradeClose()
            result.seqNo1 = i[0]
            result.seqNo2 = i[1]
            result.tranType = i[2]
            result.CUSIP = i[3]
            result.ISIN = i[4]
            result.securityName = i[5]
            result.fundName = i[6]
            result.side1 = i[7]
            result.side2 = i[8]
            result.currType1 = i[9]
            result.currType2 = i[10]
            result.price1 = i[11]
            result.price2 = i[12]
            result.quantity1 = i[13]
            result.quantity2 = i[14]
            result.principal1 = i[15]
            result.principal2 = i[16]
            result.coupon = i[17]
            result.accruedInt1 = i[18]
            result.accruedInt2 = i[19]
            result.fxRate1 = i[20]
            result.fxRate2 = i[21]
            result.repoRate = i[22]
            result.factor1 = i[23]
            result.factor2 = i[24]
            result.net1 = i[25]
            result.net2 = i[26]
            result.principalInUSD1 = i[27]
            result.principalInUSD2 = i[28]
            result.commission1 = i[29]
            result.commission2 = i[30]
            result.tradeDate1 = i[31]
            result.tradeDate2 = i[32]
            result.settleDate1 = i[33]
            result.settleDate2 = i[34]
            result.matureDate = i[35]
            result.fxAccount1 = i[36]
            result.fxAccount2 = i[37]
            result.fxCurrType1 = i[38]
            result.fxCurrType2 = i[39]
            result.reserve1 = i[40]
            result.reserve2 = i[41]
            result.reserve3 = i[42]
            result.reserve4 = i[43]
            listResult.append(result)
        return listResult
    
    def qISINFromTradeClose(self):
        listResult = list()
        sql = "select distinct ISIN from dbo.tradeClose"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = i[0]
            listResult.append(result)
        return listResult
    
    def qSecurity(self):
        listResult = list()
        sql = "select * from dbo.security"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = security.Security()
            result.securityNo = i[0]
            result.securityName = i[1]
            result.securityType = i[2]
            result.CUSIP = i[3]
            result.ISIN = i[4]
            result.bloombergId = i[5]
            result.issuer = i[6]
            result.coupon = i[7]
            result.couponType = i[8]
            result.couponFreq = i[9]
            result.matureDate = i[10]
            result.currType = i[11]
            result.factor = i[12]
            result.yesPrice = i[13]
            result.monthPrice = i[14]
            result.currPrice = i[15]
            result.moodyRating = i[16]
            result.spRating = i[17]
            result.fitchRating = i[18]
            result.comRating = i[19]
            result.duration = i[20]
            result.y = i[21]
            result.spread = i[22]
            result.category1 = i[23]
            result.category2 = i[24]
            result.issueDate = i[25]
            result.reserve1 = i[26]
            result.reserve2 = i[27]
            result.reserve3 = i[28]
            result.reserve4 = i[29]
            result.reserve5 = i[30]
            result.reserve6 = i[31]
            result.reserve7 = i[32]
            result.reserve8 = i[33]
            result.firstCoupDt = i[35]
            listResult.append(result)
        return listResult

    def qSecurityBySecurityName(self, s):
        listResult = list()
        sql = "select * from dbo.security where ISIN = ? and securityType = ?"
        self.__cur.execute(sql, s.ISIN, s.securityType)
        for i in self.__cur.fetchall():
            result = security.Security()
            result.securityNo = i[0]
            result.securityName = i[1]
            result.securityType = i[2]
            result.CUSIP = i[3]
            result.ISIN = i[4]
            result.bloombergId = i[5]
            result.issuer = i[6]
            result.coupon = i[7]
            result.couponType = i[8]
            result.couponFreq = i[9]
            result.matureDate = i[10]
            result.currType = i[11]
            result.factor = i[12]
            result.yesPrice = i[13]
            result.monthPrice = i[14]
            result.currPrice = i[15]
            result.moodyRating = i[16]
            result.spRating = i[17]
            result.fitchRating = i[18]
            result.comRating = i[19]
            result.duration = i[20]
            result.y = i[21]
            result.spread = i[22]
            result.category1 = i[23]
            result.category2 = i[24]
            result.issueDate = i[25]
            result.reserve1 = i[26]
            result.reserve2 = i[27]
            result.reserve3 = i[28]
            result.reserve4 = i[29]
            result.reserve5 = i[30]
            result.reserve6 = i[31]
            result.reserve7 = i[32]
            result.reserve8 = i[33]
            result.firstCoupDt = i[35]
            listResult.append(result)
        return listResult
    
    def qSecurityByISIN(self, isin):
        listResult = list()
        sql = "select * from dbo.security where ISIN = ?"
        self.__cur.execute(sql, isin)
        for i in self.__cur.fetchall():
            result = security.Security()
            result.securityNo = i[0]
            result.securityName = i[1]
            result.securityType = i[2]
            result.CUSIP = i[3]
            result.ISIN = i[4]
            result.bloombergId = i[5]
            result.issuer = i[6]
            result.coupon = i[7]
            result.couponType = i[8]
            result.couponFreq = i[9]
            result.matureDate = i[10]
            result.currType = i[11]
            result.factor = i[12]
            result.yesPrice = i[13]
            result.monthPrice = i[14]
            result.currPrice = i[15]
            result.moodyRating = i[16]
            result.spRating = i[17]
            result.fitchRating = i[18]
            result.comRating = i[19]
            result.duration = i[20]
            result.y = i[21]
            result.spread = i[22]
            result.category1 = i[23]
            result.category2 = i[24]
            result.issueDate = i[25]
            result.reserve1 = i[26]
            result.reserve2 = i[27]
            result.reserve3 = i[28]
            result.reserve4 = i[29]
            result.reserve5 = i[30]
            result.reserve6 = i[31]
            result.reserve7 = i[32]
            result.reserve8 = i[33]
            result.firstCoupDt = i[35]
            listResult.append(result)
        return listResult
    
    def qSecurityBySecurityNo(self, securityNo):
        listResult = list()
        sql = "select * from dbo.security where securityNo = ?"
        self.__cur.execute(sql, securityNo)
        for i in self.__cur.fetchall():
            result = security.Security()
            result.securityNo = i[0]
            result.securityName = i[1]
            result.securityType = i[2]
            result.CUSIP = i[3]
            result.ISIN = i[4]
            result.bloombergId = i[5]
            result.issuer = i[6]
            result.coupon = i[7]
            result.couponType = i[8]
            result.couponFreq = i[9]
            result.matureDate = i[10]
            result.currType = i[11]
            result.factor = i[12]
            result.yesPrice = i[13]
            result.monthPrice = i[14]
            result.currPrice = i[15]
            result.moodyRating = i[16]
            result.spRating = i[17]
            result.fitchRating = i[18]
            result.comRating = i[19]
            result.duration = i[20]
            result.y = i[21]
            result.spread = i[22]
            result.category1 = i[23]
            result.category2 = i[24]
            result.issueDate = i[25]
            result.reserve1 = i[26]
            result.reserve2 = i[27]
            result.reserve3 = i[28]
            result.reserve4 = i[29]
            result.reserve5 = i[30]
            result.reserve6 = i[31]
            result.reserve7 = i[32]
            result.reserve8 = i[33]
            result.firstCoupDt = i[35]
            listResult.append(result)
        return listResult

    def qSecurityForRepo(self, s):
        listResult = list()
        sql = "select * from dbo.security where securityName = ? and reserve3 = ?"
        self.__cur.execute(sql, s.securityName, s.reserve3)
        for i in self.__cur.fetchall():
            result = security.Security()
            result.securityNo = i[0]
            result.securityName = i[1]
            result.securityType = i[2]
            result.CUSIP = i[3]
            result.ISIN = i[4]
            result.bloombergId = i[5]
            result.issuer = i[6]
            result.coupon = i[7]
            result.couponType = i[8]
            result.couponFreq = i[9]
            result.matureDate = i[10]
            result.currType = i[11]
            result.factor = i[12]
            result.yesPrice = i[13]
            result.monthPrice = i[14]
            result.currPrice = i[15]
            result.moodyRating = i[16]
            result.spRating = i[17]
            result.fitchRating = i[18]
            result.comRating = i[19]
            result.duration = i[20]
            result.y = i[21]
            result.spread = i[22]
            result.category1 = i[23]
            result.category2 = i[24]
            result.issueDate = i[25]
            result.reserve1 = i[26]
            result.reserve2 = i[27]
            result.reserve3 = i[28]
            result.reserve4 = i[29]
            result.reserve5 = i[30]
            result.reserve6 = i[31]
            result.reserve7 = i[32]
            result.reserve8 = i[33]
            result.firstCoupDt = i[35]
            listResult.append(result)
        return listResult
    
    def qPriceHistory(self):
        listResult = list()
        sql = "select top 1 * from PRICEHISTORY order by priceDate desc"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = priceHistory.PriceHistory()
            result.price = i[0]
            result.ai = i[1]
            
            tempDate = datetime.datetime.strptime(str(i[2]), '%Y-%m-%d')
            year = str(tempDate.year)
            month = str(tempDate.month)
            day = str(tempDate.day)
            result.priceDate = month + '/' + day + '/' + year
            
            result.lastUptDt = i[3]
            result.ISIN = i[4]
            listResult.append(result)
        return listResult
    
    def qPriceHistoryByISIN(self, ISIN):
        listResult = list()
        sql = "select * from dbo.pricehistory where ISIN = ? order by priceDate desc"
        self.__cur.execute(sql, ISIN)
        for i in self.__cur.fetchall():
            result = priceHistory.PriceHistory()
            result.price = i[0]
            result.ai = i[1]
            result.priceDate = i[2]
            result.lastUptDt = i[3]
            result.ISIN = i[4]
            listResult.append(result)
        return listResult
    
    def qPriceHistoryByPriceDate(self, ISIN, priceDate):
        listResult = list()
        sql = "select * from dbo.pricehistory where ISIN = ? and priceDate < ? order by priceDate desc"
        self.__cur.execute(sql, ISIN, priceDate)
        for i in self.__cur.fetchall():
            result = priceHistory.PriceHistory()
            result.price = i[0]
            result.ai = i[1]
            result.priceDate = i[2]
            result.lastUptDt = i[3]
            result.ISIN = i[4]
            listResult.append(result)
        return listResult
    
    def qPriceHistoryAtPriceDate(self, ISIN, priceDate):
        listResult = list()
        sql = "select * from dbo.pricehistory where ISIN = ? and priceDate = ? order by priceDate desc"
        self.__cur.execute(sql, ISIN, priceDate)
        for i in self.__cur.fetchall():
            result = priceHistory.PriceHistory()
            result.price = i[0]
            result.ai = i[1]
            result.priceDate = i[2]
            result.lastUptDt = i[3]
            result.ISIN = i[4]
            listResult.append(result)
        return listResult
    
    def qPriceHistoryBeforeDate(self, currDate, ISIN):
        listResult = list()
        sql = "select * from dbo.pricehistory where priceDate < ? and ISIN = ? order by priceDate desc" 
        self.__cur.execute(sql, currDate, ISIN)
        for i in self.__cur.fetchall():
            result = priceHistory.PriceHistory()
            result.price = i[0]
            result.ai = i[1]
            result.priceDate = i[2]
            result.lastUptDt = i[3]
            result.ISIN = i[4]
            listResult.append(result)
        return listResult
    
    def qAccountHistory(self, fundName):
        listResult = list()
        sql = "select navA from accounthistory where fundName = ? order by tradeDate asc"
        param = (fundName)
        self.__cur.execute(sql, param)
        for i in self.__cur.fetchall():
            listResult.append(i[0])
        return listResult
    
    def qAccountHistoryBeforeDate(self, fundName, tradeDate):
        listResult = list()
        sql = "select * from accounthistory where fundName = ? and tradeDate < ? order by tradeDate desc"
        self.__cur.execute(sql, fundName, tradeDate)
        for i in self.__cur.fetchall():
            result = accountHistory.AccountHistory()
            result.fundName = i[0]
            result.accountValue = i[1]
            result.cash = i[2]
            result.tradeDate = i[3]
            result.reserve1 = i[4]
            result.reserve2 = i[5]
            result.reserve3 = i[6]
            result.reserve4 = i[7]
            result.costBasis = i[8]
            result.navA = i[9]
            result.navB = i[10]
            listResult.append(result)
        return listResult
    
    def qAccountHistoryAfterDate(self, fundName, tradeDate):
        listResult = list()
        sql = "select * from accounthistory where fundName = ? and tradeDate > ? order by tradeDate asc" 
        self.__cur.execute(sql, fundName, tradeDate)
        for i in self.__cur.fetchall():
            result = accountHistory.AccountHistory()
            result.fundName = i[0]
            result.accountValue = i[1]
            result.cash = i[2]
            result.tradeDate = i[3]
            result.reserve1 = i[4]
            result.reserve2 = i[5]
            result.reserve3 = i[6]
            result.reserve4 = i[7]
            result.costBasis = i[8]
            result.navA = i[9]
            result.navB = i[10]
            listResult.append(result)
        return listResult
    
    def qAccountHistoryWithinDateRange(self, fundName, startDate, endDate):
        listResult = list()
        sql = "select * from ACCOUNTHISTORY where fundName = ? and tradeDate >= DateAdd(dd, -1, ?) \
                and tradeDate < ? order by tradeDate asc"
        self.__cur.execute(sql, fundName, startDate, endDate)
        for i in self.__cur.fetchall():
            result = accountHistory.AccountHistory()
            result.fundName = i[0]
            result.accountValue = i[1]
            result.cash = i[2]
            result.tradeDate = i[3]
            result.reserve1 = i[4]
            result.reserve2 = i[5]
            result.reserve3 = i[6]
            result.reserve4 = i[7]
            result.costBasis = i[8]
            result.navA = i[9]
            result.navB = i[10]
            listResult.append(result)
        return listResult
    
    def qTotalSharesFromInvestHistory(self, investorName, fundName, tradeDate):
        listResult = list()
        sql = "select sum(share) from investHistory where investorName like '%%%s%%' and fundName='%s' and tradeDate<'%s'" \
                % (investorName, fundName, tradeDate)
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = i[0]
            listResult.append(result)
        return listResult
    
    def qInvestHistoryByInvestorName(self, investorName, fundName, startDate, endDate):
        listResult = list()
        sql = "select * from investHistory where investorName like '%%%s%%' and fundName='%s' and tradeDate>'%s' and \
                tradeDate<'%s'" % (investorName, fundName, startDate, endDate)
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = investHistory.InvestHistory()
            if i[0][0:8] == 'Shahriar':
                result.investorName = 'Investor S'
            if i[0][0:5] == 'Green':
                result.investorName = 'Trust G'
            if i[0][0:4] == 'Blue':
                result.investorName = 'Trust B'
            result.fundName = i[1]
            result.side = i[2]
            result.type = i[3]
            result.amount = format(round(i[4], 2), ',')
            result.share = format(round(i[5], 2), ',')
            
            tempDate = datetime.datetime.strptime(str(i[6]), '%Y-%m-%d')
            year = str(tempDate.year)
            month = str(tempDate.month)
            day = str(tempDate.day)
            result.tradeDate = month + '/' + day + '/' + year

            result.reserve1 = i[7]
            result.reserve2 = i[8]
            result.reserve3 = i[9]
            result.reserve4 = i[10]
            listResult.append(result)
        return listResult
    
    def qInvestHistoryByInvestorName2(self, investorName, fundName):
        listResult = list()
        sql = "select * from investHistory where investorName like '%%%s%%' and fundName='%s' order by tradeDate asc" \
                % (investorName, fundName)
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = investHistory.InvestHistory()
            if i[0][0:8] == 'Shahriar':
                result.investorName = 'Investor S'
            if i[0][0:5] == 'Green':
                result.investorName = 'Trust G'
            if i[0][0:4] == 'Blue':
                result.investorName = 'Trust B'
            result.fundName = i[1]
            result.side = i[2]
            result.type = i[3]
            result.amount = i[4]
            result.share = i[5]
            
            tempDate = datetime.datetime.strptime(str(i[6]), '%Y-%m-%d')
            year = str(tempDate.year)
            month = str(tempDate.month)
            day = str(tempDate.day)
            result.tradeDate = month + '/' + day + '/' + year
            
            result.reserve1 = i[7]
            result.reserve2 = i[8]
            result.reserve3 = i[9]
            result.reserve4 = i[10]
            listResult.append(result)
        return listResult
    
    def qInvestHistory(self, fundName):
        listResult = list()
        sql = "select * from investHistory where fundName = ? order by tradeDate asc"
        self.__cur.execute(sql, fundName)
        for i in self.__cur.fetchall():
            result = investHistory.InvestHistory()
            if i[0][0:8] == 'Shahriar':
                result.investorName = 'Investor S'
            if i[0][0:5] == 'Green':
                result.investorName = 'Trust G'
            if i[0][0:4] == 'Blue':
                result.investorName = 'Trust B'
            result.fundName = i[1]
            result.side = i[2]
            result.type = i[3]
            result.amount = format(round(i[4], 2), ',')
            result.share = format(round(i[5], 2), ',')
            
            tempDate = datetime.datetime.strptime(str(i[6]), '%Y-%m-%d')
            year = str(tempDate.year)
            month = str(tempDate.month)
            day = str(tempDate.day)
            result.tradeDate = month + '/' + day + '/' + year
            
            result.reserve1 = i[7]
            result.reserve2 = i[8]
            result.reserve3 = i[9]
            result.reserve4 = i[10]
            listResult.append(result)
        return listResult

    def qFundByFundName(self, fundName):
        listResult = list()
        sql = "select * from dbo.fund where fundName = ?"
        self.__cur.execute(sql, fundName)
        for i in self.__cur.fetchall():
            result = fund.Fund()
            result.fundId = i[0]
            result.fundName = i[1]
            result.securityNo = i[2]
            result.securityName = i[3]
            result.quantity = i[4]
            result.position = i[5]
            result.reserve1 = i[6]
            result.reserve2 = i[7]
            result.reserve3 = i[8]
            result.reserve4 = i[9]
            listResult.append(result)
        return listResult

    def qFundByCriteria(self, fundName, securityNo):
        listResult = list()
        sql = "select * from dbo.fund where fundName = ? and securityNo = ?"
        self.__cur.execute(sql, fundName, securityNo)
        for i in self.__cur.fetchall():
            result = fund.Fund()
            result.fundId = i[0]
            result.fundName = i[1]
            result.securityNo = i[2]
            result.securityName = i[3]
            result.quantity = i[4]
            result.position = i[5]
            result.reserve1 = i[6]
            result.reserve2 = i[7]
            result.reserve3 = i[8]
            result.reserve4 = i[9]
            listResult.append(result)
        return listResult

    def qCurrency(self):
        listResult = list()
        sql = "select * from dbo.currency"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = currency.Currency()
            result.currType = i[0]
            result.rate = i[1]
            result.lastUpdDt = i[2]
            result.reserve1 = i[3]
            result.reserve2 = i[4]
            result.reserve3 = i[5]
            result.reserve4 = i[6]
            result.tradeDate = i[7]
            listResult.append(result)
        return listResult
    
    def qLatestCurrency(self, currType):
        listResult = list()
        sql = "select * from currency where currType = ? and tradeDate = \
                (select top 1 tradeDate from currency order by tradeDate desc)"
        self.__cur.execute(sql, currType)
        for i in self.__cur.fetchall():
            result = currency.Currency()
            result.currType = i[0]
            result.rate = i[1]
            result.lastUpdDt = i[2]
            result.reserve1 = i[3]
            result.reserve2 = i[4]
            result.reserve3 = i[5]
            result.reserve4 = i[6]
            result.tradeDate = i[7]
            listResult.append(result)
        return listResult
    
    def qCurrencyByDate(self, currType, tradeDate):
        listResult = list()
        sql = "select * from currency where currType = ? and tradeDate = ?"
        self.__cur.execute(sql, currType, tradeDate)
        for i in self.__cur.fetchall():
            result = currency.Currency()
            result.currType = i[0]
            result.rate = i[1]
            result.lastUpdDt = i[2]
            result.reserve1 = i[3]
            result.reserve2 = i[4]
            result.reserve3 = i[5]
            result.reserve4 = i[6]
            result.tradeDate = i[7]
            listResult.append(result)
        return listResult
    
    def qCurrByCurrType(self, currType):
        listResult = list()
        sql = "select * from dbo.currency where currType = ?"
        self.__cur.execute(sql, currType)
        for i in self.__cur.fetchall():
            result = currency.Currency()
            result.currType = i[0]
            result.rate = i[1]
            result.lastUpdDt = i[2]
            result.reserve1 = i[3]
            result.reserve2 = i[4]
            result.reserve3 = i[5]
            result.reserve4 = i[6]
            result.tradeDate = i[7]
            listResult.append(result)
        return listResult

    def qBrokerByBrokerCode(self, brokerCode):
        result = counterparty.Counterparty()
        listResult = list()
        sql = "select * from dbo.counterparty where brokerCode = ?"
        self.__cur.execute(sql, brokerCode)
        for i in self.__cur.fetchall():
            result.brokerCode = i[0]
            result.brokerName = i[1]
            result.brokerGroup = i[2]
            result.euroClear = i[3]
            result.clearStream = i[4]
            result.fed = i[5]
            result.bic = i[6]
            result.dtc = i[7]
            result.reserve1 = i[8]
            result.reserve2 = i[9]
            result.reserve3 = i[10]
            result.reserve4 = i[11]
            result.lastUptdt = i[12]
            listResult.append(result)
        return listResult
    
    def qBroker(self):
        result = counterparty.Counterparty()
        listResult = list()
        sql = "select * from dbo.counterparty"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result.brokerCode = i[0]
            result.brokerName = i[1]
            result.brokerGroup = i[2]
            result.euroClear = i[3]
            result.clearStream = i[4]
            result.fed = i[5]
            result.bic = i[6]
            result.dtc = i[7]
            result.reserve1 = i[8]
            result.reserve2 = i[9]
            result.reserve3 = i[10]
            result.reserve4 = i[11]
            result.lastUptdt = i[12]
            listResult.append(result)
        return listResult
    
    def qCusipNoFromConfig(self):
        result = config.Config()
        sql = "select * from dbo.config"
        self.__cur.execute(sql)
        i = self.__cur.fetchall()[0]
        result.cusipForRepo = i[0]
        result.cusipForFuture = i[1]
        result.cusipForOption = i[2]
        return result
    
    def qOpenPositionByFundName(self, fundName):
        listResult = list()
        sql = "select security.issuer,security.category2,security.coupon,security.matureDate,\
                fund.quantity,security.currPrice,security.yesPrice,security.monthPrice,security.currType,security.ISIN,\
                security.securityType,security.securityNo,security.factor,fund.position,security.couponFreq,security.duration,\
                security.yield,security.spread,security.securityType,security.reserve4 from fund, security \
                where fundName = ? and fund.securityNo = security.securityNo and fund.position != 'C' \
                order by security.issuer asc"
        self.__cur.execute(sql, fundName)
        for i in self.__cur.fetchall():
            result = openPosition.OpenPosition()
            result.issuer = i[0]
            result.category = i[1]
            result.coupon = round(i[2], 2)
            if str(i[3])[0:4] != "1900":
                result.matureDate = str(i[3])
            else:
                result.matureDate = ""
            result.quantity = round(i[4], 2)
            result.currPrice = round(i[5], 4)
            result.yesPrice = round(i[6], 4)
            result.monthPrice = round(i[7], 4)
            result.currency = i[8]
            result.ISIN = i[9]
            result.securityType = i[10]
            result.securityNo = i[11]
            result.factor = i[12]
            result.position = i[13]
            result.couponFreq = i[14]
            try:
                result.duration = round(i[15], 2)
            except:
                result.duration = 0
            try:
                result.ytm = round(i[16], 2)
            except:
                result.ytm = 0
            try:
                result.spread = round(i[17], 2)
            except:
                result.spread = 0
            result.securityType = i[18]
            result.isDefaulted = i[19]
            listResult.append(result)
        return listResult
    
    def qOpenPositionBySecurityType(self, fundName, securityType):
        listResult = list()
        sql = "select security.issuer,security.category2,security.coupon,security.matureDate,fund.quantity,security.currPrice,\
                security.yesPrice,security.monthPrice,security.currType,security.ISIN,security.securityType,\
                security.securityNo,security.factor,fund.position,security.couponFreq,security.duration,security.yield,\
                security.spread,security.securityType,security.reserve4 from fund,security \
                where fundName = ? and fund.securityNo = security.securityNo and fund.position != 'C' \
                and security.securityType = ? order by security.issuer asc"
        self.__cur.execute(sql, fundName, securityType)
        for i in self.__cur.fetchall():
            result = openPosition.OpenPosition()
            result.issuer = i[0]
            result.category = i[1]
            result.coupon = round(i[2], 2)
            if str(i[3])[0:4] != "1900":
                result.matureDate = str(i[3])
            else:
                result.matureDate = ""
            result.quantity = round(i[4], 2)
            result.currPrice = round(i[5], 4)
            result.yesPrice = round(i[6], 4)
            result.monthPrice = round(i[7], 4)
            result.currency = i[8]
            result.ISIN = i[9]
            result.securityType = i[10]
            result.securityNo = i[11]
            result.factor = i[12]
            result.position = i[13]
            result.couponFreq = i[14]
            try:
                result.duration = round(i[15], 2)
            except:
                result.duration = 0
            try:
                result.ytm = round(i[16], 2)
            except:
                result.ytm = 0
            try:
                result.spread = round(i[17], 2)
            except:
                result.spread = 0
            result.securityType = i[18]
            result.isDefaulted = i[19]
            listResult.append(result)
        return listResult
    
    def qOpenPositionByCategory(self, fundName, category):
        listResult = list()
        sql = "select security.issuer,security.category2,security.coupon,security.matureDate,fund.quantity,security.currPrice,\
                security.yesPrice,security.monthPrice,security.currType,security.ISIN,security.securityType,\
                security.securityNo,security.factor,fund.position,security.couponFreq,security.duration,security.yield,\
                security.spread,security.securityType,security.reserve4 from fund, security \
                where fundName = ? and fund.securityNo = security.securityNo and fund.position != 'C' \
                and security.category2 = ? order by security.issuer asc"
        self.__cur.execute(sql, fundName, category)
        for i in self.__cur.fetchall():
            result = openPosition.OpenPosition()
            result.issuer = i[0]
            result.category = i[1]
            result.coupon = round(i[2], 2)
            if str(i[3])[0:4] != "1900":
                result.matureDate = str(i[3])
            else:
                result.matureDate = ""
            result.quantity = round(i[4], 2)
            result.currPrice = round(i[5], 4)
            result.yesPrice = round(i[6], 4)
            result.monthPrice = round(i[7], 4)
            result.currency = i[8]
            result.ISIN = i[9]
            result.securityType = i[10]
            result.securityNo = i[11]
            result.factor = i[12]
            result.position = i[13]
            result.couponFreq = i[14]
            try:
                result.duration = round(i[15], 2)
            except:
                result.duration = 0
            try:
                result.ytm = round(i[16], 2)
            except:
                result.ytm = 0
            try:
                result.spread = round(i[17], 2)
            except:
                result.spread = 0
            result.securityType = i[18]
            result.isDefaulted = i[19]
            listResult.append(result)
        return listResult
    
    def qOpenPositionByCurrency(self, fundName, currType):
        listResult = list()
        sql = "select security.issuer,security.category2,security.coupon,security.matureDate,fund.quantity,security.currPrice,\
                security.yesPrice,security.monthPrice,security.currType,security.ISIN,security.securityType,\
                security.securityNo,security.factor,fund.position,security.couponFreq,security.duration,security.yield,\
                security.spread,security.securityType,security.reserve4 from fund, security \
                where fundName = ? and fund.securityNo = security.securityNo and fund.position != 'C' \
                and security.currType = ? order by security.issuer asc"
        self.__cur.execute(sql, fundName, currType)
        for i in self.__cur.fetchall():
            result = openPosition.OpenPosition()
            result.issuer = i[0]
            result.category = i[1]
            result.coupon = round(i[2], 2)
            if str(i[3])[0:4] != "1900":
                result.matureDate = str(i[3])
            else:
                result.matureDate = ""
            result.quantity = round(i[4], 2)
            result.currPrice = round(i[5], 4)
            result.yesPrice = round(i[6], 4)
            result.monthPrice = round(i[7], 4)
            result.currency = i[8]
            result.ISIN = i[9]
            result.securityType = i[10]
            result.securityNo = i[11]
            result.factor = i[12]
            result.position = i[13]
            result.couponFreq = i[14]
            try:
                result.duration = round(i[15], 2)
            except:
                result.duration = 0
            try:
                result.ytm = round(i[16], 2)
            except:
                result.ytm = 0
            try:
                result.spread = round(i[17], 2)
            except:
                result.spread = 0
            result.securityType = i[18]
            result.isDefaulted = i[19]
            listResult.append(result)
        return listResult
    
    def qOpenPositionForRM(self, fundName, securityType, countryCode):
        listResult = list()
        sql = "select a.securityName,a.securityType,a.ISIN,a.category1,a.category2,a.currPrice,a.yesPrice,a.currType,a.factor,\
                b.priceDate,c.price,c.ai,d.quantity,d.position,f.rate \
                from SECURITY a \
                inner join (select max(priceDate) as priceDate,ISIN from PRICEHISTORY group by ISIN) b \
                on a.ISIN = b.ISIN \
                inner join (select price,ai,ISIN,priceDate from PRICEHISTORY) c \
                on b.ISIN = c.ISIN and b.priceDate = c.priceDate \
                inner join (select fundName,securityNo,quantity,position from FUND) d \
                on d.fundName = ? and a.securityNo=d.securityNo and d.position != 'C' and a.securityType = ? \
                and a.category2 = ? \
                inner join (select max(tradeDate) as tradeDate,currType from CURRENCY group by currType) e \
                on a.currType = e.currType \
                inner join (select rate,currType,tradeDate from CURRENCY) f \
                on e.currType = f.currType and e.tradeDate = f.tradeDate"
        self.__cur.execute(sql, fundName, securityType, countryCode)
        for i in self.__cur.fetchall():
            result = riskManagement.RiskManagement()
            result.securityName = i[0]
            result.securityType = i[1]
            result.ISIN = i[2]
            result.industry = i[3]
            result.country = i[4]
            result.currPrice = i[5]
            result.yesPrice = i[6]
            result.currType = i[7]
            result.factor = i[8]
            result.priceDate = i[9]
            result.price = i[10]
            result.ai = i[11]
            result.quantity = i[12]
            result.position = i[13]
            result.fxRate = i[14]
            listResult.append(result)
        return listResult
    
    def qOpenPositionForRmInSov(self, fundName, securityType, countryCode1, countryCode2, countryCode3):
        listResult = list()
        sql = "select a.securityName,a.securityType,a.ISIN,a.category1,a.category2,a.currPrice,a.yesPrice,a.currType,a.factor,\
                b.priceDate,c.price,c.ai,d.quantity,d.position,f.rate \
                from SECURITY a \
                inner join (select max(priceDate) as priceDate,ISIN from PRICEHISTORY group by ISIN) b \
                on a.ISIN = b.ISIN \
                inner join (select price,ai,ISIN,priceDate from PRICEHISTORY) c \
                on b.ISIN = c.ISIN and b.priceDate = c.priceDate \
                inner join (select fundName,securityNo,quantity,position from FUND) d \
                on d.fundName = ? and a.securityNo = d.securityNo and d.position != 'C' and a.securityType = ? \
                and a.category2 != ? and a.category2 != ? and a.category2 != ? and a.category1 = 'Government'\
                inner join (select max(tradeDate) as tradeDate,currType from CURRENCY group by currType) e \
                on a.currType = e.currType \
                inner join (select rate,currType,tradeDate from CURRENCY) f \
                on e.currType = f.currType and e.tradeDate = f.tradeDate"
        self.__cur.execute(sql, fundName, securityType, countryCode1, countryCode2, countryCode3)
        for i in self.__cur.fetchall():
            result = riskManagement.RiskManagement()
            result.securityName = i[0]
            result.securityType = i[1]
            result.ISIN = i[2]
            result.industry = i[3]
            result.country = i[4]
            result.currPrice = i[5]
            result.yesPrice = i[6]
            result.currType = i[7]
            result.factor = i[8]
            result.priceDate = i[9]
            result.price = i[10]
            result.ai = i[11]
            result.quantity = i[12]
            result.position = i[13]
            result.fxRate = i[14]
            listResult.append(result)
        return listResult
    
    def qOpenPositionForRmNotInSov(self, fundName, securityType, countryCode1, countryCode2, countryCode3):
        listResult = list()
        sql = "select a.securityName,a.securityType,a.ISIN,a.category1,a.category2,a.currPrice,a.yesPrice,a.currType,a.factor,\
                b.priceDate,c.price,c.ai,d.quantity,d.position,f.rate \
                from SECURITY a \
                inner join (select max(priceDate) as priceDate,ISIN from PRICEHISTORY group by ISIN) b \
                on a.ISIN = b.ISIN \
                inner join (select price,ai,ISIN,priceDate from PRICEHISTORY) c \
                on b.ISIN = c.ISIN and b.priceDate = c.priceDate \
                inner join (select fundName,securityNo,quantity,position from FUND) d \
                on d.fundName = ? and a.securityNo = d.securityNo and d.position != 'C' and a.securityType = ? \
                and a.category2 != ? and a.category2 != ? and a.category2 != ? and a.category1 != 'Government'\
                inner join (select max(tradeDate) as tradeDate,currType from CURRENCY group by currType) e \
                on a.currType = e.currType \
                inner join (select rate,currType,tradeDate from CURRENCY) f \
                on e.currType = f.currType and e.tradeDate = f.tradeDate"
        self.__cur.execute(sql, fundName, securityType, countryCode1, countryCode2, countryCode3)
        for i in self.__cur.fetchall():
            result = riskManagement.RiskManagement()
            result.securityName = i[0]
            result.securityType = i[1]
            result.ISIN = i[2]
            result.industry = i[3]
            result.country = i[4]
            result.currPrice = i[5]
            result.yesPrice = i[6]
            result.currType = i[7]
            result.factor = i[8]
            result.priceDate = i[9]
            result.price = i[10]
            result.ai = i[11]
            result.quantity = i[12]
            result.position = i[13]
            result.fxRate = i[14]
            listResult.append(result)
        return listResult

    def qOpenPositionCountryByCriteria(self, fundName):
        listResult = list()
        sql = "select distinct security.category2 from fund, security where fundName = ? \
                and fund.securityNo = security.securityNo and fund.position != 'C'"
        self.__cur.execute(sql, fundName)
        for i in self.__cur.fetchall():
            listResult.append(str(i[0]))
        return listResult
    
    def qOpenPositionCategoryByFundName(self, fundName):
        listResult = list()
        sql = "select distinct security.securityType from fund, security where fundName = ? \
                and fund.securityNo = security.securityNo and fund.position != 'C' \
                and security.securityType != 'CALL' and security.securityType != 'PUT'"
        self.__cur.execute(sql, fundName)
        for i in self.__cur.fetchall():
            listResult.append(i[0])
        return listResult
    
    def qOpenPositionCurrencyByFundName(self, fundName):
        listResult = list()
        sql = "select distinct security.currType from fund, security where fundName = ? \
                and fund.securityNo = security.securityNo and fund.position != 'C'"
        self.__cur.execute(sql, fundName)
        for i in self.__cur.fetchall():
            listResult.append(i[0])
        return listResult
    
    def qReport(self):
        listResult = list()
        sql = "select * from dbo.report order by tradeDate desc"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = report.Report()
            result.tradeDate = i[0]
            result.yesAccValue = i[1]
            result.currAccValue = i[2]
            result.monthEndAccValue = i[3]
            result.yearEndAccValue = i[4]
            result.reserve1 = i[5]
            result.reserve2 = i[6]
            result.reserve3 = i[7]
            result.reserve4 = i[8]
            result.reserve5 = i[9]
            result.reserve6 = i[10]
            result.reserve7 = i[11]
            result.reserve8 = i[12]
            listResult.append(result)
        return listResult
    
    def qReportByTradeDate(self, tradeDate):
        listResult = list()
        sql = "select * from dbo.report where tradeDate = ?"
        self.__cur.execute(sql, tradeDate)
        for i in self.__cur.fetchall():
            result = report.Report()
            result.tradeDate = i[0]
            result.yesAccValue = i[1]
            result.currAccValue = i[2]
            result.monthEndAccValue = i[3]
            result.yearEndAccValue = i[4]
            result.reserve1 = i[5]
            result.reserve2 = i[6]
            result.reserve3 = i[7]
            result.reserve4 = i[8]
            result.reserve5 = i[9]
            result.reserve6 = i[10]
            result.reserve7 = i[11]
            result.reserve8 = i[12]
            listResult.append(result)
        return listResult
    
    def qTradeBlotter(self):
        listResult = list()
        sql = "select * from dbo.tradeBlotter order by tradeDate desc, time desc"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = tradeBlotter.TradeBlotter()
            result.tradeDate = i[0]
            result.time = i[1]
            result.bs = i[2]
            result.quantity = format(int(i[3]), ',')
            result.securityName = i[4]
            result.price = round(float(i[5]), 2)
            result.currency = i[6]
            result.trader = i[7]
            result.accounts = i[8]
            result.counterparty = i[9]
            result.salesTrader = i[10]
            result.lastUptDt = i[11]
            result.remark = i[12]
            result.status = i[13]
            result.book = i[14]
            result.ISIN = i[15]
            listResult.append(result)
        return listResult
    
    def qTradeBlotterByStatus(self, status):
        listResult = list()
        sql = "select * from dbo.tradeBlotter where status = ? order by lastUptDt desc"
        self.__cur.execute(sql, status)
        for i in self.__cur.fetchall():
            result = tradeBlotter.TradeBlotter()
            result.tradeDate = i[0]
            result.time = i[1]
            result.bs = i[2]
            result.quantity = format(int(i[3]), ',')
            result.securityName = i[4]
            result.price = round(float(i[5]), 2)
            result.currency = i[6]
            result.trader = i[7]
            result.accounts = i[8]
            result.counterparty = i[9]
            result.salesTrader = i[10]
            result.lastUptDt = i[11]
            result.remark = i[12]
            result.status = i[13]
            result.book = i[14]
            result.ISIN = i[15]
            listResult.append(result)
        return listResult
    
    def qTradeBlotterWithinDate(self, startDate, endDate):
        listResult = list()
        sql = "select * from dbo.tradeBlotter where tradeDate >= ? and tradeDate <= ? order by tradeDate desc" 
        self.__cur.execute(sql, startDate, endDate)
        for i in self.__cur.fetchall():
            result = tradeBlotter.TradeBlotter()
            result.tradeDate = i[0]
            result.time = i[1]
            result.bs = i[2]
            result.quantity = format(int(i[3]), ',')
            result.securityName = i[4]
            result.price = round(float(i[5]), 2)
            result.currency = i[6]
            result.trader = i[7]
            result.accounts = i[8]
            result.counterparty = i[9]
            result.salesTrader = i[10]
            result.lastUptDt = i[11]
            result.remark = i[12]
            result.status = i[13]
            result.book = i[14]
            result.ISIN = i[15]
            listResult.append(result)
        return listResult
    
    def qMessage(self):
        listResult = list()
        sql = "select top 1 * from message order by lastUptdt desc"
        self.__cur.execute(sql)
        for i in self.__cur.fetchall():
            result = message.Message()
            result.positionListAll = i[0]
            result.positionListCategory = i[1]
            result.positionListCountry = i[2]
            result.positionListCurrency = i[3]
            result.countryWeightsList = i[4]
            result.countryLabelsList = i[5]
            result.cashFlowList = i[6]
            result.monthlyCashFlowList = i[7]
            result.returnList = i[8]
            result.monthlyReturn = i[9]
            result.shortTermGL = i[10]
            result.longTermGL = i[11]
            listResult.append(result)
        return listResult

    def iTradeHistory(self, trade):
        sql = "insert into TRADEHISTORY values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%f,%f,%f,%f,%f,%f,%f,%f,\
        %f,%f,%f,%f,%f,%f,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%f,%f,'%s','%s','%s',default)" \
              % (trade.seqNo, trade.tranType, trade.CUSIP, trade.ISIN, trade.securityName, trade.brokerName, trade.fundName, \
                 trade.customerName, trade.traderName, trade.side, trade.currType, trade.price, trade.y, trade.quantity, \
                 trade.principal, trade.coupon, trade.accruedInt, trade.repoRate, trade.factor, trade.net, trade.principalInUSD, \
                 trade.commission, trade.tax, trade.fee, trade.charge, trade.settleLocation, trade.tradeDate, trade.issueDate, \
                 trade.settleDate, trade.matureDate, trade.dlrAlias, trade.remarks, trade.status, trade.settled, trade.custody, \
                 trade.fxAccount1, trade.fxAccount2, trade.fxCurrType1, trade.fxCurrType2, trade.reserve1, \
                 trade.reserve2, trade.reserve3, trade.reserve4, trade.source)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def iTradeClose(self, tradeClose):
        sql = "insert into TRADECLOSE values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%f,%f,%f,%f,%f, \
                %f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,'%s','%s','%s','%s','%s','%s','%s','%s','%s',%f,%f, \
                '%s','%s',default)" \
              % (tradeClose.seqNo1,tradeClose.seqNo2,tradeClose.tranType,tradeClose.CUSIP,tradeClose.ISIN,\
                 tradeClose.securityName,tradeClose.fundName,tradeClose.side1,tradeClose.side2,tradeClose.currType1,\
                 tradeClose.currType2,tradeClose.price1,tradeClose.price2,tradeClose.quantity1,tradeClose.quantity2,\
                 tradeClose.principal1,tradeClose.principal2,tradeClose.coupon,tradeClose.accruedInt1,tradeClose.accruedInt2,\
                 tradeClose.fxRate1,tradeClose.fxRate2,tradeClose.repoRate,tradeClose.factor1,tradeClose.factor2,\
                 tradeClose.net1,tradeClose.net2,tradeClose.principalInUSD1,tradeClose.principalInUSD2,tradeClose.commission1,\
                 tradeClose.commission2,tradeClose.tradeDate1,tradeClose.tradeDate2,tradeClose.settleDate1,\
                 tradeClose.settleDate2,tradeClose.matureDate,tradeClose.fxAccount1,tradeClose.fxAccount2,\
                 tradeClose.fxCurrType1,tradeClose.fxCurrType2,tradeClose.reserve1,tradeClose.reserve2,tradeClose.reserve3,\
                 tradeClose.reserve4)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)

    def iTrade(self, trade):
        sql = "insert into TRADE values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%f,%f,%f,%f,%f,%f,%f,%f,\
        %f,%f,%f,%f,%f,%f,'%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%f,%f,'%s','%s','%s',default)" \
              % (trade.seqNo, trade.tranType, trade.CUSIP, trade.ISIN, trade.securityName, trade.brokerName, trade.fundName, \
                 trade.customerName, trade.traderName, trade.side, trade.currType, trade.price, trade.y, trade.quantity, \
                 trade.principal, trade.coupon, trade.accruedInt, trade.repoRate, trade.factor, trade.net, trade.principalInUSD, \
                 trade.commission, trade.tax, trade.fee, trade.charge, trade.settleLocation, trade.tradeDate, trade.issueDate, \
                 trade.settleDate, trade.matureDate, trade.dlrAlias, trade.remarks, trade.status, trade.settled, trade.custody, \
                 trade.fxAccount1, trade.fxAccount2, trade.fxCurrType1, trade.fxCurrType2, trade.reserve1, \
                 trade.reserve2, trade.reserve3, trade.reserve4, trade.source)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)

    def iSecurity(self, security):
        sql = "insert into SECURITY values ('%s','%s','%s','%s','%s','%s',%f,'%s',%f,'%s','%s','%s',0,0,%f,\
            null,null,null,null,null,null,null,null,null,'%s',null,null,'%s',null,null,null,null,null,default,'%s')" \
              % (security.securityName, security.securityType, security.CUSIP, security.ISIN, security.bloombergId, \
                 security.issuer, security.coupon, security.couponType, security.couponFreq, security.matureDate, \
                 security.currType, security.factor, security.currPrice, security.issueDate,security.reserve3,security.firstCoupDt)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def iPrice(self, priceHistory):
        sql = "insert into PRICEHISTORY values (%f,%f,'%s',default,'%s')" \
                % (priceHistory.price, priceHistory.ai, priceHistory.priceDate, priceHistory.ISIN)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)

    def iFund(self, fund):
        sql = "insert into FUND values ('%s','%s','%s',%f,'%s',null,null,null,null,default)" \
              % (fund.fundName, fund.securityNo, fund.securityName, fund.quantity, fund.position)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)

    def iCurrency(self, currency):
        sql = "insert into CURRENCY values ('%s',%f,default,%f,%f,'%s','%s','%s')" \
              % (currency.currType, currency.rate, currency.reserve1, currency.reserve2, \
                 currency.reserve3, currency.reserve4, currency.tradeDate)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def iCounterparty(self, counterparty):
        sql = "insert into COUNTERPARTY values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%f,%f,default)" \
              % (counterparty.brokerCode, counterparty.brokerName, counterparty.brokerGroup, counterparty.euroClear, \
                 counterparty.clearStream, counterparty.fed, counterparty.bic, counterparty.dtc, counterparty.reserve1, \
                 counterparty.reserve2, counterparty.reserve3, counterparty.reserve4)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def iTradeBlotter(self, tradeBlotter):
        sql = "insert into TRADEBLOTTER values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',default,'%s','%s','%s','%s')" \
              % (tradeBlotter.tradeDate, tradeBlotter.time, tradeBlotter.bs, tradeBlotter.quantity, tradeBlotter.securityName, \
                 tradeBlotter.price, tradeBlotter.currency, tradeBlotter.trader, tradeBlotter.accounts, \
                 tradeBlotter.counterparty, tradeBlotter.salesTrader, tradeBlotter.remark, tradeBlotter.status, \
                 tradeBlotter.book, tradeBlotter.isin)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def iReport(self, report):
        sql = "insert into REPORT values (?,?,?,?,?,?,?,?,?,?,?,?,?)" 
        try:
            self.__cur.execute(sql,report.tradeDate,report.yesAccValue,report.currAccValue,report.monthEndAccValue,\
                               report.yearEndAccValue,report.reserve1,report.reserve2,report.reserve3,report.reserve4,\
                               report.reserve5,report.reserve6,report.reserve7,report.reserve8)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def iMessage(self, message):
        sql = "insert into MESSAGE values (?,?,?,?,?,?,?,?,?,?,?,?,default)" 
        try:
            self.__cur.execute(sql,message.positionListAll,message.positionListCategory,message.positionListCountry, \
                               message.positionListCurrency,message.countryWeightsList,message.countryLabelsList, \
                               message.cashFlowList,message.monthlyCashFlowList,message.returnList,message.monthlyReturn, \
                               message.shortTermGL,message.longTermGL)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def uTradeHistoryBySeqNo(self, trade):
        sql = "update tradehistory set reserve1 = ?,reserve4 = ? where seqNo = ?"
        try:
            self.__cur.execute(sql, trade.reserve1, trade.reserve4, trade.seqNo)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def uTradeFromTradeHistory(self):
        sql = "update TRADE set reserve1 = (select reserve1 from TRADEHISTORY where TRADE.seqNo=TRADEHISTORY.seqNo)"
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)

    def uSecurityBySecurityName(self, security):
        sql = "update security set coupon=%f,couponType='%s',couponFreq=%f,factor=%f where securityName='%s'" \
              % (security.coupon, security.couponType, security.couponFreq, security.factor, security.securityName)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def uSecurityBySecurityNameForPriceUpdate(self, security):
        sql = "update security set moodyRating='%s',spRating='%s',fitchRating='%s',comRating='%s',category1='%s', \
                category2='%s',issueDate='%s',duration='%s',yield='%s',spread='%s',bloombergId='%s',\
                factor=%f,reserve4='%s',currPrice=%f,yesPrice=%f,couponFreq=%f,firstCoupDt='%s' \
                where ISIN='%s' and securityType!='REPO'" \
              % (security.moodyRating, security.spRating, security.fitchRating, security.comRating, security.category1, \
                 security.category2, security.issueDate, security.duration, security.y, security.spread, security.bloombergId, \
                 security.factor, security.reserve4, security.currPrice, security.yesPrice, security.couponFreq, \
                 security.firstCoupDt, security.ISIN)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def uSecurityWithoutCountryForPriceUpdate(self, security):
        sql = "update security set moodyRating='%s',spRating='%s',fitchRating='%s',comRating='%s',category1='%s', \
                issueDate='%s',duration='%s',yield='%s',spread='%s',bloombergId='%s', \
                factor=%f,reserve4='%s',currPrice=%f,yesPrice=%f,couponFreq=%f,firstCoupDt='%s' \
                where ISIN='%s' and securityType!='REPO'" \
              % (security.moodyRating, security.spRating, security.fitchRating, security.comRating, security.category1, \
                 security.issueDate, security.duration, security.y, security.spread, security.bloombergId, \
                 security.factor, security.reserve4, security.currPrice, security.yesPrice, security.couponFreq, \
                 security.firstCoupDt, security.ISIN)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)

    def uFundByFundName(self, fund):
        sql = "update fund set quantity=%f,position='%s',lastUptdt=default where fundName='%s'" \
              % (fund.quantity, fund.position, fund.fundName)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)

    def uFundByCriteria(self, fund):
        sql = "update fund set quantity=%f,position='%s',lastUptdt=default where fundName='%s' and securityNo='%s'" \
              % (fund.quantity, fund.position, fund.fundName, fund.securityNo)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def uCounterpartyByBrokerCode(self, counterparty):
        sql = "update COUNTERPARTY set euroClear='%s',clearStream='%s',fed='%s',bic='%s',dtc='%s',lastUptdt=default \
                 where brokerCode='%s'" % (counterparty.euroClear, counterparty.clearStream, counterparty.fed, counterparty.bic, \
                                         counterparty.dtc, counterparty.brokerCode)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def uCusipInConfig(self, config):
        sql = "update CONFIG set cusipForRepo=%f,cusipForFuture=%f" % (config.cusipForRepo, config.cusipForFuture)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def uStatusInTradeBlotter(self, tradeBlotter):
        sql = "update TRADEBLOTTER set status='%s' where id='%d'" % (tradeBlotter.status, tradeBlotter.id)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def uReport(self, report):
        sql = "update REPORT set yesAccValue = ?, currAccValue = ?, monthEndAccValue = ?, yearEndAccValue = ?, reserve1 = ?,\
                reserve2 = ?, reserve3 = ?, reserve4 = ?, reserve5 = ?, reserve6 = ?, reserve7 = ?, reserve8 = ? \
                where tradeDate = ?"
        try:
            self.__cur.execute(sql, report.yesAccValue, report.currAccValue, report.currAccValue, report.yearEndAccValue, \
                               report.reserve1, report.reserve2, report.reserve3, report.reserve4, report.reserve5, \
                               report.reserve6, report.reserve7, report.reserve8, report.tradeDate)
        except Exception, e:
            self.__con.rollback()
            print(e)

    def dTrade(self, trade):
        sql = "delete from trade where reserve4 = '%s' and fundName = '%s'" % (trade.reserve4, trade.fundName)
        #reserve4 = securityNo
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def dCurrency(self):
        sql = "delete from currency"
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
    
    def dCurrencyByTradeDate(self, currType, tradeDate):
        sql = "delete from currency where currType='%s'and tradeDate='%s'" % (currType, tradeDate)
        try:
            self.__cur.execute(sql)
        except Exception, e:
            self.__con.rollback()
            print(e)
