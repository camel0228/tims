import os, urllib
basedir = os.path.abspath(os.path.dirname(__file__))

# SQLALCHEMY_DATABASE_URI = 'mssql+pymssql://sa:Heron7056@127.0.0.1:1433/Test'
SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc://sa:Heron7056@127.0.0.1:1433/Test?driver=ODBC+Driver+13+for+SQL+Server'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Shahriar', 'url': 'https://me.yahoo.com/a/Hfoz1x9xoPKpXG6ZPBxtvePD5Vq7yHsBR0xzSwOxOkEAEqRWQnppRMTgVe6TGm_VYzO9YII-' },
    { 'name': 'Varun', 'url': 'https://me.yahoo.com/a/ga2hLEoErf.aU6MxWpgYE17qtAthxFn00_LSqqSg_NbU6sYYBYHRCGYqyYeg1QsYyCKlm48-' },
    { 'name': 'George', 'url': 'https://me.yahoo.com/a/7cx1rjVxs.tqVBuZenRVjekU5jAbxqIZY7WOuPszYKvrYu_Nn48VQCzs2yXQNR7vLwLBfN8-' },
    { 'name': 'Eugene', 'url': 'https://me.yahoo.com/a/Mvs08dEih4HF6hEXEhrrqfdh2KveZpV26Lh0a2cLxgUG5QMVeQWsg5MtxwT00ZRLjqWxeKk-' },
    { 'name': 'Phil', 'url': 'https://me.yahoo.com/a/b0Z8RXIEpM07TfFqkzJgGF_b9H2zbrdwTK7MdcAhoB8vleXSTbnuQsI.LUq1AkJAJmRyNrM-' },
    { 'name': 'Hong', 'url': 'https://me.yahoo.com/a/W7WGlIxog_FvdFM.WPcH1zsRPNer_XeOcZnFhOUqIMyTXReCKMjGGOcDcQC5xZYvMhX_YUE-' },
    { 'name': 'Qiang', 'url': 'https://me.yahoo.com/a/CddmH_phtf5wpSp4MytTYLPlE1YkySE5a40rM4pKy7Xas18XiayH40YduBFWwG_kOqZEMY0-' }]

# Bonds in AR
US040114GM64 = 'Warrent'
ARARGE03E139 = 'Sovereign'
XS0501195134 = 'Sovereign'
ARARGE03F441 = 'Provincial'
XS0209139244 = 'Warrent'
XS0205545840 = 'Sovereign'
XS1422866456 = 'Provincial'
USP79171AE79 = 'Provincial'
US040114HR43 = 'Sovereign'
US040114HQ69 = 'Sovereign'
USP989MJBL47 = 'Corporate'
US040114GK09 = 'Sovereign'

# Bonds in GR
GR0128012698 = 'Sovereign'
GR0138014809 = 'Sovereign'
GRR000000010 = 'Warrent'
GR0128013704 = 'Sovereign'
GR0114028534 = 'Sovereign'
GR0138005716 = 'Sovereign'
GR0133007204 = 'Sovereign'
GR0138007738 = 'Sovereign'
GR0114029540 = 'Sovereign'
GR0124034688 = 'Sovereign'
GR0133011248 = 'Sovereign'

# Bonds in VE
USP97475AN08 = 'Sovereign'
USP97475AG56 = 'Sovereign'
USP7807HAK16 = 'Quasi Sovereign'
XS0294364954 = 'Quasi Sovereign'
USP7807HAR68 = 'Quasi Sovereign'
USP7807HAT25 = 'Quasi Sovereign'
USP7807HAV70 = 'Quasi Sovereign'
XS0356521160 = 'Corporate'
USP17625AB33 = 'Sovereign'
XS1126891685 = 'Quasi Sovereign'
XS0294367205 = 'Quasi Sovereign'
USP7807HAM71 = 'Sovereign'

# Country Code
AR = 'Argentina' 
DE = 'Germany'
GR = 'Greece'
PH = 'Phllippine'
BR = 'Brazil'
VE = 'Venezuela'
UA = 'Ukraine'
US = 'United States'
RU = 'Russia'
KZ = 'Kazakhstan'
GB = 'United Kindom'
NL = 'Netherlands'
CH = 'Switzerland'
IL = 'Israel'
EC = 'Ecuador'
EG = 'Egypt'
NG = 'Nigeria'
JP = 'Japan'
AT = 'Austria'
CA = 'Canada'
CI = 'Ivory Coast'
CR = 'Costa Rica'
PE = 'Peru'
PR = 'Puerto Rico'
VN = 'Vietnam'
PA = 'Panama'
SA = 'Saudi Arabia'
OTHER_SOV = 'Other EM Sov'
OTHER_CORP = 'Other EM Corp'

# color code
COLOR_LAYER1_1 = '#b09733'
COLOR_LAYER1_2 = '#3aa255'
COLOR_LAYER1_3 = '#0aa3b5'
COLOR_LAYER1_4 = '#76c0cb'
COLOR_LAYER1_5 = '#c94930'
COLOR_LAYER1_6 = '#899893'
COLOR_LAYER1_7 = '#ddaf61'
COLOR_LAYER2_1 = '#ebb40f'
COLOR_LAYER2_2 = '#e1c315'
COLOR_LAYER2_3 = '#f7a128'
COLOR_LAYER2_4 = '#7eb138'
COLOR_LAYER2_5 = '#d0b24f'
COLOR_LAYER2_6 = '#ebb40f'
COLOR_LAYER2_7 = '#c1ba07'
COLOR_LAYER2_8 = '#718933'
COLOR_LAYER2_9 = '#3aa255'
COLOR_LAYER2_10 = '#03a653'
COLOR_LAYER2_11 = '#28b44b'
COLOR_LAYER2_12 = '#9db2b7'
COLOR_LAYER2_13 = '#beb276'
COLOR_LAYER2_14 = '#80a89d'
COLOR_LAYER2_15 = '#7a9bae'
COLOR_LAYER2_16 = '#5e777b'
COLOR_LAYER2_17 = '#c949305'
COLOR_LAYER2_18 = '#be8663'
COLOR_LAYER2_19 = '#a1743b'
COLOR_LAYER2_20 = '#b7906f'


