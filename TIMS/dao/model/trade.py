class Trade:
    seqNo = ""
    tranType = ""
    CUSIP = ""
    ISIN = ""
    securityName = ""
    brokerName = ""
    fundName = ""
    customerName = ""
    traderName = ""
    side = ""
    currType = ""
    price = 0.0
    y = 0.0        #yield
    quantity = 0.0
    principal = 0.0
    coupon = 0.0
    accruedInt = 0.0
    repoRate = 0.0
    factor = 0.0
    net = 0.0
    principalInUSD = 0.0
    commission = 0.0
    tax = 0.0
    fee = 0.0
    charge = 0.0
    settleLocation = ""
    tradeDate = ""
    issueDate = ""
    settleDate = ""
    matureDate = ""
    dlrAlias = ""
    remarks = ""
    status = ""
    settled = ""
    custody = ""
    fxAccount1 = ""
    fxAccount2 = ""
    fxCurrType1 = ""
    fxCurrType2 = ""
    reserve1 = -10000
    reserve2 = 0.0
    reserve3 = ""
    reserve4 = ""
    source = ""
    securityType = ""     #only used to update status of tradehistory