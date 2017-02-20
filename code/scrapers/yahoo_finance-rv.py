from yahoo_finance import Share
from yahoo_finance import Currency
from pprint import pprint

yahoo = Share('YHOO')
yahoo.get_open()
yahoo.get_price()
yahoo.get_trade_datetime()



pprint(yahoo.get_historical('2014-04-25', '2014-04-29'))

eur_pln = Currency('EURPLN')

eur_pln.get_bid()