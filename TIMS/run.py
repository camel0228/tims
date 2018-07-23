from flask import Flask, render_template, flash, redirect, g, abort, session, url_for, request
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_openid import OpenID
from forms import LoginForm, TradeBlotterForm
from dao import db 
from service import serviceImpl
from config import basedir
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import date
from pymemcache.client.base import Client
import os, logging, csv, datetime, calendar
import json

app = Flask(__name__)
app.config.from_object('config')
# client = Client(('54.157.14.150', 11211))
client = Client(('127.0.0.1', 11211))
# dbAlchemy = SQLAlchemy(app)
# lm = LoginManager()
# lm.init_app(app)
# lm.login_view = 'login'
# oid = OpenID(app, os.path.join(basedir, 'tmp'))

logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# @lm.user_loader
# def load_user(id):
#     from models import User, ROLE_USER, ROLE_ADMIN
#     return User.query.get(int(id))

@app.before_request
def before_request():
#     g.user = current_user
    g.service = serviceImpl.Service()
    g.dataBase = db.DbConn()
    g.random = 0
    g.fundCode = {"ANDROMEDA":"AGCF", "BALDR DRACO":"INC5", "HARTZ":"HART", "BALDR DRACO SERIES B":"INC0","PERSEUS":"PGOF",\
                  "ASPEN CREEK":"ACPT","GOLDEN TREE":"GTAM", "PETRUS TACTICAL":"PTAC"}
    g.ibFund = {"U1320604":"AGCF", "U1238201":"ACPT","U1681581":"PGOF","U1988095":"HART"}
    g.longTermGL = 0
    g.shortTermGL = 0
    g.queryRealizedGL = 0
#     g.client = Client(('localhost', 11211))
    g.reportDate = ''
    g.lastUptDt = "Last Updated on " + str(g.dataBase.qPriceHistory()[0].priceDate)
    g.cashComponent = g.service.getAvailCashFromReport()['Perseus']
    
@app.route('/index')
# @login_required
def main():
    try:
        g.service.fxRate()
    except IOError:
        logger.error("FX rate file does not exist!", exc_info = True)
        abort(401)
    
#     g.service.newSecurityFileGenerate()
            
    if g.service.fileNotEmpty("BBG"):
        g.service.tradeList()
        g.service.dataParsingForBBG()
        g.service.fileMovement("BBG")
    if g.service.fileNotEmpty("FX_TRADE"):
        g.service.fxList()
        g.service.dataParsingForFX()
        g.service.fileMovement("FX_TRADE")
    if g.service.fileNotEmpty("IB"):
        g.service.ibList()
        g.service.dataParsingForIB()
        g.service.fileMovement("IB")
    if g.service.fileNotEmpty("PRICE"):
        g.service.priceUpdateFromBBG()
#     g.service.counterpartyAlert()
    g.dataBase.commitment()
#     g.service.fileGenerator()
    
    return redirect(url_for('test'))

@app.route('/test')
# @login_required
def test():
    account = 'PGOF'
    countryLabelsList = list()
    countryWeightsList = list()
    positionListAll = list()
    positionListCategory = list()
    positionListCountry = list()
    positionListCurrency = list()
    cashFlowList = list()
    monthlyCashFlowList = list()
    returnList = [3.15, 0.01, 2.89, 3.39, -1.19, -4.05]
    monthlyReturn = [3.15, -2.62, 2.43, 0.49, -4.43, -2.89]
    accountValueYearStart = 20047906.31
    accountValueLastMonth = 19235422.92
    summary = db.frontSummary.FrontSummary()
    
    currList = g.dataBase.qOpenPositionCurrencyByFundName(account)
    for i in currList:
        tempDict = {}
        tempDict['name'] = str(i)
        tempDict['data'] = [0,0,0,0,0,0,0,0,0,0,0,0]
        monthlyCashFlowList.append(tempDict)
    
    countryList = g.dataBase.qOpenPositionCountryByCriteria(account)
    
    g.service.summaryCalculate(summary, account)
    g.service.positionListAdd(positionListAll, countryList, summary, account, 'all', cashFlowList, monthlyCashFlowList)
    g.service.positionListAdd(positionListCategory, countryList, summary, account, 'securityType', cashFlowList, monthlyCashFlowList)
    g.service.positionListAdd(positionListCountry, countryList, summary, account, 'category2', cashFlowList, monthlyCashFlowList)
    g.service.positionListAdd(positionListCurrency, countryList, summary, account, 'currType', cashFlowList, monthlyCashFlowList)
    g.service.countryDistribution(countryList, countryLabelsList, countryWeightsList, summary, account)
    g.service.calRealizedGL()
    
    currReturn = (summary.accountValue - accountValueLastMonth) / accountValueLastMonth
    accReturn = (1 + currReturn) * (1 + returnList[-1]/100) - 1
    returnList.append(round(accReturn * 100, 2))
    monthlyReturn.append(round(currReturn * 100, 2))
    client.set('unrealized_GL_YTD', int(accountValueYearStart * accReturn - g.longTermGL - g.shortTermGL))
    pnlFromReport = g.dataBase.qReport()[0]
    
    summary.dailyPNL = format(int(pnlFromReport.currAccValue) - int(pnlFromReport.yesAccValue), ',')
    summary.gainLossYTD = int(accountValueYearStart * accReturn - g.longTermGL - g.shortTermGL)
    summary.realizedGL = format(int(g.longTermGL + g.shortTermGL), ',')
    summary.accountValue = format(int(summary.accountValue), ',')
    summary.cash = format(int(summary.cash), ',')
    summary.marketValue = format(int(summary.marketValue), ',')
    summary.costBasis = format(int(summary.costBasis), ',')
    summary.gainLoss = format(int(summary.gainLoss), ',')
    summary.gainLossSumYTD = (format(int(accountValueYearStart * accReturn), ',') + "  /  {}%").format(str(round(accReturn * 100, 2)))
    
    g.service.updatePnlFromReport(summary.accountValue)
    
    client.set('positionListAll', positionListAll)
    client.set('positionListCategory', positionListCategory)
    client.set('positionListCountry', positionListCountry)
    client.set('positionListCurrency', positionListCurrency)
    client.set('countryWeightsList', countryWeightsList)
    client.set('countryLabelsList', countryLabelsList)
    client.set('cashFlowList', cashFlowList)
    client.set('monthlyCashFlowList', monthlyCashFlowList)
    client.set('returnList', returnList)
    client.set('monthlyReturn', monthlyReturn)
    client.set('shortTermGL', int(g.shortTermGL))
    client.set('longTermGL', int(g.longTermGL))
    client.set('accountValue', summary.accountValue)
    client.set('cash', summary.cash)
    client.set('marketValue', summary.marketValue)
    client.set('costBasis', summary.costBasis)
    client.set('gainLoss', summary.gainLoss)
    client.set('gainLossSumYTD', summary.gainLossSumYTD)
    client.set('dailyPNL', summary.dailyPNL)
    client.set('gainLossYTD', summary.gainLossYTD)
        
    return redirect(url_for('openPosition'))

@app.route('/op', methods=['GET', 'POST'])
# @login_required
def openPosition():
    account = request.args.get('account')
    group = request.args.get('group')
    if account == None:
        account = "PGOF"
    if group == None:
        group = "all"
    
    message = g.dataBase.qMessage()[0]
    
    if group == 'all':
        positionList = client.get('positionListAll')
    elif group == 'securityType':
        positionList = client.get('positionListCategory')
    elif group == 'category2':
        positionList = client.get('positionListCountry')
    else:
        positionList = client.get('positionListCurrency')
    
    return render_template("openPosition_flexibleTable.html", title = 'Open Position', positionList = positionList, 
                           country_weights_list = client.get('countryWeightsList'), 
                           country_labels_list = client.get('countryLabelsList'), account = account, 
                           group = group, cashFlowList = client.get('cashFlowList'), 
                           monthlyCashFlow = client.get('monthlyCashFlowList'), returnList = client.get('returnList'), 
                           monthlyReturn = client.get('monthlyReturn'), shortTermGL = client.get('shortTermGL'), 
                           longTermGL = client.get('longTermGL'), cash_component = g.cashComponent, lastUptDt = g.lastUptDt,
                           accountValue =  client.get('accountValue'), cash = client.get('cash'), 
                           marketValue = client.get('marketValue'), costBasis = client.get('costBasis'),
                           gainLoss = client.get('gainLoss'), gainLossSumYTD = client.get('gainLossSumYTD'),
                           dailyPNL = client.get('dailyPNL'), gainLossYTD = client.get('gainLossYTD'))

@app.route('/riskManagement', methods=['GET', 'POST'])
# @login_required
def riskManagement():
    portfolioConstituteList = g.service.portfolioConstitute('PGOF')
    return render_template("riskManagement.html", title = 'Risk Management', portfolioConstituteList = portfolioConstituteList) 

@app.route('/transView', methods=['GET', 'POST'])
# @login_required
def transView():
    form = FlaskForm()
    account = request.args.get('account')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    if account == None:
        account = "PGOF"
    if startDate == None:
        startDate = ""
    if endDate == None:
        endDate = ""
    if startDate != "" or endDate != "":
        if startDate == "":
            startDate = "0000-00-00"
        if endDate == "":
            endDate = "9999-99-99"
        listResult = g.dataBase.qTradeHistoryByDateRange(account, startDate, endDate)
    else:
        listResult = g.dataBase.qTradeHistoryByFundName(account)
#     p = Paginator(listResult, 30)
#     pageNo = request.args.get('pageNo')
#     try:
#         result = p.page(pageNo)
#     except PageNotAnInteger:
#         result = p.page(1)
#     except EmptyPage:
#         result = p.page(p.num_pages)
    return render_template("TransactionsView.html", title = 'Transactions', name = listResult, startDate = startDate, \
                           endDate = endDate, lastUptDt = g.lastUptDt) 

@app.route('/transSearch', methods=['GET', 'POST'])
# @login_required
def transSearch():
    form = FlaskForm()
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    criteria = str(request.args.get('criteria')).lower()
    if criteria == "bond":
        criteria = "EURO"
    if criteria == "equity":
        criteria = "EQTY"
    if criteria == "future":
        criteria = "FUT"
    if startDate == None:
        startDate = ""
    if endDate == None:
        endDate = ""
    listResult = g.dataBase.qFuzzyTradeHistory(criteria)
    return render_template("TransactionsView.html", title = 'Transactions', name = listResult, startDate = startDate, endDate = endDate)  

@app.route('/gl', methods=['GET', 'POST'])
# @login_required
def realizedGL():
    form = FlaskForm()
    account = request.args.get('account')
    if account == None:
        account = "PGOF"
    year = request.args.get('year')
    month = request.args.get('month')
    if year == "" or year == None:
        year = "2018"
    if month == None:
        month = "0"
    realizedGLList = g.service.realizedGLDetails(year, month)
    unGL = format(int(client.get('unrealized_GL_YTD')), ',')
    return render_template("RealizedGLDetails.html", title = 'Gain/Loss', realizedGLList = realizedGLList, account = account, \
                           lastUptDt = g.lastUptDt, year = year, month = month, unGL = unGL)

@app.route('/sh', methods=['GET', 'POST'])
# @login_required
def shareholdersView():
    form = FlaskForm()
    account = request.args.get('account')
    investor = request.args.get('investor')
    year = request.args.get('year')
    month = request.args.get('month')
    if account == None:
        account = "PGOF"
    if investor == None:
        investor = "Shahriar"
    if year == "" or year == None:
        year = "2018"
    yearView = year
    if month == None:
        month = str(datetime.datetime.now().month - 1)
        if month == "0":
            month = "12"
            yearView = str(int(year) - 1)
    monthRange = calendar.monthrange(int(yearView), int(month))
    if int(month) < 10:
        dateStart = '0' + month + '/' + '01/' + yearView 
        dateEnd = '0' + month + '/' + str(monthRange[1]) + '/' + yearView
    else:
        dateStart = month + '/' + '01/' + yearView 
        dateEnd = month + '/' + str(monthRange[1]) + '/' + yearView
    if int(year) >= datetime.datetime.now().year and int(month) >= datetime.datetime.now().month:
        shareholders = db.frontInvestPNL.FrontInvestPNL()
    else:
        shareholders = g.service.shareholderDetails(account, investor, year, month)
        shareholders.subscriptionRange = format(shareholders.subscriptionRange, ',')
        shareholders.subscriptionYear = format(shareholders.subscriptionYear, ',')
        shareholders.redemptionRange = format(shareholders.redemptionRange, ',')
        shareholders.redemptionYear = format(shareholders.redemptionYear, ',')
        shareholders.accountValueYearStart = format(shareholders.accountValueYearStart, ',')
        shareholders.accountValueStartDt = format(shareholders.accountValueStartDt, ',')
        shareholders.accountValueEndDt = format(shareholders.accountValueEndDt, ',')
        shareholders.deltaAccountValue = format(shareholders.deltaAccountValue, ',')
        shareholders.deltaAccountValueYTD = format(shareholders.deltaAccountValueYTD, ',')
        shareholders.currReturn = str(shareholders.currReturn) + "%"
        shareholders.ytdReturn = str(shareholders.ytdReturn) + "%"
    valueList, colorList, categoryList = g.service.shareholdersChart(account, investor)
    return render_template("InvestorReport.html", title = 'Shareholders', investor = investor, account = account, \
                           year = year, month = month, shareholders = shareholders, dateStart = dateStart, dateEnd = dateEnd, \
                           valueList = valueList, colorList = colorList, categoryList = categoryList) 

@app.route('/sh2', methods=['GET', 'POST'])
# @login_required
def shareholdersDetails():
    form = FlaskForm()
    account = request.args.get('account')
    investor = request.args.get('investor')
    if account == None:
        account = "PGOF"
    if investor == None:
        investor = "All"
    if investor == "All":
        investHistory = g.dataBase.qInvestHistory(account)
    else:
        investHistory = g.dataBase.qInvestHistoryByInvestorName(investor, account, "1900-01-01", "2099-12-31")
    return render_template("InvestorDetails.html", title = 'Shareholders', account = account, investHistory = investHistory, \
                           investor = investor)

# @app.route('/', methods=['GET', 'POST'])
# @app.route('/login', methods=['GET', 'POST'])
# @oid.loginhandler
# def login():
#     if g.user is not None and g.user.is_authenticated():
#         return redirect(url_for('openPosition'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         session['remember_me'] = form.remember_me.data
#         return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
#     return render_template('login.html', title='Sign In', form=form, providers=app.config['OPENID_PROVIDERS'])

# @oid.after_login
# def after_login(resp):
#     from models import User, ROLE_USER, ROLE_ADMIN
#     if resp.email is None or resp.email == "":
#         flash('Invalid login. Please try again.')
#         return redirect(url_for('login'))
#     user = User.query.filter_by(email=resp.email).first()
#     if user is None:
#         nickname = resp.nickname
#         if nickname is None or nickname == "":
#             nickname = resp.email.split('@')[0]
#         user = User(nickname=nickname, email=resp.email)
#         dbAlchemy.session.add(user)
#         dbAlchemy.session.commit()
#     remember_me = False
#     if 'remember_me' in session:
#         remember_me = session['remember_me']
#         session.pop('remember_me', None)
#     login_user(user, remember = remember_me)
#     return redirect(url_for('openPosition'))

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

@app.route('/tb', methods=['GET', 'POST'])
# @login_required
def tb():
    form = TradeBlotterForm()
    return render_template("TradeBlotter.html", title = 'Trader Blotter', form = form)

@app.route('/tb2', methods=['GET', 'POST'])
# @login_required
def tb2():
    form = TradeBlotterForm()
    tb = db.tradeBlotter.TradeBlotter()
    securityList = list()
    tb.isin = request.args.get('isin')
    tb.tradeDate = request.args.get('date')
    tb.time = request.args.get('time')
    securityList = g.dataBase.qSecurityByISIN(tb.isin)
    if len(securityList) == 0:
        return render_template("TradeBlotter2.html", title = 'Trader Blotter', form = form, isin = tb.isin, myDate = tb.tradeDate, myTime = tb.time)
    else:
        sName = securityList[0].securityName
        currType = securityList[0].currType
        sType = securityList[0].securityType
        if sType == "EURO" or sType == "FUT":
            return render_template("TradeBlotter2.html", title = 'Trader Blotter', form = form, name = sName, isin = tb.isin, myDate = tb.tradeDate, myTime = tb.time, currType = currType, sType = sType)
        elif sType == "EQTY":
            return render_template("TradeBlotter2.html", title = 'Trader Blotter', form = form, name = sName, isin = tb.isin, myDate = tb.tradeDate, myTime = tb.time, currType = currType, sType2 = sType)
        else:
            return render_template("TradeBlotter2.html", title = 'Trader Blotter', form = form, name = sName, isin = tb.isin, myDate = tb.tradeDate, myTime = tb.time, currType = currType)

@app.route('/tbView', methods=['GET', 'POST'])
# @login_required
def tbView():
    form = FlaskForm()
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    if form.validate_on_submit():
        return redirect(url_for('tb'))
    if startDate == None:
        startDate = ""
    if endDate == None:
        endDate = ""
    if startDate != "" or endDate != "":
        if startDate == "":
            startDate = "0000-00-00"
        if endDate == "":
            endDate = "9999-99-99"
        listResult = g.dataBase.qTradeBlotterWithinDate(startDate, endDate)
    else:
        listResult = g.dataBase.qTradeBlotter()
    return render_template("TradeBlotterView.html", title = 'Trade Blotter', name = listResult, startDate = startDate, endDate = endDate)

@app.route('/tbSubmit', methods=['GET', 'POST'])
# @login_required
def tbSubmit():
    form = TradeBlotterForm()
    tb = db.tradeBlotter.TradeBlotter()
    if form.validate_on_submit():
        tb.tradeDate = form['tradeDate'].data
        tb.time = form['time'].data
        tb.isin = form['isin'].data
        tb.securityName = form['securityName'].data
        tb.bs = form['bs'].data
        tb.quantity = form['quantity'].data
        tb.price = form['price'].data
        tb.currency = form['currency'].data
        tb.trader = str(form['trader'].data)
        tb.counterparty = form['counterparty'].data
        tb.salesTrader = form['salesTrader'].data
        tb.remark = form['remark'].data
        tb.status = "Applied"
        tb.book = form['book'].data
        tb.accounts = ""
        if form['AGCF'].data != "0":
            tb.accounts += "AGCF:" + form['AGCF'].data + " "
        if form['INC5'].data != "0":
            tb.accounts += "INC5:" + form['INC5'].data + " "
        if form['ACPT'].data != "0":
            tb.accounts += "ACPT:" + form['ACPT'].data + " "
        if form['PGOF'].data != "0":
            tb.accounts += "PGOF:" + form['PGOF'].data + " "
        if form['INC0'].data != "0":
            tb.accounts += "INC0:" + form['INC0'].data + " "
        if form['HART'].data != "0":
            tb.accounts += "HART:" + form['HART'].data
        g.dataBase.iTradeBlotter(tb)
        g.dataBase.commitment()
        listResult = g.dataBase.qTradeBlotter()
#         return render_template("TradeBlotterView.html", title = 'Trade Blotter', name = listResult)
        return redirect(url_for('tbView'))
    return render_template('TradeBlotter.html', title='ADD', form=form)

@app.route('/tbManage', methods=['GET', 'POST'])
# @login_required
def tbManage():
    form = FlaskForm()
    listResult = g.dataBase.qTradeBlotterByStatus("Applied")
    p = Paginator(listResult, 10)
    pageNo = request.args.get('pageNo')
    try:
        result = p.page(pageNo)
    except PageNotAnInteger:
        result = p.page(1)
    except EmptyPage:
        result = p.page(p.num_pages) 
    return render_template("TradeBlotterManage.html", title = 'Trade Blotter', name = result)

@app.route('/tbConfirm', methods=['GET', 'POST'])
# @login_required
def tbConfirm():
    tb = db.tradeBlotter.TradeBlotter()
    tb.id = request.args.get('id')
    tb.status = "Granted"
    g.dataBase.uStatusInTradeBlotter(tb)
    return redirect(url_for('tbManage'))

# @app.teardown_request
# def teardown_request(exception):
#     print("SUCCESS")

@app.errorhandler(404)  
def not_found(e):
#     g.service.emailAutoSend("Unauthorized counterparty detected, stop procedure!")  
    return render_template("404.html", msg = "Unauthorized counterparty detected, stop procedure!")

@app.errorhandler(401)  
def not_found(e):
    return render_template("401.html", msg = "File does not exist!")

if __name__=='__main__':
    app.run()