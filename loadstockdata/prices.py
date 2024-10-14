import requests
import pandas as pd
import re
import datetime
from .compute import *
from .config import HEADERS  # 설정 파일에서 헤더 정보를 가져옵니다.
from tenacity import retry, stop_after_attempt, wait_fixed  # 재시도 라이브러리


@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def get_stock_data_by_date_range(symbol, start_date, end_date, moving_avg_periods=None):
    """
    네이버 API를 이용하여 종목별, 기간별 데이터를 추출하고 이동평균선을 계산하는 함수입니다.
    Retrieves stock data by symbol and date range using Naver API and calculates moving averages.

    Parameters:
        symbol (str): 종목 코드입니다. 국내 종목은 숫자 6자리, 해외 종목은 네이버 기준 티커를 사용합니다.
                      Stock symbol. Use 6-digit number for domestic stocks, Naver-style ticker for foreign stocks.
        start_date (str): 시작 날짜입니다. 형식은 'YYYYMMDD'입니다.
                          Start date in 'YYYYMMDD' format.
        end_date (str): 종료 날짜입니다. 형식은 'YYYYMMDD'입니다.
                        End date in 'YYYYMMDD' format.
        moving_avg_periods (list, optional): 이동평균선을 계산할 기간의 리스트입니다. 예: [30, 60, 120]
                                             List of periods for moving averages. e.g., [30, 60, 120]

    Returns:
        pandas.DataFrame: 종목의 기간별 데이터와 이동평균선이 담긴 데이터프레임입니다.
                          DataFrame containing stock data and moving averages for the specified period.

    Raises:
        Exception: 통신 오류나 데이터 파싱 오류가 발생한 경우 예외를 발생시킵니다.
                   Raises an exception if a communication error or data parsing error occurs.
    """
    dataframe = retrieve_stock_data(symbol, start_date, end_date)
    dataframe['RSI14'] = compute_rsi(dataframe)

    # 이동평균선 계산 및 컬럼 추가
    # Calculate moving averages and add columns
    if moving_avg_periods:
        for period in moving_avg_periods:
            dataframe[f'MA{period}'] = compute_moving_average(dataframe, period)

    return dataframe

def get_recent_stock_data(symbol, num_days, moving_avg_periods=None):
    """
    최근 N일 동안의 데이터를 추출하고 이동평균선을 계산하는 함수입니다.
    Retrieves stock data for the last N business days and calculates moving averages.

    Parameters:
        symbol (str): 종목 코드입니다. 국내 종목은 숫자 6자리, 해외 종목은 네이버 기준 티커를 사용합니다.
                      Stock symbol. Use 6-digit number for domestic stocks, Naver-style ticker for foreign stocks.
        num_days (int): 최근 가져올 영업일의 수입니다.
                        Number of recent business days to retrieve.
        moving_avg_periods (list, optional): 이동평균선을 계산할 기간의 리스트입니다. 예: [30, 60, 120]
                                             List of periods for moving averages. e.g., [30, 60, 120]

    Returns:
        pandas.DataFrame: 종목의 최근 N일 데이터와 이동평균선이 담긴 데이터프레임입니다.
                          DataFrame containing stock data and moving averages for the last N business days.

    Raises:
        Exception: 통신 오류나 데이터 파싱 오류가 발생한 경우 예외를 발생시킵니다.
                   Raises an exception if a communication error or data parsing error occurs.
    """
    # 오늘 날짜와 필요한 기간 계산
    # Calculate today's date and required period
    today = datetime.date.today()
    past_date = today - datetime.timedelta(days=num_days * 2)  # 여유를 두고 두 배의 기간을 가져옴
    start_date = past_date.strftime("%Y%m%d")
    end_date = today.strftime("%Y%m%d")

    dataframe = retrieve_stock_data(symbol, start_date, end_date)

    # 최근 영업일 기준으로 데이터 슬라이싱
    # Slice data based on recent business days
    dataframe = dataframe.tail(num_days).reset_index(drop=True)
    dataframe['RSI14'] = compute_rsi(dataframe)

    # 이동평균선 계산 및 컬럼 추가
    # Calculate moving averages and add columns
    if moving_avg_periods:
        for period in moving_avg_periods:
            dataframe[f'MA{period}'] = compute_moving_average(dataframe, period)

    return dataframe
