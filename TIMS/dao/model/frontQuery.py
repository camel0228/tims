class FrontQuery:
    fundName = None
    securityName = None
    securityType = None
    coupon = None
    maturity = None
    currency = None
    quantity = None
    price = None    # 100
    principal = None
    factor = None
    marketValue = None  # quantity*factor*price + accruedInterest
    marketValuePercent = None
    unrealizedGL = None
    ISIN = None
    position = None