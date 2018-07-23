import csv
from flask import g
from datetime import date
from dao.model import trade
import time
import os.path
from symbol import continue_stmt

USBankAcc={"AGCF":"001050987829", "ACPT":"001050986301","PGOF":"001050993158","HART":"001050996312"}

class FileGenerator:
    def AGCF_Admin(self):
        today = date.today()
#         fundtrades=g.dataBase.qTradeByFundName("AGCF",str(today))
        fundtrades = g.dataBase.qTradeByFundName("AGCF", "2017-06-14")
        
        if len(fundtrades)==0:
            return
    
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Admin\AGCF\Trades AGCF " + datestamp + ".csv"
        # if (os.path.isfile(file):    
        with open (file,'w') as csvfile:
            fieldsnames=['Account','CUSIP/TICKER','ISIN','Buy/Sell','Inv Type','Issuer','Trade Date',\
                         'Settle Date','Coupon','Maturity','Currency','Original Notional','Current Notional',\
                         'FXRate','Price','Accured Interest','Commission','Cost','Counter Party','Euroclear','DTC','CEDEL']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                tempFXRate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempissuerlist=i.securityName.split()
                tempissuer=tempissuerlist[0]
                tempAI = i.accruedInt
                tempSettlementLocation=""
                tempEuroClearAccount=0
                tempClearStreamAccount=0
                tempSide = i.side
                
                if i.tranType == 'EURO':
                    tempTranType = "Bond"
                elif i.tranType =='EQTY':
                    tempTranType = "Equity"
                elif i.tranType == 'REPO':
                    tempTranType = "Repos"
                    tempAI = 0
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType=="CREPO":
                    tempTranType ="Repos"
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType == "FUT":
                    tempissuer = "Futures"
                    tempTranType = "Futures"
                    
                if broker.euroClear != None:
                    tempSettlementLocation = "EUR"
                    tempEuroClearAccount = broker.euroClear
                    tempClearStreamAccount = 0
                else:
                    tempSettlementLocation = "CED"
                    tempEuroClearAccount = 0
                    tempClearStreamAccount = broker.clearStream
                    
                if tempSide == 'S' and i.status =='Initial':
                    tempSide = 'Short Sell'
                elif tempSide == 'B' and i.status =='Close':
                    tempSide = 'Repurchase'
                
                writer.writerow({ 'Account': i.fundName, \
                                  'CUSIP/TICKER' : i.CUSIP, \
                                  'ISIN': i.ISIN, \
                                  'Buy/Sell': tempSide, \
                                  'Inv Type': tempTranType, \
                                  'Issuer': tempissuer, \
                                  'Trade Date': i.tradeDate.strftime('%m/%d/%Y'), \
                                  'Settle Date': i.settleDate.strftime('%m/%d/%Y'), \
                                  'Coupon': i.coupon, \
                                  'Maturity':i.matureDate.strftime('%m/%d/%Y'), \
                                  'Currency': i.currType , \
                                  'Original Notional': str(i.quantity), \
                                  'Current Notional' : str(i.quantity*i.factor), \
                                  'FXRate':tempFXRate, \
                                  'Price': i.price, \
                                  'Accured Interest': tempAI, \
                                  'Commission': i.commission, \
                                  'Cost':i.net, \
                                  'Counter Party': broker.brokerName, \
                                  'Euroclear':tempEuroClearAccount, \
                                  'DTC':'', \
                                  'CEDEL': tempClearStreamAccount })
########################################################################################
    def HART_Admin(self):
        today = date.today()
#         fundtrades=g.dataBase.qTradeByFundName("HART",str(today))
        fundtrades = g.dataBase.qTradeByFundName("HART", "2017-05-15")
        if len(fundtrades)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Admin\HART\Trades HART " + datestamp + ".csv"
        # if (os.path.isfile(file):
    
        with open (file,'w') as csvfile:
            fieldsnames=['Account','CUSIP/TICKER','ISIN','Buy/Sell','Inv Type','Issuer','Trade Date',\
                         'Settle Date','Coupon','Maturity','Currency','Original Notional','Current Notional',\
                         'FXRate','Price','Accured Interest','Commission','Cost','Counter Party','Euroclear','DTC','CEDEL']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                tempFXRate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempissuerlist=i.securityName.split()
                tempissuer=tempissuerlist[0]
                tempAI = i.accruedInt
                tempSettlementLocation=""
                tempEuroClearAccount=0
                tempClearStreamAccount=0
                
                if i.tranType == 'EURO':
                    tempTranType = "Bond"
                elif i.tranType =='EQTY':
                    tempTranType = "Equity"
                elif i.tranType == 'REPO':
                    tempTranType = "Repos"
                    tempAI = 0
                elif i.tranType=="CREPO":
                    tempTranType ="Repos"
                elif i.tranType == "FUT":
                    tempissuer = "Futures"
                    tempTranType='Futures'
                if broker.euroClear != None:
                    tempSettlementLocation = "EUR"
                    tempEuroClearAccount = broker.euroClear
                    tempClearStreamAccount = 0
                else:
                    tempSettlementLocation = "CED"
                    tempEuroClearAccount = 0
                    tempClearStreamAccount = broker.clearStream
                
                writer.writerow({ 'Account': i.fundName, \
                                  'CUSIP/TICKER' : i.CUSIP, \
                                  'ISIN': i.ISIN, \
                                  'Buy/Sell': i.side, \
                                  'Inv Type': tempTranType, \
                                  'Issuer': tempissuer, \
                                  'Trade Date': i.tradeDate.strftime('%m/%d/%Y'), \
                                  'Settle Date': i.settleDate.strftime('%m/%d/%Y'), \
                                  'Coupon': i.coupon, \
                                  'Maturity':i.matureDate.strftime('%m/%d/%Y'), \
                                  'Currency': i.currType , \
                                  'Original Notional': str(i.quantity), \
                                  'Current Notional' : str(i.quantity*i.factor), \
                                  'FXRate':tempFXRate, \
                                  'Price': i.price, \
                                  'Accured Interest': tempAI, \
                                  'Commission': i.commission, \
                                  'Cost':i.net, \
                                  'Counter Party': broker.brokerName, \
                                  'Euroclear':tempEuroClearAccount, \
                                  'DTC':'', \
                                  'CEDEL': tempClearStreamAccount })
########################################################################################
    def INC_Admin(self):
        today = date.today()
#         fundtrades1=g.dataBase.qTradeByFundName("INC5",str(today))
#         fundtrades2=g.dataBase.qTradeByFundName("INC5",str(today))
        fundtrades1 = g.dataBase.qTradeByFundName("INC5", "2017-06-14")
        fundtrades2 = g.dataBase.qTradeByFundName("INC0", "2017-06-14")
        if len(fundtrades1)+len(fundtrades2)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Admin\INC5\INC5_Trades_" + datestamp + "_IFS"+ ".csv"
    
        with open (file,'w') as csvfile:
            fieldsnames=['Transaction Reference Number','Fund Number','Fund Name','Transaction Type','Security Type',\
                         'Trade Type','Security Identifier','Instrument Name','Trade Date','Settlement Date',\
                         'Maturity Date','Currency','Quantity','Clean Price','Accured Interest',\
                         'Commission','Tax','Fees','Other Charges','Net Settlement',\
                         'Executing Broker','Executing Broker BIC','Executing Safe Keeping account','Clearing BIC/Participant',\
                         'Clearing Account','Settlement Location Broker','Settlement Location Custody','Original Face',\
                         'Index Ratio','Current Face','Accounting Only','Custodian','unit of Calc','Currency #1 amount for FX',\
                         'Settlement currency #1 for FX','Currency #2 amount for FX','Settlement currency #2 for FX','FX Rate',\
                         'Basis','ISIN','Custody Only','CUSIP', 'Coupon','Position','Dirty Price','Liquidity Category',\
                         'Risk Sub Category','Instrument Group','RED Pair','Start Date','First Coupon', 'Frequency','Day Count',\
                         'Restructuring']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades1:
                fxrate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempClearAccount=0
                tempSettlementLocation=''
                tempSecurityType=''
                tempSettlementLocationCustody=''
                tempSide = ''
                tempPosition = ''
                tempAccuredInterest = 0
                tempMaturity =i.matureDate.strftime('%m/%d/%Y')
                tempCoupon=""
                if broker.euroClear != None:
                    tempClearAccount=broker.euroClear
                    tempSettlementLocation="EUR"
                else:
                    tempClearAccount=broker.clearStream
                    tempSettlementLocation="CED"
                if i.tranType=='EURO':
                    tempSecurityType ='Bond'               
                elif i.tranType=='EQTY':
                    tempSecurityType='Equity'
                elif i.tranType=='REPO' or i.tranType=='CREPO':
                    tempSecurityType='Repos'
                if i.side=='B' and i.tranType=='REPO':
                    tempSide = 'Open Reverse Repo'
                    tempPosition ='Long'
                    tempSettlementLocationCustody='Settle in Euroclear'
                    tempInstrumentName = 'Reverse Repo ' + str(round(i.repoRate,2)) + '% OPEN'
                    tempAccuredInterest = 0
                elif i.side=='S'and i.tranType=='REPO':
                    tempSide = 'Open Repo'
                    tempPosition ='Short'
                    tempSettlementLocationCustody='Deliver from Euroclear'
                    tempInstrumentName = 'Repo ' + str(round(i.repoRate,2)) + '% OPEN'
                    tempAccuredInterest = 0
                elif i.side=='B'and i.tranType=='CREPO':
                    tempSide = 'Close Repo'
                    tempPosition ='Short'
                    tempSettlementLocationCustody='Settle in Euroclear'
                    tempInstrumentName = 'Repo ' + str(round(i.repoRate,2)) + '% CLOSE'
                    tempAccuredInterest = i.accruedInt
                elif i.side=='S'and i.tranType=='CREPO':
                    tempSide = 'Close Reverse Repo'
                    tempPosition ='Long'
                    tempSettlementLocationCustody='Deliver from Euroclear'
                    tempInstrumentName = 'Reverse Repo ' + str(round(i.repoRate,2)) + '% CLOSE'
                    tempAccuredInterest = i.accruedInt
                elif i.side =='B':
                    if i.status == 'Initial':
                        tempSide = 'Buy'
                        tempPosition='Long'
                    else:
                        tempSide = 'Repurchase'
                        tempPosition='Short'
                    tempSettlementLocationCustody='Settle in Euroclear'
#                     tempInstrumentName = i.securityName
                    tempissuerlist=i.securityName.split()
                    tempissuer=tempissuerlist[0]                    
                    tempInstrumentName = tempissuer+' ' + str(i.coupon)+'% ' +str(i.matureDate.year)  
                    tempAccuredInterest = i.accruedInt
                elif i.side =='S':
                    if i.status == 'Initial':
                        tempSide = 'Short Sell'
                        tempPosition='Short'
                    else:
                        tempSide = 'Sell'
                        tempPosition='Long'
                    tempSettlementLocationCustody='Deliver from Euroclear'
#                     tempInstrumentName = i.securityName
                    tempissuerlist=i.securityName.split()
                    tempissuer=tempissuerlist[0]                    
                    tempInstrumentName = tempissuer+' ' + str(i.coupon)+'% ' +str(i.matureDate.year) 
                    tempAccuredInterest = i.accruedInt                            
                if i.tranType=="FX":
                    q1=i.quantity
                    q2=i.coupon
                    c1=i.fxCurrType1
                    c2=i.fxCurrType2
                    tempCoupon=""
                elif i.tranType=='REPO' or i.tranType=='CREPO':
                    q1 = ""
                    q2 = ""
                    c1 = ""
                    c2 = ""
                    tempCoupon=i.repoRate
                else:
                    q1 = ""
                    q2 = ""
                    c1 = ""
                    c2 = ""
                    tempCoupon=i.coupon
                tempDirtyPrice = i.net/i.quantity*100
    
                writer.writerow({'Transaction Reference Number':i.seqNo,\
                                 'Fund Number':i.fundName,\
                                 'Fund Name':"Baldr Draco Fund",\
                                 'Transaction Type':"NEW",\
                                 'Security Type': tempSecurityType,\
                                 'Trade Type': tempSide,\
                                 'Security Identifier':i.CUSIP,\
                                 'Instrument Name': tempInstrumentName,\
                                 'Trade Date': i.tradeDate.strftime('%m/%d/%Y'),\
                                 'Settlement Date': i.settleDate.strftime('%m/%d/%Y'),\
                                 'Maturity Date': i.matureDate.strftime('%m/%d/%Y'),\
                                 'Currency': i.currType,\
                                 'Quantity': i.quantity,\
                                 'Clean Price': i.price,\
                                 'Accured Interest': tempAccuredInterest,\
                                 'Commission':i.commission,\
                                 'Tax': i.tax,\
                                 'Fees': i.fee,\
                                 'Other Charges': i.charge,\
                                 'Net Settlement': i.net,\
                                 'Executing Broker': broker.brokerName,\
                                 'Executing Broker BIC' : broker.bic,\
                                 'Executing Safe Keeping account':"",\
                                 'Clearing BIC/Participant': broker.bic,\
                                 'Clearing Account': tempClearAccount,\
                                 'Settlement Location Broker':tempSettlementLocation,\
                                 'Settlement Location Custody':tempSettlementLocationCustody,\
                                 'Original Face':i.quantity,\
                                 'Index Ratio':i.factor,\
                                 'Current Face':i.quantity*i.factor,\
                                 'Accounting Only':"N",\
                                 'Custodian': "State Street : Share Class A",\
                                 'unit of Calc':"",\
                                 'Currency #1 amount for FX':q1,\
                                 'Settlement currency #1 for FX': c1,\
                                 'Currency #2 amount for FX': q2,\
                                 'Settlement currency #2 for FX':c2,\
                                 'FX Rate':fxrate,\
                                 'Basis':i.principal,\
                                 'ISIN': i.ISIN,\
                                 'Custody Only':"Y",\
                                 'CUSIP': i.CUSIP,\
                                 'Coupon': tempCoupon,\
                                 'Position':tempPosition,\
                                 'Dirty Price':tempDirtyPrice ,\
                                 'Liquidity Category':"",\
                                 'Risk Sub Category':"",\
                                 'Instrument Group':"",\
                                 'RED Pair':"",\
                                 'Start Date':"",\
                                 'First Coupon':"",\
                                 'Frequency':"",\
                                 'Day Count':"",\
                                 'Restructuring':""})
    
                #############################################
            for i in fundtrades2:
                fxrate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempClearAccount=0
                tempSettlementLocation=''
                tempSecurityType=''
                tempSettlementLocationCustody=''
                tempSide = ''
                tempAccuredInterest = 0
                tempMaturity =i.matureDate.strftime('%m/%d/%Y')
                tempCoupon=""
                tempPosition = ''
                if broker.euroClear != None:
                    tempClearAccount=broker.euroClear
                    tempSettlementLocation="EUR"
                else:
                    tempClearAccount=broker.clearStream
                    tempSettlementLocation="CED"
                if i.tranType=='EURO':
                    tempSecurityType ='Bond'               
                elif i.tranType=='EQTY':
                    tempSecurityType='Equity'
                elif i.tranType=='REPO' or i.tranType=='CREPO':
                    tempSecurityType='Repos'
                if i.side=='B' and i.tranType=='REPO':
                    tempSide = 'Open Reverse Repo'
                    tempPosition='Long'
                    tempSettlementLocationCustody='Settle in Euroclear'
                    tempInstrumentName = 'Reverse Repo ' + str(round(i.repoRate,2)) + '% OPEN'
                    tempAccuredInterest = 0
                    tempMaturity=date(2050,1,1)
                elif i.side=='S'and i.tranType=='REPO':
                    tempSide = 'Open Repo'
                    tempPosition='Short'
                    tempSettlementLocationCustody='Deliver from Euroclear'
                    tempInstrumentName = 'Repo ' + str(round(i.repoRate,2)) + '% OPEN'
                    tempAccuredInterest = 0
                    tempMaturity=date(2050,1,1)
                elif i.side=='B'and i.tranType=='CREPO':
                    tempSide = 'Close Repo'
                    tempPosition='Short'
                    tempSettlementLocationCustody='Settle in Euroclear'
                    tempInstrumentName = 'Repo ' + str(round(i.repoRate,2)) + '% CLOSE'
                    tempAccuredInterest = i.accruedInt
                elif i.side=='S'and i.tranType=='CREPO':
                    tempSide = 'Close Reverse Repo'
                    tempPosition='Long'
                    tempSettlementLocationCustody='Deliver from Euroclear'
                    tempInstrumentName = 'Reverse Repo ' + str(round(i.repoRate,2)) + '% CLOSE'
                    tempAccuredInterest = i.accruedInt
                elif i.side =='B':
                    if i.status == 'Initial':
                        tempSide = 'Buy'
                        tempPosition='Long'
                    else:
                        tempSide = 'Repurchase'
                        tempPosition='Short'
                    tempSettlementLocationCustody='Settle in Euroclear'
#                     tempInstrumentName = i.securityName
                    tempissuerlist=i.securityName.split()
                    tempissuer=tempissuerlist[0]                    
                    tempInstrumentName = tempissuer+' ' + str(i.coupon)+'% ' +str(i.matureDate.year)  
                    tempAccuredInterest = i.accruedInt
                elif i.side =='S':
                    if i.status == 'Initial':
                        tempSide = 'Short Sell'
                        tempPosition='Short'
                    else:
                        tempSide = 'Sell'
                        tempPosition='Long'
                    tempSettlementLocationCustody='Deliver from Euroclear'
#                     tempInstrumentName = i.securityName
                    tempissuerlist=i.securityName.split()
                    tempissuer=tempissuerlist[0]                    
                    tempInstrumentName = tempissuer+' ' + str(i.coupon)+'% ' +str(i.matureDate.year) 
                    tempAccuredInterest = i.accruedInt                            
                if i.tranType=="FX":
                    q1=i.quantity
                    q2=i.coupon
                    c1=i.fxCurrType1
                    c2=i.fxCurrType2
                    tempCoupon=""
                elif i.tranType=='REPO' or i.tranType=='CREPO':
                    q1 = ""
                    q2 = ""
                    c1 = ""
                    c2 = ""
                    tempCoupon=i.repoRate
                else:
                    q1 = ""
                    q2 = ""
                    c1 = ""
                    c2 = ""
                    tempCoupon=i.coupon
                tempDirtyPrice = i.net/i.quantity*100
    
                writer.writerow({'Transaction Reference Number':i.seqNo,\
                                 'Fund Number':i.fundName,\
                                 'Fund Name':"Baldr Draco Fund Class B",\
                                 'Transaction Type':"NEW",\
                                 'Security Type': tempSecurityType,\
                                 'Trade Type': tempSide,\
                                 'Security Identifier':i.CUSIP,\
                                 'Instrument Name': tempInstrumentName,\
                                 'Trade Date': i.tradeDate.strftime('%m/%d/%Y'),\
                                 'Settlement Date': i.settleDate.strftime('%m/%d/%Y'),\
                                 'Maturity Date': i.matureDate.strftime('%m/%d/%Y'),\
                                 'Currency': i.currType,\
                                 'Quantity': i.quantity,\
                                 'Clean Price': i.price,\
                                 'Accured Interest': tempAccuredInterest,\
                                 'Commission':i.commission,\
                                 'Tax': i.tax,\
                                 'Fees': i.fee,\
                                 'Other Charges': i.charge,\
                                 'Net Settlement': i.net,\
                                 'Executing Broker': broker.brokerName,\
                                 'Executing Broker BIC' : broker.bic,\
                                 'Executing Safe Keeping account':"",\
                                 'Clearing BIC/Participant': broker.bic,\
                                 'Clearing Account': tempClearAccount,\
                                 'Settlement Location Broker':tempSettlementLocation,\
                                 'Settlement Location Custody':tempSettlementLocationCustody,\
                                 'Original Face':i.quantity,\
                                 'Index Ratio':i.factor,\
                                 'Current Face':i.quantity*i.factor,\
                                 'Accounting Only':"N",\
                                 'Custodian': "State Street : Share Class B",\
                                 'unit of Calc':"",\
                                 'Currency #1 amount for FX':q1,\
                                 'Settlement currency #1 for FX': c1,\
                                 'Currency #2 amount for FX': q2,\
                                 'Settlement currency #2 for FX':c2,\
                                 'FX Rate':fxrate,\
                                 'Basis':i.principal,\
                                 'ISIN': i.ISIN,\
                                 'Custody Only':"Y",\
                                 'CUSIP': i.CUSIP,\
                                 'Coupon': tempCoupon,\
                                 'Position':tempPosition,\
                                 'Dirty Price':tempDirtyPrice ,\
                                 'Liquidity Category':"",\
                                 'Risk Sub Category':"",\
                                 'Instrument Group':"",\
                                 'RED Pair':"",\
                                 'Start Date':"",\
                                 'First Coupon':"",\
                                 'Frequency':"",\
                                 'Day Count':"",\
                                 'Restructuring':""})
########################################################################################
    def CCM_trades_RANET(self):
        today = date.today()
#         fundtrades=g.dataBase.qTradeByFundName("AGCF",str(today))
        fundtrades1 = g.dataBase.qTradeByFundName("AGCF", "2017-06-14")
        fundtrades2 = g.dataBase.qTradeByFundName("ACPT", "2017-06-14")
        fundtrades3 = g.dataBase.qTradeByFundName("PGOF", "2017-06-14")
        fundtrades4 = g.dataBase.qTradeByFundName("HART", "2017-06-14")
        fundtrades5 = g.dataBase.qTradeByFundName("INC5", "2017-06-14")
        fundtrades6 = g.dataBase.qTradeByFundName("INC0", "2017-06-14")
        
        if len(fundtrades1)+len(fundtrades2)+len(fundtrades3)+len(fundtrades4)+len(fundtrades5)+len(fundtrades6)==0:
            return
        fundtrades0 = fundtrades1 + fundtrades2 + fundtrades3 + fundtrades4 + fundtrades5 + fundtrades6
        
        initialTrades =list()
        closeTrades = list()
        
        for i in fundtrades0:
            if i.status == 'Initial':
                initialTrades.append(i)
            elif i.status == 'Closed':
                closeTrades.append(i)
        fundtrades = initialTrades+closeTrades
        
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Admin\RANET\CCM Trades _" + datestamp + ".csv"
        # if (os.path.isfile(file):
    
        with open (file,'w') as csvfile:
            fieldsnames=['Type','Account','CUSIP/TICKER','ISIN','Buy/Sell','Inv Type','Issuer','Trade Date',\
                         'Settle Date','Coupon','Maturity','Currency','Original Notional','Current Notional',\
                         'FXRate','Price','Accured Interest','Commission','Cost','Counterparty','Counterparty BIC',\
                         'Safe Keeping Account','Clearing BIC','Clearing Account','Settlement Location','Trader','Trader Book','Remarks']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                tempTranType = ""
                if i.tranType == 'FX':
                    continue
                tempFXRate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                
                tempAI = i.accruedInt
                tempSettlementLocation=""
                tempClearAccount=""
                tempissuer = ""
                if i.tranType == 'EURO':
                    tempTranType = "Bond"
                    tempissuerlist=i.securityName.split()
                    tempissuer=tempissuerlist[0]
                elif i.tranType =='EQTY':
                    tempTranType = "Equity"
                elif i.tranType == 'REPO':
                    tempTranType = "Repos"
                    tempissuer='Repos'
                    tempAI = 0
                elif i.tranType=="CREPO":
                    tempTranType ="Repos"
                    tempissuer='Repos'
                elif i.tranType =="FUT":
                    tempissuer = "Futures"
                    tempTranType = "Futures"
                if broker.euroClear != None:
                    tempClearAccount=broker.euroClear
                    tempSettlementLocation="EUR"
                else:
                    tempClearAccount=broker.clearStream
                    tempSettlementLocation="CED"

                writer.writerow({ 'Type': i.status,\
                                  'Account': i.fundName, \
                                  'CUSIP/TICKER' : i.CUSIP, \
                                  'ISIN': i.ISIN, \
                                  'Buy/Sell': i.side, \
                                  'Inv Type': tempTranType, \
                                  'Issuer': tempissuer, \
                                  'Trade Date': i.tradeDate.strftime('%m/%d/%Y'), \
                                  'Settle Date': i.settleDate.strftime('%m/%d/%Y'), \
                                  'Coupon': i.coupon, \
                                  'Maturity':i.matureDate.strftime('%m/%d/%Y'), \
                                  'Currency': i.currType , \
                                  'Original Notional': str(i.quantity), \
                                  'Current Notional' : str(i.quantity*i.factor), \
                                  'FXRate':tempFXRate, \
                                  'Price': i.price, \
                                  'Accured Interest': tempAI, \
                                  'Commission': i.commission, \
                                  'Cost':i.net, \
                                  'Counterparty': broker.brokerName, \
                                  'Counterparty BIC':broker.bic,\
                                  'Safe Keeping Account':'',\
                                  'Clearing BIC':broker.bic,\
                                  'Clearing Account':tempClearAccount,\
                                  'Settlement Location':tempSettlementLocation,\
                                  'Trader':'',\
                                  'Trader Book':"Common",\
                                  'Remarks':i.remarks })
                
        file2 = "C:\TIMS_OutputFile\Files_to_Admin\RANET\CCM FXTrades _" + datestamp + ".csv"
        with open (file2,'w') as csvfile:
            fieldsnames=['Account','Trade Date','Settle Date','Forward/Spot','Side','Deal Currency','Deal Account','Deal Quantity',\
                         'FXRate','Base Quantity','Base Currency','Base Account','Counter Party','Trader']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            
            for i in fundtrades:
                if i.tranType != 'FX':
                    continue
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempFXType = "Forward"
                delta = i.settleDate - i.tradeDate
                if delta.days <=5 :
                    tempFXType = "Spot"
                writer.writerow({ 'Account': i.fundName, \
                                  'Trade Date': i.tradeDate, \
                                  'Settle Date': i.settleDate, \
                                  'Forward/Spot': tempFXType, \
                                  'Side':i.side,\
                                  'Deal Currency': i.fxCurrType1 , \
                                  'Deal Account': i.fxAccount1, \
                                  'Deal Quantity' : str(i.quantity), \
                                  'FXRate':i.price, \
                                  'Base Quantity': i.net, \
                                  'Base Currency': i.fxCurrType2, \
                                  'Base Account':i.fxAccount2,\
                                  'Counter Party':broker.brokerName,\
                                  'Trader':i.traderName})
########################################################################################    
    def CCM_NewSecurity_RANET(self):
        today = date.today()
        datestamp = today.strftime("%Y%m%d")
        newSecurityFile = "C:\TIMS_OutputFile\Files_to_Admin\RANET\CCM Trades _" + datestamp + ".csv"
        with open (newSecurityFile,'w') as csvfile:
            fieldsnames=['Issuer','Security Name','CUSIP','ISIN','Coupon','Maturity','Currency','Class']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
        csvfile.close()                 
########################################################################################
    def AGCF_Custody(self):
        today = date.today()
#         fundtrades=g.dataBase.qTradeByFundName("AGCF",str(today))
        fundtrades = g.dataBase.qTradeByFundName("AGCF", "2017-06-14")
        
        if len(fundtrades)==0:
            return
    
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Custody\AGCF\Trades AGCF " + datestamp + ".csv"
        # if (os.path.isfile(file):    
        with open (file,'w') as csvfile:
            fieldsnames=['Account','CUSIP/TICKER','ISIN','Buy/Sell','Inv Type','Issuer','Trade Date',\
                         'Settle Date','Coupon','Maturity','Currency','Original Notional','Current Notional',\
                         'FXRate','Price','Accured Interest','Commission','Cost','Counter Party','Euroclear','DTC','CEDEL']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                if i.custody != 'US Bank':
                    continue
                tempFXRate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempissuerlist=i.securityName.split()
                tempissuer=tempissuerlist[0]
                tempAI = i.accruedInt
                tempSettlementLocation=""
                tempEuroClearAccount=0
                tempClearStreamAccount=0
                tempSide = i.side
                
                if i.tranType == 'EURO':
                    tempTranType = "Bond"
                elif i.tranType =='EQTY':
                    tempTranType = "Equity"
                elif i.tranType == 'REPO':
                    tempTranType = "Repos"
                    tempAI = 0
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType=="CREPO":
                    tempTranType ="Repos"
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType == "FUT":
                    tempissuer = "Futures"
                    tempTranType = "Futures"
                    
                if broker.euroClear != None:
                    tempSettlementLocation = "EUR"
                    tempEuroClearAccount = broker.euroClear
                    tempClearStreamAccount = 0
                else:
                    tempSettlementLocation = "CED"
                    tempEuroClearAccount = 0
                    tempClearStreamAccount = broker.clearStream
                    
                if tempSide == 'S' and i.status =='Initial':
                    tempSide = 'Short Sell'
                elif tempSide == 'B' and i.status =='Close':
                    tempSide = 'Repurchase'
                
                writer.writerow({ 'Account': i.fundName, \
                                  'CUSIP/TICKER' : i.CUSIP, \
                                  'ISIN': i.ISIN, \
                                  'Buy/Sell': tempSide, \
                                  'Inv Type': tempTranType, \
                                  'Issuer': tempissuer, \
                                  'Trade Date': i.tradeDate.strftime('%m/%d/%Y'), \
                                  'Settle Date': i.settleDate.strftime('%m/%d/%Y'), \
                                  'Coupon': i.coupon, \
                                  'Maturity':i.matureDate.strftime('%m/%d/%Y'), \
                                  'Currency': i.currType , \
                                  'Original Notional': str(i.quantity), \
                                  'Current Notional' : str(i.quantity*i.factor), \
                                  'FXRate':tempFXRate, \
                                  'Price': i.price, \
                                  'Accured Interest': tempAI, \
                                  'Commission': i.commission, \
                                  'Cost':i.net, \
                                  'Counter Party': broker.brokerName, \
                                  'Euroclear':tempEuroClearAccount, \
                                  'DTC':'', \
                                  'CEDEL': tempClearStreamAccount })
####################################################################################
    def HART_Custody(self):
        today = date.today()
#         fundtrades=g.dataBase.qTradeByFundName("HART",str(today))
        fundtrades = g.dataBase.qTradeByFundName("HART", "2017-05-15")
        if len(fundtrades)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Custody\HART\Trades HART " + datestamp + ".csv"
        # if (os.path.isfile(file):
    
        with open (file,'w') as csvfile:
            fieldsnames=['Account','CUSIP/TICKER','ISIN','Buy/Sell','Inv Type','Issuer','Trade Date',\
                         'Settle Date','Coupon','Maturity','Currency','Original Notional','Current Notional',\
                         'FXRate','Price','Accured Interest','Commission','Cost','Counter Party','Euroclear','DTC','CEDEL']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                if i.custody != 'US Bank':
                    continue
                tempFXRate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempissuerlist=i.securityName.split()
                tempissuer=tempissuerlist[0]
                tempAI = i.accruedInt
                tempSettlementLocation=""
                tempEuroClearAccount=0
                tempClearStreamAccount=0
                tempSide = i.side
                
                if i.tranType == 'EURO':
                    tempTranType = "Bond"
                elif i.tranType =='EQTY':
                    tempTranType = "Equity"
                elif i.tranType == 'REPO':
                    tempTranType = "Repos"
                    tempAI = 0
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType=="CREPO":
                    tempTranType ="Repos"
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType == "FUT":
                    tempissuer = "Futures"
                    tempTranType = "Futures"
                    
                if broker.euroClear != None:
                    tempSettlementLocation = "EUR"
                    tempEuroClearAccount = broker.euroClear
                    tempClearStreamAccount = 0
                else:
                    tempSettlementLocation = "CED"
                    tempEuroClearAccount = 0
                    tempClearStreamAccount = broker.clearStream
                    
                if tempSide == 'S' and i.status =='Initial':
                    tempSide = 'Short Sell'
                elif tempSide == 'B' and i.status =='Close':
                    tempSide = 'Repurchase'
                
                writer.writerow({ 'Account': i.fundName, \
                                  'CUSIP/TICKER' : i.CUSIP, \
                                  'ISIN': i.ISIN, \
                                  'Buy/Sell': tempSide, \
                                  'Inv Type': tempTranType, \
                                  'Issuer': tempissuer, \
                                  'Trade Date': i.tradeDate.strftime('%m/%d/%Y'), \
                                  'Settle Date': i.settleDate.strftime('%m/%d/%Y'), \
                                  'Coupon': i.coupon, \
                                  'Maturity':i.matureDate.strftime('%m/%d/%Y'), \
                                  'Currency': i.currType , \
                                  'Original Notional': str(i.quantity), \
                                  'Current Notional' : str(i.quantity*i.factor), \
                                  'FXRate':tempFXRate, \
                                  'Price': i.price, \
                                  'Accured Interest': tempAI, \
                                  'Commission': i.commission, \
                                  'Cost':i.net, \
                                  'Counter Party': broker.brokerName, \
                                  'Euroclear':tempEuroClearAccount, \
                                  'DTC':'', \
                                  'CEDEL': tempClearStreamAccount })
#############################################################################
    def ACPT_Custody(self):
        today = date.today()
#         fundtrades=g.dataBase.qTradeByFundName("ACPT",str(today))
        fundtrades = g.dataBase.qTradeByFundName("ACPT", "2017-05-15")
        if len(fundtrades)==0:
            return        
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Custody\ACPT\Trades ACPT " + datestamp + ".csv"
        # if (os.path.isfile(file):
    
        with open (file,'w') as csvfile:
            fieldsnames=['Account','CUSIP/TICKER','ISIN','Buy/Sell','Inv Type','Issuer','Trade Date',\
                         'Settle Date','Coupon','Maturity','Currency','Original Notional','Current Notional',\
                         'FXRate','Price','Accured Interest','Commission','Cost','Counter Party','Euroclear','DTC','CEDEL']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                if i.custody != 'US Bank':
                    continue
                tempFXRate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempissuerlist=i.securityName.split()
                tempissuer=tempissuerlist[0]
                tempAI = i.accruedInt
                tempSettlementLocation=""
                tempEuroClearAccount=0
                tempClearStreamAccount=0
                tempSide = i.side
                
                if i.tranType == 'EURO':
                    tempTranType = "Bond"
                elif i.tranType =='EQTY':
                    tempTranType = "Equity"
                elif i.tranType == 'REPO':
                    tempTranType = "Repos"
                    tempAI = 0
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType=="CREPO":
                    tempTranType ="Repos"
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType == "FUT":
                    tempissuer = "Futures"
                    tempTranType = "Futures"
                    
                if broker.euroClear != None:
                    tempSettlementLocation = "EUR"
                    tempEuroClearAccount = broker.euroClear
                    tempClearStreamAccount = 0
                else:
                    tempSettlementLocation = "CED"
                    tempEuroClearAccount = 0
                    tempClearStreamAccount = broker.clearStream
                    
                if tempSide == 'S' and i.status =='Initial':
                    tempSide = 'Short Sell'
                elif tempSide == 'B' and i.status =='Close':
                    tempSide = 'Repurchase'
                
                writer.writerow({ 'Account': i.fundName, \
                                  'CUSIP/TICKER' : i.CUSIP, \
                                  'ISIN': i.ISIN, \
                                  'Buy/Sell': tempSide, \
                                  'Inv Type': tempTranType, \
                                  'Issuer': tempissuer, \
                                  'Trade Date': i.tradeDate.strftime('%m/%d/%Y'), \
                                  'Settle Date': i.settleDate.strftime('%m/%d/%Y'), \
                                  'Coupon': i.coupon, \
                                  'Maturity':i.matureDate.strftime('%m/%d/%Y'), \
                                  'Currency': i.currType , \
                                  'Original Notional': str(i.quantity), \
                                  'Current Notional' : str(i.quantity*i.factor), \
                                  'FXRate':tempFXRate, \
                                  'Price': i.price, \
                                  'Accured Interest': tempAI, \
                                  'Commission': i.commission, \
                                  'Cost':i.net, \
                                  'Counter Party': broker.brokerName, \
                                  'Euroclear':tempEuroClearAccount, \
                                  'DTC':'', \
                                  'CEDEL': tempClearStreamAccount })
###################################################################################
    def PGOF_Custody(self):
        today = date.today()
#         fundtrades=g.dataBase.qTradeByFundName("PGOF",str(today))
        fundtrades = g.dataBase.qTradeByFundName("PGOF", "2017-05-15")
        if len(fundtrades)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Custody\PGOF\Trades PGOF " + datestamp + ".csv"
        # if (os.path.isfile(file):
    
        with open (file,'w') as csvfile:
            fieldsnames=['Account','CUSIP/TICKER','ISIN','Buy/Sell','Inv Type','Issuer','Trade Date',\
                         'Settle Date','Coupon','Maturity','Currency','Original Notional','Current Notional',\
                         'FXRate','Price','Accured Interest','Commission','Cost','Counter Party','Euroclear','DTC','CEDEL']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                if i.custody != 'US Bank':
                    continue
                tempFXRate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempissuerlist=i.securityName.split()
                tempissuer=tempissuerlist[0]
                tempAI = i.accruedInt
                tempSettlementLocation=""
                tempEuroClearAccount=0
                tempClearStreamAccount=0
                tempSide = i.side
                
                if i.tranType == 'EURO':
                    tempTranType = "Bond"
                elif i.tranType =='EQTY':
                    tempTranType = "Equity"
                elif i.tranType == 'REPO':
                    tempTranType = "Repos"
                    tempAI = 0
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType=="CREPO":
                    tempTranType ="Repos"
                    tempCoupon = i.repoRate
                    tempissuer = 'Repos'
                elif i.tranType == "FUT":
                    tempissuer = "Futures"
                    tempTranType = "Futures"
                    
                if broker.euroClear != None:
                    tempSettlementLocation = "EUR"
                    tempEuroClearAccount = broker.euroClear
                    tempClearStreamAccount = 0
                else:
                    tempSettlementLocation = "CED"
                    tempEuroClearAccount = 0
                    tempClearStreamAccount = broker.clearStream
                    
                if tempSide == 'S' and i.status =='Initial':
                    tempSide = 'Short Sell'
                elif tempSide == 'B' and i.status =='Close':
                    tempSide = 'Repurchase'
                
                writer.writerow({ 'Account': i.fundName, \
                                  'CUSIP/TICKER' : i.CUSIP, \
                                  'ISIN': i.ISIN, \
                                  'Buy/Sell': tempSide, \
                                  'Inv Type': tempTranType, \
                                  'Issuer': tempissuer, \
                                  'Trade Date': i.tradeDate.strftime('%m/%d/%Y'), \
                                  'Settle Date': i.settleDate.strftime('%m/%d/%Y'), \
                                  'Coupon': i.coupon, \
                                  'Maturity':i.matureDate.strftime('%m/%d/%Y'), \
                                  'Currency': i.currType , \
                                  'Original Notional': str(i.quantity), \
                                  'Current Notional' : str(i.quantity*i.factor), \
                                  'FXRate':tempFXRate, \
                                  'Price': i.price, \
                                  'Accured Interest': tempAI, \
                                  'Commission': i.commission, \
                                  'Cost':i.net, \
                                  'Counter Party': broker.brokerName, \
                                  'Euroclear':tempEuroClearAccount, \
                                  'DTC':'', \
                                  'CEDEL': tempClearStreamAccount })
##########################################################################################
    def INC__Repo_Custody(self):
        today = date.today()
#         fundtrades1 = g.dataBase.qTradeByFundName("INC5",str(today))
#         fundtrades2 = g.dataBase.qTradeByFundName("INC0",str(today))
        fundtrades1 = g.dataBase.qTradeByFundName("INC5", "2017-06-26")
        fundtrades2 = g.dataBase.qTradeByFundName("INC0", "2017-06-26")
        if len(fundtrades1)+len(fundtrades2)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Custody\INC5\INC5_Repos_" + datestamp + "_ss"+ ".csv"
    
        with open (file,'w') as csvfile:
            fieldsnames=['Transaction Reference Number','Fund Number','Fund Name','Transaction Type','Security Type',\
                         'Trade Type','Security Identifier','Instrument Name','Trade Date','Settlement Date',\
                         'Maturity Date','Currency','Quantity','Clean Price','Accured Interest',\
                         'Commission','Tax','Fees','Other Charges','Net Settlement',\
                         'Executing Broker','Executing Broker BIC','Executing Safe Keeping account','Clearing BIC/Participant',\
                         'Clearing Account','Settlement Location Broker','Settlement Location Custody','Original Face',\
                         'Index Ratio','Current Face','Accounting Only','Custodian','unit of Calc','Currency #1 amount for FX',\
                         'Settlement currency #1 for FX','Currency #2 amount for FX','Settlement currency #2 for FX','FX Rate',\
                         'Basis','ISIN','Custody Only','CUSIP', 'Coupon','Position','Dirty Price','Liquidity Category',\
                         'Risk Sub Category','Instrument Group','RED Pair','Start Date','First Coupon', 'Frequency','Day Count',\
                         'Restructuring']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades1:
                if i.tranType=="REPO" or i.tranType=="CREPO":
                    fxrate = g.currency.get(i.currType)
                    a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                    broker=a[0]
                    tempClearAccount=0
                    tempSettlementLocation=''
                    tempSecurityType=''
                    tempSettlementLocationCustody=''
                    tempSide = ''
                    tempPosition = ''
                    tempAccuredInterest = 0
                    if len(str(broker.euroClear))!=0:
                        tempClearAccount=broker.euroClear
                        tempSettlementLocation="EUR"
                    else:
                        tempClearAccount=broker.clearStream
                        tempSettlementLocation="CED"
                    if i.tranType=='EURO':
                        tempSecurityType ='Bond'
                    elif i.tranType=='EQTY':
                        tempSecurityType='Equity'
                    elif i.tranType=='REPO' or i.tranType=='CREPO':
                        tempSecurityType='Repos'
                    if i.side=='B' and i.tranType=='REPO':
                        tempSide = 'Open Reverse Repo'
                        tempPosition ='Long'
                        tempSettlementLocationCustody='Settle in Euroclear'
                        tempInstrumentName = 'Reverse Repo ' + str(round(i.repoRate,2)) + '% OPEN'
                        tempAccuredInterest = 0
                    elif i.side=='S'and i.tranType=='REPO':
                        tempSide = 'Open Repo'
                        tempPosition ='Short'
                        tempSettlementLocationCustody='Deliver from Euroclear'
                        tempInstrumentName = 'Repo ' + str(round(i.repoRate,2)) + '% OPEN'
                        tempAccuredInterest = 0
                    elif i.side=='B'and i.tranType=='CREPO':
                        tempSide = 'Close Repo'
                        tempPosition ='Short'
                        tempSettlementLocationCustody='Settle in Euroclear'
                        tempInstrumentName = 'Repo ' + str(round(i.repoRate,2)) + '% CLOSE'
                        tempAccuredInterest = i.accruedInt
                    elif i.side=='S'and i.tranType=='CREPO':
                        tempSide = 'Close Reverse Repo'
                        tempPosition ='Long'
                        tempSettlementLocationCustody='Deliver from Euroclear'
                        tempInstrumentName = 'Reverse Repo ' + str(round(i.repoRate,2)) + '% CLOSE'
                        tempAccuredInterest = i.accruedInt                  
    
                    writer.writerow({'Transaction Reference Number': i.seqNo,\
                                     'Fund Number':i.fundName,\
                                     'Fund Name':"Baldr Draco Fund",\
                                     'Transaction Type':"NEW",\
                                     'Security Type': tempSecurityType,\
                                     'Trade Type': tempSide,\
                                     'Security Identifier':i.CUSIP,\
                                     'Instrument Name': tempInstrumentName,\
                                     'Trade Date': i.tradeDate.strftime("%m/%d/%Y"),\
                                     'Settlement Date': i.settleDate.strftime("%m/%d/%Y"),\
                                     'Maturity Date': i.matureDate.strftime("%m/%d/%Y"),\
                                     'Currency': i.currType,\
                                     'Quantity': i.quantity,\
                                     'Clean Price': i.price,\
                                     'Accured Interest': tempAccuredInterest,\
                                     'Commission':i.commission,\
                                     'Tax': i.tax,\
                                     'Fees': i.fee,\
                                     'Other Charges': i.charge,\
                                     'Net Settlement': i.net,
                                     'Executing Broker': broker.brokerName,\
                                     'Executing Broker BIC' : broker.bic,\
                                     'Executing Safe Keeping account':"",\
                                     'Clearing BIC/Participant': broker.bic,\
                                     'Clearing Account': tempClearAccount,\
                                     'Settlement Location Broker':tempSettlementLocation,\
                                     'Settlement Location Custody':tempSettlementLocationCustody,\
                                     'Original Face':i.quantity,\
                                     'Index Ratio':1,\
                                     'Current Face':i.quantity,\
                                     'Accounting Only':"N",\
                                     'Custodian': "State Street : Share Class A",\
                                     'unit of Calc':"",\
                                     'Currency #1 amount for FX':"",\
                                     'Settlement currency #1 for FX': "",\
                                     'Currency #2 amount for FX': "",\
                                     'Settlement currency #2 for FX':"",\
                                     'FX Rate':fxrate,\
                                     'Basis':i.principal,\
                                     'ISIN': i.ISIN,\
                                     'Custody Only':"Y",\
                                     'CUSIP': i.CUSIP,\
                                     'Coupon': i.repoRate,\
                                     'Position':tempPosition,\
                                     'Dirty Price':i.price,\
                                     'Liquidity Category':"",\
                                     'Risk Sub Category':"",\
                                     'Instrument Group':"",\
                                     'RED Pair':"",\
                                     'Start Date':"",\
                                     'First Coupon':"",\
                                     'Frequency':"",\
                                     'Day Count':"",\
                                     'Restructuring':""})
    
                #############################################
            for i in fundtrades2:
                if i.tranType=="REPO" or i.tranType=="CREPO":
                    fxrate = g.currency.get(i.currType)
                    a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                    broker=a[0]
                    tempClearAccount=0
                    tempSettlementLocation=''
                    tempSecurityType=''
                    tempSettlementLocationCustody=''
                    tempSide = ''
                    tempAccuredInterest = 0
                    if len(str(broker.euroClear))!=0:
                        tempClearAccount=broker.euroClear
                        tempSettlementLocation="EUR"
                    else:
                        tempClearAccount=broker.clearStream
                        tempSettlementLocation="CED"
                    if i.tranType=='EURO':
                        tempSecurityType ='Bond'
                    elif i.tranType=='EQTY':
                        tempSecurityType='Equity'
                    elif i.tranType=='REPO' or i.tranType=='CREPO':
                        tempSecurityType='Repos'
                    if i.side=='B' and i.tranType=='REPO':
                        tempSide = 'Open Reverse Repo'
                        tempPosition ='Long'
                        tempSettlementLocationCustody='Settle in Euroclear'
                        tempInstrumentName = 'Reverse Repo ' + str(round(i.repoRate,2))+ '% OPEN'
                        tempAccuredInterest = 0
                    elif i.side=='S'and i.tranType=='REPO':
                        tempSide = 'Open Repo'
                        tempPosition ='Short'
                        tempSettlementLocationCustody='Deliver from Euroclear'
                        tempInstrumentName = 'Repo ' + str(round(i.repoRate,2)) + '% OPEN'
                        tempAccuredInterest = 0
                    elif i.side=='B'and i.tranType=='CREPO':
                        tempSide = 'Close Repo'
                        tempPosition ='Short'
                        tempSettlementLocationCustody='Settle in Euroclear'
                        tempInstrumentName = 'Repo ' + str(round(i.repoRate,2))+ '% CLOSE'
                        tempAccuredInterest = i.accruedInt
                    elif i.side=='S'and i.tranType=='CREPO':
                        tempSide = 'Close Reverse Repo'
                        tempPosition ='Long'
                        tempSettlementLocationCustody='Deliver from Euroclear'
                        tempInstrumentName = 'Reverse Repo ' + str(round(i.repoRate,2)) + '% CLOSE'
                        tempAccuredInterest = i.accruedInt                  
    
                    writer.writerow({'Transaction Reference Number': i.seqNo,\
                                     'Fund Number':i.fundName,\
                                     'Fund Name':"Baldr Draco Fund Class B",\
                                     'Transaction Type':"NEW",\
                                     'Security Type': tempSecurityType,\
                                     'Trade Type': tempSide,\
                                     'Security Identifier':i.CUSIP,\
                                     'Instrument Name': tempInstrumentName,\
                                     'Trade Date': i.tradeDate.strftime("%m/%d/%Y"),\
                                     'Settlement Date': i.settleDate.strftime("%m/%d/%Y"),\
                                     'Maturity Date': i.matureDate.strftime("%m/%d/%Y"),\
                                     'Currency': i.currType,\
                                     'Quantity': i.quantity,\
                                     'Clean Price': i.price,\
                                     'Accured Interest': tempAccuredInterest,\
                                     'Commission':i.commission,\
                                     'Tax': i.tax,\
                                     'Fees': i.fee,\
                                     'Other Charges': i.charge,\
                                     'Net Settlement': i.net,
                                     'Executing Broker': broker.brokerName,\
                                     'Executing Broker BIC' : broker.bic,\
                                     'Executing Safe Keeping account':"",\
                                     'Clearing BIC/Participant': broker.bic,\
                                     'Clearing Account': tempClearAccount,\
                                     'Settlement Location Broker':tempSettlementLocation,\
                                     'Settlement Location Custody':tempSettlementLocationCustody,\
                                     'Original Face':i.quantity,\
                                     'Index Ratio':1,\
                                     'Current Face':i.quantity,\
                                     'Accounting Only':"N",\
                                     'Custodian': "State Street : Share Class B",\
                                     'unit of Calc':"",\
                                     'Currency #1 amount for FX':"",\
                                     'Settlement currency #1 for FX': "",\
                                     'Currency #2 amount for FX': "",\
                                     'Settlement currency #2 for FX':"",\
                                     'FX Rate':"fxrate",\
                                     'Basis':i.principal,\
                                     'ISIN': i.ISIN,\
                                     'Custody Only':"Y",\
                                     'CUSIP': i.CUSIP,\
                                     'Coupon': i.repoRate,\
                                     'Position':tempPosition,\
                                     'Dirty Price':i.price,\
                                     'Liquidity Category':"",\
                                     'Risk Sub Category':"",\
                                     'Instrument Group':"",\
                                     'RED Pair':"",\
                                     'Start Date':"",\
                                     'First Coupon':"",\
                                     'Frequency':"",\
                                     'Day Count':"",\
                                     'Restructuring':""})
###########################################################################################
    def INC__Trade_Custody(self):
        today = date.today()
#         fundtrades1=g.dataBase.qTradeByFundName("INC5",str(today))
#         fundtrades2=g.dataBase.qTradeByFundName("INC0",str(today))
        fundtrades1 = g.dataBase.qTradeByFundName("INC5", "2017-05-15")
        fundtrades2 = g.dataBase.qTradeByFundName("INC0", "2017-05-15")
        if len(fundtrades1)+len(fundtrades2)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Custody\INC5\INC5_Trades_" + datestamp + "_ss"+ ".csv"
    
        with open (file,'w') as csvfile:
            fieldsnames=['Transaction Reference Number','Fund Number','Fund Name','Transaction Type','Security Type',\
                         'Trade Type','Security Identifier','Instrument Name','Trade Date','Settlement Date',\
                         'Maturity Date','Currency','Quantity','Clean Price','Accured Interest',\
                         'Commission','Tax','Fees','Other Charges','Net Settlement',\
                         'Executing Broker','Executing Broker BIC','Executing Safe Keeping account','Clearing BIC/Participant',\
                         'Clearing Account','Settlement Location Broker','Settlement Location Custody','Original Face',\
                         'Index Ratio','Current Face','Accounting Only','Custodian','unit of Calc','Currency #1 amount for FX',\
                         'Settlement currency #1 for FX','Currency #2 amount for FX','Settlement currency #2 for FX','FX Rate',\
                         'Basis','ISIN','Custody Only','CUSIP', 'Coupon','Position','Dirty Price','Liquidity Category',\
                         'Risk Sub Category','Instrument Group','RED Pair','Start Date','First Coupon', 'Frequency','Day Count',\
                         'Restructuring']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades1:
                if i.tranType!="REPO" and i.tranType!="CREPO" and i.tranType!="FX":
                    fxrate = g.currency.get(i.currType)
                    a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                    broker=a[0]
                    tempClearAccount=0
                    tempSettlementLocation=''
                    tempSecurityType=''
                    tempSettlementLocationCustody=''
                    tempSide = ''
                    tempPosition = ''
                    if len(str(broker.euroClear))!=0:
                        tempClearAccount=broker.euroClear
                        tempSettlementLocation="EUR"
                    else:
                        tempClearAccount=broker.clearStream
                        tempSettlementLocation="CED"
                    if i.tranType=='EURO':
                        tempSecurityType ='Bond'
                    elif i.tranType=='EQTY':
                        tempSecurityType='Equity'
                    elif i.tranType=='REPO' or i.tranType=='CREPO':
                        tempSecurityType='Repos'
                    if i.side=='B':
                        if i.status == 'Initial':
                            tempSide = 'Buy'
                            tempPosition='Long'
                        else:
                            tempSide = 'Repurchase'
                            tempPosition='Short'
                        tempissuerlist=i.securityName.split()
                        tempissuer=tempissuerlist[0]                    
                        tempInstrumentName = tempissuer+' ' + str(i.coupon)+'% ' +str(i.matureDate.year)  
                        tempSettlementLocationCustody='Settle in Euroclear'
                    elif i.side=='S':
                        if i.status == 'Initial':
                            tempSide = 'Short Sell'
                            tempPosition='Short'
                        else:
                            tempSide = 'Sell'
                            tempPosition='Long'
                        tempissuerlist=i.securityName.split()
                        tempissuer=tempissuerlist[0]                    
                        tempInstrumentName = tempissuer+' ' + str(i.coupon)+'% ' +str(i.matureDate.year) 
                        tempSettlementLocationCustody='Deliver from Euroclear'
                    tempDirtyPrice = i.net/i.quantity*100    
                    writer.writerow({'Transaction Reference Number': i.seqNo,\
                                     'Fund Number':i.fundName,\
                                     'Fund Name':"Baldr Draco Fund",\
                                     'Transaction Type':"NEW",\
                                     'Security Type': tempSecurityType,\
                                     'Trade Type': tempSide,\
                                     'Security Identifier':i.CUSIP,\
                                     'Instrument Name': tempInstrumentName,\
                                     'Trade Date': i.tradeDate.strftime("%m/%d/%Y"),\
                                     'Settlement Date': i.settleDate.strftime("%m/%d/%Y"),\
                                     'Maturity Date': i.matureDate.strftime("%m/%d/%Y"),\
                                     'Currency': i.currType,\
                                     'Quantity': i.quantity,\
                                     'Clean Price': i.price,\
                                     'Accured Interest': i.accruedInt,\
                                     'Commission':i.commission,\
                                     'Tax': i.tax,\
                                     'Fees': i.fee,\
                                     'Other Charges': i.charge,\
                                     'Net Settlement': i.net,\
                                     'Executing Broker': broker.brokerName,\
                                     'Executing Broker BIC' : broker.bic,\
                                     'Executing Safe Keeping account':"",\
                                     'Clearing BIC/Participant': broker.bic,\
                                     'Clearing Account': tempClearAccount,\
                                     'Settlement Location Broker':tempSettlementLocation,\
                                     'Settlement Location Custody':tempSettlementLocationCustody,\
                                     'Original Face':i.quantity,\
                                     'Index Ratio':i.factor,\
                                     'Current Face':i.quantity*i.factor,\
                                     'Accounting Only':"N",\
                                     'Custodian': 'State Street : Share Class A',\
                                     'unit of Calc':"",\
                                     'Currency #1 amount for FX':"",\
                                     'Settlement currency #1 for FX': "",\
                                     'Currency #2 amount for FX': "",\
                                     'Settlement currency #2 for FX':"",\
                                     'FX Rate':fxrate,\
                                     'Basis':i.principal,\
                                     'ISIN': i.ISIN,\
                                     'Custody Only':"Y",\
                                     'CUSIP': i.CUSIP,\
                                     'Coupon': i.coupon,\
                                     'Position':tempPosition,\
                                     'Dirty Price':tempDirtyPrice,\
                                     'Liquidity Category':"",\
                                     'Risk Sub Category':"",\
                                     'Instrument Group':"",\
                                     'RED Pair':"",\
                                     'Start Date':"",\
                                     'First Coupon':"",\
                                     'Frequency':"",\
                                     'Day Count':"",\
                                     'Restructuring':""})
    
                #############################################
            for i in fundtrades2:
                if i.tranType!="REPO" and i.tranType!="CREPO" and i.tranType!="FX":
                    fxrate = g.currency.get(i.currType)
                    a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                    broker=a[0]
                    tempClearAccount=0
                    tempSettlementLocation=''
                    tempSecurityType=''
                    tempSettlementLocationCustody=''
                    tempSide = ''
                    tempPosition = ''
                    if len(str(broker.euroClear))!=0:
                        tempClearAccount=broker.euroClear
                        tempSettlementLocation="EUR"
                    else:
                        tempClearAccount=broker.clearStream
                        tempSettlementLocation="CED"
                    if i.tranType=='EURO':
                        tempSecurityType ='Bond'
                    elif i.tranType=='EQTY':
                        tempSecurityType='Equity'
                    elif i.tranType=='REPO' or i.tranType=='CREPO':
                        tempSecurityType='Repos'
                    if i.side=='B':
                        if i.status == 'Initial':
                            tempSide = 'Buy'
                            tempPosition='Long'
                        else:
                            tempSide = 'Repurchase'
                            tempPosition='Short'
                        tempissuerlist=i.securityName.split()
                        tempissuer=tempissuerlist[0]                    
                        tempInstrumentName = tempissuer+' ' + str(i.coupon)+'% ' +str(i.matureDate.year)  
                        tempSettlementLocationCustody='Settle in Euroclear'
                    elif i.side=='S':
                        if i.status == 'Initial':
                            tempSide = 'Short Sell'
                            tempPosition='Short'
                        else:
                            tempSide = 'Sell'
                            tempPosition='Long'
                        tempissuerlist=i.securityName.split()
                        tempissuer=tempissuerlist[0]                    
                        tempInstrumentName = tempissuer+' ' + str(i.coupon)+'% ' +str(i.matureDate.year) 
                        tempSettlementLocationCustody='Deliver from Euroclear'
                    tempDirtyPrice = i.net/i.quantity*100    
                    writer.writerow({'Transaction Reference Number': i.seqNo,\
                                     'Fund Number':i.fundName,\
                                     'Fund Name':"Baldr Draco Fund",\
                                     'Transaction Type':"NEW",\
                                     'Security Type': tempSecurityType,\
                                     'Trade Type': tempSide,\
                                     'Security Identifier':i.CUSIP,\
                                     'Instrument Name': tempInstrumentName,\
                                     'Trade Date': i.tradeDate.strftime("%m/%d/%Y"),\
                                     'Settlement Date': i.settleDate.strftime("%m/%d/%Y"),\
                                     'Maturity Date': i.matureDate.strftime("%m/%d/%Y"),\
                                     'Currency': i.currType,\
                                     'Quantity': i.quantity,\
                                     'Clean Price': i.price,\
                                     'Accured Interest': i.accruedInt,\
                                     'Commission':i.commission,\
                                     'Tax': i.tax,\
                                     'Fees': i.fee,\
                                     'Other Charges': i.charge,\
                                     'Net Settlement': i.net,\
                                     'Executing Broker': broker.brokerName,\
                                     'Executing Broker BIC' : broker.bic,\
                                     'Executing Safe Keeping account':"",\
                                     'Clearing BIC/Participant': broker.bic,\
                                     'Clearing Account': tempClearAccount,\
                                     'Settlement Location Broker':tempSettlementLocation,\
                                     'Settlement Location Custody':tempSettlementLocationCustody,\
                                     'Original Face':i.quantity,\
                                     'Index Ratio':i.factor,\
                                     'Current Face':i.quantity*i.factor,\
                                     'Accounting Only':"N",\
                                     'Custodian': 'State Street : Share Class A',\
                                     'unit of Calc':"",\
                                     'Currency #1 amount for FX':"",\
                                     'Settlement currency #1 for FX': "",\
                                     'Currency #2 amount for FX': "",\
                                     'Settlement currency #2 for FX':"",\
                                     'FX Rate':fxrate,\
                                     'Basis':i.principal,\
                                     'ISIN': i.ISIN,\
                                     'Custody Only':"Y",\
                                     'CUSIP': i.CUSIP,\
                                     'Coupon': i.coupon,\
                                     'Position':tempPosition,\
                                     'Dirty Price':tempDirtyPrice,\
                                     'Liquidity Category':"",\
                                     'Risk Sub Category':"",\
                                     'Instrument Group':"",\
                                     'RED Pair':"",\
                                     'Start Date':"",\
                                     'First Coupon':"",\
                                     'Frequency':"",\
                                     'Day Count':"",\
                                     'Restructuring':""})
########################################################################################
    def PGOF_SpotDeal_Admin(self):
        today = date.today()
#         fundtrades=g.dataBase.qTradeByFundName("PGOF",str(today))
        fundtrades = g.dataBase.qTradeByFundName("PGOF", "2017-05-15")
        if len(fundtrades)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Admin\PGOF\CONSTELLATION.SpotDeal." + datestamp + ".csv"
        # if (os.path.isfile(file):
    
        with open (file,'w') as csvfile:
            fieldsnames=['dealtype','dealid','action','client','reserved01','reserved02','strategy','custodian','cashaccount',\
                         'counterparty','comments','state','tradedate','settlementdate','dealtcurrency','spotrate',\
                         'reserved03','buycurrency','buyamount','sellcurrency','sellamount','clearingfees',\
                         'blockid','blockamount','commissioncurrency','commission','reserved04','associateddealtype',\
                         'associateddealid','brokershortname','clientreference','preserveorder','datetimestamp']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                fxrate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                if len(str(broker.euroClear))!=0:
                    tempeuroclear=broker.euroClear
                    tempclearstream=""
                else:
                    tempeuroclear=""
                    tempclearstream=broker.clearStream
                if i.side=='S' or i.side=='Sell' or i.side == 'SLD':
                    bc=i.fxCurrType2
                    sc=i.fxCurrType1
                    bcq=i.coupon
                    scq=i.quantity
                else:
                    bc=i.fxCurrType1
                    sc=i.fxCurrType2
                    bcq=i.quantity
                    scq=i.quantity
    
                if i.tranType=="FX":
                    writer.writerow({ 'dealtype':'SpotDeal',\
                                      'dealid':i.seqNo,\
                                      'action':'NEW',\
                                      'client':'CONSTELLATION',\
                                      'reserved01':'',\
                                      'reserved02':'',\
                                      'strategy':'PERSEUS',\
                                      'custodian':i.custody,\
                                      #Format of Custodian might not be accepted
                                      'cashaccount':'',\
                                      #Include Cash Account
                                      'counterparty':broker.brokerName,\
                                      'comments':'',\
                                      'state':'Valid',\
                                      'tradedate': i.tradeDate,\
                                      'settlementdate': i.settleDate,\
                                      'dealtcurrency': '',\
                                      'spotrate':i.price,\
                                      'reserved03':'',\
                                      'buycurrency':bc,\
                                      'buyamount':bcq,\
                                      'sellcurrency':sc,\
                                      'sellamount':scq,\
                                      'clearingfees':'',\
                                      'blockid':'',\
                                      'blockamount':'',\
                                      'commissioncurrency':'',\
                                      'commission':i.commission,\
                                      'reserved04':'',\
                                      'associateddealtype':'',\
                                      'associateddealid':'',\
                                      'brokershortname':'',\
                                      'clientreference':'',\
                                      'preserveorder':'',\
                                      'datetimestamp':''})
##################################################################################################
    def PGOF_RepoDeal_Admin(self):
        today = date.today()
#         fundtrades=g.dataBase.qTradeByFundName("PGOF",str(today))
        fundtrades = g.dataBase.qTradeByFundName("PGOF", "2017-05-15")
        if len(fundtrades)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Admin\PGOF\CONSTELLATION.RepoDeal." + datestamp + ".csv"
        # if (os.path.isfile(file):
    
        with open (file,'w') as csvfile:
            fieldsnames=['dealtype','dealid','action','client','reserved01','reserved02','strategy','custodian','cashaccount',\
                         'counterparty','comments','state','tradedate','settlementdate','brokershortname','gosecid','cusip',\
                         'isin','sedol','reserved03','reserved04','securitydescription','transactionindicator',\
                         'subtransactionindicator','quantity','price','commission','tax','blockid','blockamount',\
                         'reserved05','reserved06','accrued','clearingmode','faceamount','reserved07','settlementcurrency',\
                         'reserved08','crosscurrencyrate','clientreference','reserved09','settlementamount','yield',\
                         'tradedatetimestamp','cpirefratio']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                fxrate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                if len(str(broker.euroClear))!=0:
                    tempeuroclear=broker.euroClear
                    tempclearstream=""
                else:
                    tempeuroclear=""
                    tempclearstream=broker.clearStream
                if i.side=='S' or i.side=='Sell' or i.side == 'SLD':
                    bc=i.fxCurrType2
                    sc=i.fxCurrType1
                    bcq=i.coupon
                    scq=i.quantity
                else:
                    bc=i.fxCurrType1
                    sc=i.fxCurrType2
                    bcq=i.quantity
                    scq=i.quantity
                if i.tranType=='REPO' and i.side=='B':
                    ti='Open'
                    si='Reverse Repo'
                if i.tranType=='REPO' and i.side =='S':
                    ti='Open'
                    si='Repo'
                if i.tranType=='CREPO' and i.side=='S':
                    ti='Close'
                    si='Reverse Repo'
                if i.tranType == 'REPO' and i.side == 'B':
                    ti = 'Close'
                    si = 'Repo'
    
                if i.tranType=="REPO" or i.tranType=="CREPO":
                    writer.writerow({'dealtype':'SpotDeal', \
                                     'dealid':i.seqNo,\
                                      'action':'NEW',\
                                      'client':'CONSTELLATION',\
                                      'reserved01':'',\
                                      'reserved02':'',\
                                      'strategy':'PERSEUS',\
                                      'custodian':i.custody, \
                                     # Format of Custodian might not be accepted
                                      'cashaccount':'', \
                                     # Include Cash Account
                                      'counterparty':broker.brokerName,\
                                      'comments':'',\
                                      'state':'Valid',\
                                      'tradedate': i.tradeDate,\
                                      'settlementdate': i.settleDate,\
                                      'brokershortname':'',\
                                      'gosecid':'',\
                                      'cusip':'',\
                                      'isin':i.ISIN,\
                                      'sedol':'',\
                                      'reserved03':'',\
                                      'reserved04':'',\
                                      'securitydescription': i.securityName,\
                                      'transactionindicator':ti,\
                                      'subtransactionindicator':si,\
                                      'quantity':(i.quantity/100),\
                                      'price':i.price,\
                                      'commission':i.commission,\
                                      'tax':i.tax,\
                                      'blockid':'',\
                                      'blockamount':'',\
                                      'reserved05':'',\
                                      'reserved06':'',\
                                      'accrued':i.accruedInt,\
                                      'clearingmode':'',\
                                      'faceamount':i.quantity,\
                                      'reserved07':'',\
                                      'settlementcurrency':i.currType,\
                                      'reserved08':'',\
                                      'crosscurrencyrate':fxrate,\
                                      'clientreference':'',\
                                      'reserved09':'',\
                                      'settlementamount':(i.price * i.quantity ),\
                                      'yield':i.y,\
                                      'tradedatetimestamp':'',\
                                      'cpirefratio':''})
################################################################################################################
    def PGOF_EquityDeal_Admin(self):
        today = date.today()
        fundtrades=g.dataBase.qTradeByFundName("PGFO",str(today))
        fundtrades = g.dataBase.qTradeByFundName("PGOF", "2017-05-15")
        if len(fundtrades)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Admin\PGOF\CONSTELLATION.EquityDeal." + datestamp + ".csv"
        # if (os.path.isfile(file):
    
        with open (file,'w') as csvfile:
            fieldsnames=['dealtype','dealid','action','client','reserved01','reserved02','strategy','custodian','cashaccount',\
                         'counterparty','comments','state','tradedate','settlementdate','reserved03','gosecid','cusip','isin',\
                         'sedol','bbergticker','ric','securitydescription','transactionindicator','subtransactionindicator',\
                         'quantity','price','commission','secfee','vat','tradecurrency','exchangerate','reserved04','brokershortname',\
                         'clearingmode','exchange','clientreference','reserved05','securitycurrency','blockid','blockamount',\
                         'tradedatetimestamp']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                if i.tranType!="EQTY" or i.tranType!="STK":
                    continue
                fxrate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempClearAccount = 0
                tempClearLocation = ''
                if len(str(broker.euroClear))!=0:
                    tempClearAccount=broker.euroClear
                    tempClearLocation="EUR"
                else:
                    tempClearAccount=broker.clearStream
                    tempClearLocation='CED'                
                if i.side=='B':
                    tempSide='Buy'
                elif i.side=='S':
                    tempSide='Sell'
                if i.custody == 'US Bank':
                    tempCustodian = 'USBANK'
                    tempCashAccount ='UKNCOQAAPB'
                elif i.custody == 'Interctive Broker':
                    tempCustodian = 'INTBR'
                    tempCashAccount ='IANCOQAAPB'                
                writer.writerow({'dealtype':'EquityDeal',\
                                 'dealid':i.seqNo,\
                                 'action':"NEW",\
                                 'client':'CONSTELLATION',\
                                 'reserved01':'',\
                                 'reserved02':'',\
                                 'strategy':'PERSEUS',\
                                 'custodian':tempCustodian,\
                                 'cashaccount':tempCashAccount,\
                                 'counterparty':broker.brokerName,\
                                 'comments':'',\
                                 'state':'Valid',\
                                 'tradedate':i.tradeDate,\
                                 'settlementdate':i.settleDate,\
                                 'reserved03':'',\
                                 'gosecid':'',\
                                 'cusip':i.CUSIP,\
                                 'isin':i.ISIN,\
                                 'sedol':'',\
                                 'bbergticker':'',\
                                 'ric':'',\
                                 'securitydescription':i.securityName,\
                                 'transactionindicator':tempSide,\
                                 'subtransactionindicator':'',\
                                 #BuyLong or SellShort.....
                                 'quantity':i.quantity,
                                 'price':i.price,\
                                 'commission':i.commission,\
                                 'secfee':'',\
                                 'vat':'',\
                                 'tradecurrency':i.currType,\
                                 'exchangerate':fxrate,\
                                 'reserved04':'',\
                                 'brokershortname':'',\
                                 'clearingmode':'',\
                                 'exchange':'',\
                                 'clientreference':'',\
                                 'reserved05':'',\
                                 'securitycurrency':i.currType,\
                                 'blockid':'',\
                                 'blockamount':'',\
                                 'tradedatetimestamp':''})
###########################################################################################################
    def PGOF_BondDeal_Admin(self):
        today = date.today()
        fundtrades=g.dataBase.qTradeByFundName("PGOF",str(today))
        fundtrades = g.dataBase.qTradeByFundName("PGOF", "2017-05-15")
        if len(fundtrades)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Admin\PGOF\CONSTELLATION.BondDeal." + datestamp + ".csv"
        # if (os.path.isfile(file):
    
        with open (file,'w') as csvfile:
            fieldsnames=['dealtype','dealid','action','client','reserved01','reserved02','strategy','custodian','cashaccount',\
                         'counterparty','comments','state','tradedate','settlementdate','brokershortname','gosecid','cusip',\
                         'isin','sedol','reserved03','reserved04','securitydescription','transactionindicator','subtransactionindicator',\
                         'quantity','price','commission','tax','blockid','blockamount','reserved05','reserved06','exp','clearingmode',\
                         'faceamount','reserved07','settlementcurrency','reserved08','crosscurrencyrate','clientreference','reserved09',\
                         'settlementamount','yield','tradedatetimestamp','cpirefratio']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades:
                tempCustodian = ""
                tempCashAccount = ""
                if i.tranType !='EURO':
                    continue
                fxrate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0]
                tempClearAccount = 0
                tempClearLocation = ''
                tempCustodian=''
                tempCashAccount=''
                if len(str(broker.euroClear))!=0:
                    tempClearAccount=broker.euroClear
                    tempClearLocation="EUR"
                else:
                    tempClearAccount=broker.clearStream
                    tempClearLocation='CED'
                if i.side=='S' or i.side=='Sell' or i.side == 'SLD':
                    bc=i.fxCurrType2
                    sc=i.fxCurrType1
                    bcq=i.coupon
                    scq=i.quantity
                else:
                    bc=i.fxCurrType1
                    sc=i.fxCurrType2
                    bcq=i.quantity
                    scq=i.quantity               
                if i.side=='B':
                    tempSide='Buy'
                elif i.side=='S':
                    tempSide='Sell'
                if i.custody == 'US Bank':
                    tempCustodian = 'USBANK'
                    tempCashAccount ='UKNCOQAAPB'
                elif i.custody == 'Interactive Broker':
                    tempCustodian = 'INTBR'
                    tempCashAccount ='IANCOQAAPB'
                writer.writerow({'dealtype':'BondDeal', \
                                 'dealid':i.seqNo, \
                                 'action':"NEW", \
                                 'client':'CONSTELLATION', \
                                 'reserved01':'', \
                                 'reserved02':'', \
                                 'strategy':'PERSEUS', \
                                 'custodian':tempCustodian, \
                                 'cashaccount':tempCashAccount, \
                                 'counterparty':broker.brokerName, \
                                 #brokerCode is different from this admin
                                 'comments':'', \
                                 'state':'Valid', \
                                 'tradedate':i.tradeDate, \
                                 'settlementdate':i.settleDate, \
                                 'brokershortname':'',\
                                 'gosecid':'',\
                                 'cusip':i.CUSIP,\
                                 'isin':i.ISIN,\
                                 'sedol':'',\
                                 'reserved03':'',\
                                 'reserved04':'',\
                                 'securitydescription':i.securityName,\
                                 'transactionindicator':tempSide,\
                                 'subtransactionindicator':'', \
                                 # BuyLong or SellShort.....
                                 'quantity':(i.quantity/100),\
                                 'price': i.price,\
                                 'commission': i.commission,\
                                 'tax':i.tax,\
                                 'blockid':'',\
                                 'blockamount':'',\
                                 'reserved05':'',\
                                 'reserved06':'',\
                                 'exp':'',\
                                 'clearingmode':tempClearLocation,\
                                 'faceamount': i.quantity,\
                                 'reserved07':'',\
                                 'settlementcurrency': i.currType,\
                                 'reserved08': '',\
                                 'crosscurrencyrate':fxrate,\
                                 'clientreference':'',\
                                 'reserved09':'',\
                                 'settlementamount':i.net,\
                                 'yield':'',\
                                 'tradedatetimestamp':'',\
                                 'cpirefratio':''})
########################################################################################################
    def USBank_generic(self):
        today = date.today()
#         fundtrades1=g.dataBase.qTradeByFundName("AGCF",str(today))
#         fundtrades2=g.dataBase.qTradeByFundName("ACPT",str(today))
#         fundtrades3=g.dataBase.qTradeByFundName("PGOF",str(today))
#         fundtrades4=g.dataBase.qTradeByFundName("HART",str(today))
        fundtrades1 = g.dataBase.qTradeByFundName("AGCF", "2017-06-21")
        fundtrades2 = g.dataBase.qTradeByFundName("ACPT", "2017-06-21")
        fundtrades3 = g.dataBase.qTradeByFundName("PGOF", "2017-06-21")
        fundtrades4 = g.dataBase.qTradeByFundName("HART", "2017-06-21")
        fundtrades_combined = fundtrades1 + fundtrades2 + fundtrades3 + fundtrades4
        if len(fundtrades_combined)==0:
            return
        datestamp = today.strftime("%Y%m%d")
        file = "C:\TIMS_OutputFile\Files_to_Custody\USBank\\xf00.tg8towsp.tg00.USBank_Trades" + datestamp + ".csv"
        # if (os.path.isfile(file):    
        with open (file,'w') as csvfile:
            fieldsnames=['account','cusip','sedol','trade_date','settle_date','quantity','orig_face_amt','exec_price','commission_amt',\
                         'other_fees','exchange_fees','sec_fees','net_settlement_amount','principal','accrued_interest',\
                         'tran_code','executing_broker','executing_broker_name','executing_broker_ac','clearing_broker',\
                         'clearing_broker_ac','place_of_settlement','exch_rate_ind','execute_fx','foreign_ccy_iso_of_trade',\
                         'security_description','comments','security_type','transaction_fx_rate','fx_buy_ccy_iso',\
                         'fx_buy_ccy_amount','fx_buy_ccy_delivering_bic','fx_sell_ccy_iso','fx_sell_ccy_amount',\
                         'fx_sell_ccy_account_with_institution_bic','fx_sell_ccy_beneficiary_acct__',\
                         'fx_sell_ccy_beneficiary_bic','fx_sell_ccy_ffc_information']
            writer = csv.DictWriter(csvfile,fieldnames=fieldsnames, lineterminator='\n')
            writer.writeheader()
            for i in fundtrades_combined:
                if i.custody != 'US Bank':
                    continue
                fxrate = g.currency.get(i.currType)
                a = g.dataBase.qBrokerByBrokerCode(i.brokerName)
                broker=a[0] 
                tempClearAccount = 0
                tempClearBic =''
                tempSide = ''               
                if broker.euroClear!= None:
                    tempClearAccount=broker.euroClear
                    tempClearBic='MGTCBEBE'
                    clearmode="EUR"
                else:
                    tempClearAccount=broker.clearStream
                    tempClearBic='CEDELULL'
                    clearmode='CED'
                if i.side=='S' or i.side=='Sell' or i.side == 'SLD':
                    bc=i.fxCurrType2
                    sc=i.fxCurrType1
                    bcq=i.coupon
                    scq=i.quantity
                else:
                    bc=i.fxCurrType1
                    sc=i.fxCurrType2
                    bcq=i.quantity
                    scq=i.quantity
                tempSecurityType = ''
                if i.tranType=='REPO' and i.side=='B':
                    ti='Open'
                    si='Reverse Repo'                    
                if i.tranType=='REPO' and i.side =='S':
                    ti='Open'
                    si='Repo'
                if i.tranType=='CREPO' and i.side=='S':
                    ti='Close'
                    si='Reverse Repo'
                if i.tranType == 'REPO' and i.side == 'B':
                    ti = 'Close'
                    si = 'Repo'
                if i.tranType=='EURO':
                    tempSecurityType ='B'
                elif i.tranType=='EQTY':
                    tempSecurityType='E'
                elif i.tranType=='REPO' or i.tranType=='CREPO':
                    tempSecurityType='R'
                if i.side=='B':
                    if i.status == 'Initial':
                        tempSide='B'
                    elif i.status == 'Close':
                        tempSide='BC'
                elif i.side=='S':
                    if i.status == 'Initial':
                        tempSide='SS'
                    elif i.status == 'Close':
                        tempSide='S'
                elif i.side=='S':
                    side='Sell'
                if i.custody=="US Bank":
                    writer.writerow({'account':USBankAcc[i.fundName],\
                                     'cusip':i.ISIN,\
                                     'sedol':'',\
                                     'trade_date':i.tradeDate.strftime('%m/%d/%Y'),\
                                     'settle_date': i.settleDate.strftime('%m/%d/%Y'),\
                                     'quantity':i.quantity*i.factor,\
                                     'orig_face_amt':i.quantity,\
                                     'exec_price':i.price,\
                                     'commission_amt': i.commission,\
                                     'other_fees':i.fee,\
                                     'exchange_fees':'',\
                                     'sec_fees':'',\
                                     'net_settlement_amount':i.net,\
                                     #add this field
                                     'principal':i.principal,\
                                     'accrued_interest':i.accruedInt,\
                                     'tran_code':tempSide,\
                                     ##########complete following########
                                     'executing_broker':tempClearAccount,\
                                     'executing_broker_name':broker.brokerName,\
                                     'executing_broker_ac':'',\
                                     'clearing_broker':tempClearAccount,\
                                     'clearing_broker_ac':'',\
                                     'place_of_settlement':tempClearBic,\
                                     ######### use variable broker, ex.broker.brokerName################
                                     'exch_rate_ind':'',\
                                     'execute_fx':'N',\
                                     'foreign_ccy_iso_of_trade':i.currType,\
                                     'security_description':i.securityName,\
                                     'comments':'',\
                                     'security_type': tempSecurityType,\
                                     'transaction_fx_rate':fxrate,\
                                     'fx_buy_ccy_iso':'',\
                                     'fx_buy_ccy_amount':'',\
                                     'fx_buy_ccy_delivering_bic':'',\
                                     'fx_sell_ccy_iso':'',\
                                     'fx_sell_ccy_amount':'',\
                                     'fx_sell_ccy_account_with_institution_bic':'',\
                                     'fx_sell_ccy_beneficiary_acct__':'',\
                                     'fx_sell_ccy_beneficiary_bic':'',\
                                     'fx_sell_ccy_ffc_information':''})