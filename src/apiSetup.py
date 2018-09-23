from binance.client import Client
import json

fp = open('key.json','r')
keys = json.load(fp)

client = Client(keys['api_key'], keys['secret_key'])
# get market depth
depth = client.get_order_book(symbol='BNBBTC')
print(depth)


# fetch list of withdrawals
# withdraws = client.get_withdraw_history()
# print(withdraws)
# 
# trades = client.get_my_trades(symbol='ETHUSDT')
# print(trades)

fees = client.get_trade_fee()
print(fees)
print('others')