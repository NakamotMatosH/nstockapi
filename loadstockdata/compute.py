import requests
import pandas as pd
import re
import datetime



def compute_rsi(dataframe, price_column='closePrice', period=14):
    """
    RSI를 계산하는 함수입니다.
    Calculates the RSI.

    Parameters:
        dataframe (pandas.DataFrame): 가격 데이터프레임입니다.
                                      Price DataFrame.
        price_column (str): 가격 열 이름입니다.
                            The column name for price data.
        period (int): RSI 계산 기간입니다.
                      Period for RSI calculation.

    Returns:
        pandas.Series: RSI 값이 담긴 시리즈입니다.
                       Series containing RSI values.
    """
    delta = dataframe[price_column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.ewm(com=period - 1, min_periods=period).mean()
    avg_loss = loss.ewm(com=period - 1, min_periods=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def compute_moving_average(dataframe, price_column='closePrice', window_size=30):
    """
    N일 이동평균선을 계산하는 함수입니다.
    Calculates the N-day Moving Average.

    Parameters:
        dataframe (pandas.DataFrame): 가격 데이터프레임입니다.
                                      Price DataFrame.
        price_column (str): 가격 열 이름입니다.
                            The column name for price data.
        window_size (int): 이동평균 기간(n일)입니다.
                           The window size for moving average.

    Returns:
        pandas.Series: 이동평균 값이 담긴 시리즈입니다.
                       Series containing moving average values.
    """
    moving_avg = dataframe[price_column].rolling(window=window_size, min_periods=1).mean()
    return moving_avg


def compute_bollinger_bands(dataframe, price_column='closePrice', window_size=20, num_std_dev=2):
    """
    볼린저 밴드를 계산하는 함수입니다.
    Calculates the Bollinger Bands.

    Parameters:
        dataframe (pandas.DataFrame): 가격 데이터프레임입니다.
                                      Price DataFrame.
        price_column (str): 가격 열 이름입니다.
                            The column name for price data.
        window_size (int): 이동평균을 계산할 기간입니다.
                           The window size for the moving average.
        num_std_dev (int): 표준편차의 배수입니다. 보통 2를 사용합니다.
                           The number of standard deviations for the bands.

    Returns:
        pandas.DataFrame: 상단 밴드, 중간 밴드(이동평균), 하단 밴드가 포함된 데이터프레임입니다.
                          DataFrame containing Upper Band, Middle Band (Moving Average), and Lower Band.
    """
    # 중간 밴드(Moving Average) 계산
    middle_band = dataframe[price_column].rolling(window=window_size, min_periods=1).mean()

    # 표준편차(Standard Deviation) 계산
    rolling_std = dataframe[price_column].rolling(window=window_size, min_periods=1).std()

    # 상단 밴드 및 하단 밴드 계산
    upper_band = middle_band + (rolling_std * num_std_dev)
    lower_band = middle_band - (rolling_std * num_std_dev)

    # 결과를 데이터프레임으로 반환
    bollinger_bands = pd.DataFrame({
        'middle_band': middle_band,
        'upper_band': upper_band,
        'lower_band': lower_band
    })

    return bollinger_bands
