import requests
import pandas as pd
import re
import datetime

def compute_rsi(dataframe, period=14):
    """
    RSI를 계산하는 함수입니다.
    Calculates the RSI.

    Parameters:
        dataframe (pandas.DataFrame): 가격 데이터프레임입니다.
                                      Price DataFrame.
        period (int): RSI 계산 기간입니다.
                      Period for RSI calculation.

    Returns:
        pandas.Series: RSI 값이 담긴 시리즈입니다.
                       Series containing RSI values.
    """
    delta = dataframe['closePrice'].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # 지수 이동 평균(EMA) 사용으로 RSI 계산 최적화
    # Use Exponential Moving Average (EMA) for smoother RSI
    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def compute_moving_average(dataframe, window_size):
    """
    N일 이동평균선을 계산하는 함수입니다.
    Calculates the N-day Moving Average.

    Parameters:
        dataframe (pandas.DataFrame): 가격 데이터프레임입니다.
                                      Price DataFrame.
        window_size (int): 이동평균 기간(n일)입니다.
                           The window size for moving average.

    Returns:
        pandas.Series: 이동평균 값이 담긴 시리즈입니다.
                       Series containing moving average values.
    """
    # 단순 이동평균(SMA) 계산
    # Calculate Simple Moving Average (SMA)
    moving_avg = dataframe['closePrice'].rolling(window=window_size, min_periods=1).mean()
    return moving_avg
