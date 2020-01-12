import datetime as dt
import numpy as np


class tickPreproc:
    def __init__(self, time, Tint=60):
        self.Tint = Tint
        def timerange(time1, time2, int):
            delta = dt.timedelta(seconds=int)
            curr = time1
            while curr < time2:
                yield curr
                curr += delta
            return curr

        self.OHLCVoutput = [[0]]
        self.start_T = time.replace(hour=0, minute=0, second=0, microsecond=0) - dt.timedelta(days=1)
        end_T = self.start_T + dt.timedelta(days=2)
        self._Time = timerange(self.start_T, end_T, self.Tint)  # 疊代元素

    def toOHLCV(self, time, data, vol=0):
        if self.OHLCVoutput[0] == [0]:
            self.OHLCVTime_flag = self.start_T
            self._OHLCV_Time = self._Time
            self.OHLCVoutput_tmp = []  # OHLCV暫存list
        while time - dt.timedelta(seconds=self.Tint) > self.OHLCVTime_flag:
            self.OHLCVTime_flag = next(self._OHLCV_Time)

            if len(self.OHLCVoutput_tmp) != 0 and self.OHLCVoutput_tmp[2] != -99999: self.OHLCVoutput += [0]

            self.OHLCVoutput_tmp = [self.OHLCVTime_flag, data, -99999, 99999, data, 0,time,
                                    time]  ###[Time_flag,O,H,L,C,V,openTime,closeTime]
            continue
        self.OHLCVoutput_tmp[2] = max(self.OHLCVoutput_tmp[2], data)  # High
        self.OHLCVoutput_tmp[3] = min(self.OHLCVoutput_tmp[3], data)  # Low
        self.OHLCVoutput_tmp[4] = data  # Close
        self.OHLCVoutput_tmp[5] += vol  # Volume
        self.OHLCVoutput_tmp[7] = time  # close time

        self.OHLCVoutput[-1] = self.OHLCVoutput_tmp
        return self.OHLCVoutput

def getKD(lenkd,data,KD):
    '''
    :param data: data = [[time_flag, OHLC],[time_flag, OHLC],....]
    :param lenma:
    :return: KD = {time_flag: [K,D,RSV]}
    '''
    if len(data) < lenkd:
        return {data[-1][0]:[KD[0],KD[1],KD[2]]}
    else:
        low_list = [i[3] for i in data[-lenkd:]]
        high_list = [i[2] for i in data[-lenkd:]]
        # print(data[-1][4], min(low_list), max(high_list), min(low_list))
        RSV = (data[-1][4] - min(low_list)) / (max(high_list) - min(low_list)) * 100.
        # RSV =  (第n天收盤價 - 最近n天內最低價)/(最近n天內最高價 - 最近n天內最低價) * 100.

        K = 2 / 3. * KD[0] + 1 / 3. * RSV     # 當日K值(%K)= 2/3 前一日 K值 + 1/3 RSV
        D = 2 / 3. * KD[1] + 1 / 3. * K       # 當日D值(%D)= 2/3 前一日 D值 + 1/3 當日K值
        return {data[-1][0]: [K, D, RSV]}

def getMA(data, lenma=5):
    '''
    :param data: data = [[time_flag, price],[time_flag, price],....]
    :param lenma:
    :return: MA = {time_flag: MA}
    '''

    if len(data) < lenma:
        return {data[-1][0]: np.nan}
    else:
        MA_list = [i[1] for i in data[-lenma:]]
        return {data[-1][0]: sum(MA_list)/lenma}



