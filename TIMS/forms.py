from flask import g
from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, DateField, FloatField, SelectField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    openid = StringField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class TradeBlotterForm(FlaskForm):
    tradeDate = DateField('tradeDate', validators = [DataRequired()])
    time = StringField('time', validators = [DataRequired()])
    isin = StringField('isin', validators = [DataRequired()])
    securityName = StringField('securityName', validators = [DataRequired()])
#     bs = SelectField('bs', choices=[('B', 'BUY'), ('S', 'SELL'), ('SS', 'SHORT SELL'),('BTC', 'BUY TO COVER')], validators = [DataRequired()])
    bs = StringField('bs', validators = [DataRequired()])
    quantity = StringField('quantity', validators = [DataRequired()])
    price = FloatField('price', validators = [DataRequired()])
    currency = StringField('currency', validators = [DataRequired()])
#     trader = SelectMultipleField('trader', choices=[('SS', 'Shahriar'), ('VG', 'Varun'), ('GN', 'George')], validators = [DataRequired()])
    trader = StringField('trader', validators = [DataRequired()])
    accounts = StringField('accounts')
    AGCF = StringField('AGCF', validators = [DataRequired()])
    INC5 = StringField('INC5', validators = [DataRequired()])
    ACPT = StringField('ACPT', validators = [DataRequired()])
    PGOF = StringField('PGOF', validators = [DataRequired()])
    INC0 = StringField('INC0', validators = [DataRequired()])
    HART = StringField('HART', validators = [DataRequired()])
#     counterparty = StringField('counterparty', validators = [DataRequired()])
    counterparty = SelectField('counterparty', choices=[('',''),\
                                                        ('BA','Bank Of America'),\
                                                        ('BAIM','Banca IMI'),\
                                                        ('BARC','Barclays'),\
                                                        ('CG','Citigroup'),\
                                                        ('CSGN','Credit Suisse'),\
                                                        ('DBLA','Deutsche Bank'),\
                                                        ('GSCO','Goldman Sachs'),\
                                                        ('HTIB','Haitong Security'),\
                                                        ('ITBK','Interactive Brokers'),\
                                                        ('JP','JPMorgan'),\
                                                        ('MS','Morgan Stanley'),\
                                                        ('MZHO','Mizuho'),\
                                                        ('NOM','Nomura Securities'),\
                                                        ('SNC','Stifel Nicolaus'),\
                                                        ('UBSW','UBS'),\
                                                        ('ADAM','ADAM'),\
                                                        ('ADCA','Advanced Capital'),\
                                                        ('BBV','BBVA'),\
                                                        ('BCP','BCP Securities'),\
                                                        ('BMLA','Merril Lynch'),\
                                                        ('BMSA','Mariva'),\
                                                        ('BPXJ','BNP Paribas'),\
                                                        ('BRAI','Bradesco Security'),\
                                                        ('CBLN','Commerz Bank'),\
                                                        ('CF','Cantor Fitzgerald'),\
                                                        ('DRGN','Dragon Capital'),\
                                                        ('EDF','ED & F Man Capital'),\
                                                        ('EXOT','Exotix'),\
                                                        ('FB','Credit Suisse Repo'),\
                                                        ('GAZP','Gazprom Bank'),\
                                                        ('GMPE','GMP Securities'),\
                                                        ('GPBM','Gazprom Bank'),\
                                                        ('HSBC','HSBC'),\
                                                        ('JEF','Jefferies'),\
                                                        ('LEUM','Bank Leumi'),\
                                                        ('LFIM','Liquidity Finance'),\
                                                        ('MUSL','Mitsubishi UFJ Securities'),\
                                                        ('PECA','Pembroke'),\
                                                        ('PUEN','Puente'),\
                                                        ('RCAP','Renaissance Capital'),\
                                                        ('RZB','RB International Market'),\
                                                        ('SANT','Banco Santander'),\
                                                        ('SBER','Sberbank CIB USA'),\
                                                        ('SCLO','SC Lowy'),\
                                                        ('SEAP','The Seaport Group'),\
                                                        ('SSBK','State Street'),\
                                                        ('TPCG','TPCG Financial Services'),\
                                                        ('TRNO','Torino Capital LLC'),\
                                                        ('USBK','US bank'),\
                                                        ('VTBX','VTB Capital')], validators = [DataRequired()])
    salesTrader = StringField('salesTrader', validators = [DataRequired()])
    book = StringField('book', validators = [DataRequired()])
    remark = StringField('remark')
