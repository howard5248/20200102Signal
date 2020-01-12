# 匯入模組
from haohaninfo import GOrder
import datetime

# Yuanta(元大證券)、Capital(群益證券)、Capital_Future(群益期貨)、Kgi(凱基證券)、Kgi_Future(凱基期貨)、Simulator(虛擬期貨)
Broker = 'Masterlink_Future'
PriceOffer = 'Simulator'

# match(成交資訊)、commission(委託資訊)、updn5(上下五檔資訊)
Kind = 'match'

# 取即時報價的商品代碼(GOrder內需先訂閱該商品)
Prod = 'TXFA0'

# 取得當天日期
Date = datetime.datetime.now().strftime("%Y/%m/%d")

# 定義報價指令的物件
GOQ = GOrder.GOQuote()
# 定義下單指令的物件
GOC = GOrder.GOCommand()

endTime = datetime.datetime.strptime('2020/1/3 16:33:10','%Y/%m/%d %H:%M:%S')
import tick2OHLC
A = tick2OHLC.tick2OHLC()
for row in GOQ.Describe(PriceOffer,Kind,Prod):
    time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    price = float(row[2])
    print(time,price)
    A.put(time,price)

    # if time >= endTime:
    #     GOQ.EndDescribe()