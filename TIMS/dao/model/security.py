from datetime import date

class Security:
    securityNo = ""
    securityName = ""
    securityType = ""
    CUSIP = ""
    ISIN = ""
    bloombergId = ""
    issuer = ""
    coupon = 0
    couponType = ""
    couponFreq = 2
    matureDate = date(2050,1,1)
    currType = ""
    factor = 1
    yesPrice = 0
    monthPrice = 0
    currPrice = 0
    moodyRating = ""
    spRating = ""
    fitchRating = ""
    comRating = ""
    duration = 0
    y = 0
    spread = 0
    category1 = ""
    category2 = ""
    issueDate = ""
    reserve1 = ""
    reserve2 = ""
    reserve3 = ""     # Bloomberg unique No.
    reserve4 = ""     # Default or not
    reserve5 = ""
    reserve6 = ""
    reserve7 = ""
    reserve8 = ""
    firstCoupDt = ""