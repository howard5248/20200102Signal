import datetime
import os
import tick2OHLC

pwd = 'C:\\Users\\Howard\\Desktop\\simulator\\20200110'
file = os.path.join(pwd,'TXFA0_Match.txt')

with open(file) as f:
    I020 = f.readlines()
    I020 = [i.strip('\n').split(',') for i in I020]


# A = tick2OHLC.tick2OHLC()
startTime = datetime.datetime.strptime('2020/1/10 08:45','%Y/%m/%d %H:%M')
A = tick2OHLC.tickPreproc(time=startTime,Tint=60)

time_list = []
price_list = []

endTime = datetime.datetime.strptime('2020/1/10 13:45:00','%Y/%m/%d %H:%M:%S')
# endTime = datetime.datetime.strptime('2020/1/9 00:11:03','%Y/%m/%d %H:%M:%S')
MA5_dict,MA10_dict,MA20_dict = {},{},{}
timeFlag_tmp = 0
KD9_dict = {}
KD9_value ={0:[50,50,100]}
for row in I020:
    time = datetime.datetime.strptime(row[0],'%Y/%m/%d %H:%M:%S.%f')
    if time <= startTime or time >= endTime: continue
    price = float(row[2])
    vol = int(row[3])
    BB_tmp = int(row[5])
    SS_tmp = int(row[6])
    time_list.append(time)
    price_list.append(price)

    # print(time,price)
    OHLCV = A.toOHLCV(time,price,vol)
    # print(OHLC[-1])
    closedata = [[i[0],i[4]] for i in OHLCV]
    MA5 = tick2OHLC.getMA(closedata,lenma=5)
    MA5_dict.update(MA5)
    MA10 = tick2OHLC.getMA(closedata, lenma=10)
    MA10_dict.update(MA10)
    MA20 = tick2OHLC.getMA(closedata, lenma=20)
    MA20_dict.update(MA20)
    timeFlag = OHLCV[-1][0]
    if timeFlag == timeFlag_tmp and len(KD9_dict) > 2:
        KD9_value = tick2OHLC.getKD(lenkd=9,data=OHLCV,KD=list(KD9_dict.values())[-2])
    else:
        timeFlag_tmp = timeFlag
        KD9_value = tick2OHLC.getKD(lenkd=9, data=OHLCV, KD=list(KD9_value.values())[0])
    KD9_dict.update(KD9_value)
    # print(OHLCV[-1][:5],',',list(KD9_value.values())[0])

    # if time > endTime: break
# for i in range(len(OHLC)):
#     print(OHLC[i],list(MA5_dict.values())[i],list(KD9_dict.values())[i])

def plotData1():
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import numpy as np

    fig, ax = plt.subplots(figsize=(16, 10))

    plotTime1 = datetime.datetime.strptime('2020/1/10 8:45', '%Y/%m/%d %H:%M')
    plotTime2 = datetime.datetime.strptime('2020/1/10 13:45', '%Y/%m/%d %H:%M')

    titleTime = plotTime1.strftime('%Y/%m/%d')
    ax.set_xlim(plotTime1,plotTime2)

    myFmt = mdates.DateFormatter('%m/%d %H:%M')
    ax.xaxis.set_major_formatter(myFmt)
    ax.xaxis.set_tick_params(labelsize=15)
    ymax = max(price_list) + (max(price_list)-min(price_list)) * 0.1
    ymin = min(price_list) - (max(price_list)-min(price_list)) * 0.1
    ax.set_yticklabels(np.arange(int(ymin), int(ymax)),fontdict={'size':15})
    plt.plot(time_list, price_list, color='k')
    plt.title(titleTime,fontdict={'size':20,'color':'r'})
    fig.autofmt_xdate()

    plt.plot(list(MA5_dict.keys()),list(MA5_dict.values()),color='r',label='MA5')
    plt.plot(list(MA10_dict.keys()),list(MA10_dict.values()),color='b',label='MA10')

    plt.legend()
    plt.show()

def plotData_KD():
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    import matplotlib.dates as mdates
    import numpy as np
    plt.figure(figsize=(8,5), dpi=200)
    mpl.rcParams['grid.color'] = 'k'
    mpl.rcParams['grid.linestyle'] = ':'
    mpl.rcParams['grid.linewidth'] = 0.5
    ax1_t = plt.subplot2grid((7,8),(0,0),colspan=8,rowspan=3)
    #sns.set(style="whitegrid")
    ax1 = ax1_t.twinx()
    #ax1_t.vlines(time_list,[0],vol_list,facecolor='#0079a3')
    ax1_t.fill_between([i[0] for i in OHLCV],0,[i[5] for i in OHLCV], facecolor='#0079a3', alpha=0.4)
    # ax1.plot(I080.time_list,I080.SumupAvePrice_list,lw=0.8,color='grey')
    # ax1.plot(I080.time_list,I080.SumdownAvePrice_list,lw=0.8,color='grey')
    ax1.plot(time_list,price_list,'black',lw=0.5)
    #ax1.plot(I020.time_list[Time_index:],I020.close_5maList[Time_index:],lw=0.8,color='blue')
    ax1.plot(list(MA10_dict.keys()),list(MA10_dict.values()),lw=0.8,color='green')
    ax1.plot(list(MA20_dict.keys()),list(MA20_dict.values()),lw=0.8,color='red')

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    #ax1.axes.get_xaxis().set_visible(False)         #關閉上圖X座標軸的label
    # ax1.set_xlim([time_list[0],I020.stoptime])
    mpl.rcParams['grid.linestyle'] = ':'
    ax1.grid(True)
    font = {'family': 'serif', 'color':  'darkred', 'weight': 'normal', 'size': 16,}
    plotTime1 = datetime.datetime.strptime('2020/1/10 8:45', '%Y/%m/%d %H:%M')
    titleTime = plotTime1.strftime('%Y/%m/%d')
    ax1.set_title(titleTime, fontdict=font)

    ax2 = plt.subplot2grid((7, 8), (3, 0), colspan=8)
    ax2.plot(list(KD9_dict.keys()), [i[0] for i in KD9_dict.values()],lw=0.8,color='red')
    ax2.plot(list(KD9_dict.keys()), [i[1] for i in KD9_dict.values()],lw=0.8,color='green')
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax2.yaxis.set_ticks(np.array([20,50,80]))
    # ax2.set_xlim([I020.starttime,I020.stoptime])
    ax2.grid(True)

    # ax3 = plt.subplot2grid((7, 8), (4, 0), colspan=8)
    # ax3.plot(I020.time_list[Time_index:],I020.bRatio_list,lw=0.8,color='red')
    # ax3.plot(I020.time_list[Time_index:],I020.sRatio_list,lw=0.8,color='green')
    # ax3.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    # ax3.set_xlim([I020.starttime,I020.stoptime])
    # ax3.grid(True)
    #
    # ax4 = plt.subplot2grid((7, 8), (5, 0), colspan=8)
    # ax4.plot(I030.time_list,I030.b3Ratio_list,lw=0.8,color='red')
    # ax4.plot(I030.time_list,I030.s3Ratio_list,lw=0.8,color='green')
    # ax4.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    # ax4.set_xlim([I030.starttime,I030.stoptime])
    # ax4.grid(True)
    #
    # ax5 = plt.subplot2grid((7, 8), (6, 0), colspan=8)
    # ax5.plot(I080.time_list,I080.SumallupVolume_list,lw=0.8,color='red')
    # ax5.plot(I080.time_list,I080.SumalldownVolume_list,lw=0.8,color='green')
    # ax5.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    # ax5.set_xlim([I080.starttime,I080.stoptime])
    # ax5.grid(True)

    # print(Date[k]+'-'+dataType[k]+'  計算時間一共：',datetime.datetime.now() - start)
    # plt.savefig('TXFpic/'+Date[k]+dataType[k]+'.png')
    # plt.close()
    plt.show()

# plotData1()
plotData_KD()