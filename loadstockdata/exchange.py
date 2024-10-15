import requests
import json
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import yfinance as yf

def fetch_usd_to_krw_data():
    """
    네이버 API에서 지난 3개월간의 USD to KRW 환율 데이터를 가져옵니다.
    Fetches USD to KRW exchange rate data for the past 3 months from Naver API.

    Returns:
        dict: 환율 데이터가 포함된 JSON 응답.
              JSON response containing exchange rate data.
    """
    url = 'https://m.stock.naver.com/front-api/chart/pricesByPeriod'
    params = {
        'reutersCode': 'FX_USDKRW',
        'category': 'exchange',
        'chartInfoType': 'marketindex',
        'scriptChartType': 'areaMonthThree'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return json.loads(response.content)

def create_exchange_rate_dataframe(data):
    """
    가져온 환율 데이터로부터 데이터프레임을 생성하고 누락된 날짜를 채웁니다.
    Creates a DataFrame from the fetched exchange rate data and fills missing dates.

    Parameters:
        data (dict): 환율 정보를 포함한 JSON 데이터.
                     JSON data containing exchange rate information.

    Returns:
        pd.DataFrame: 스무딩된 환율 데이터가 포함된 데이터프레임.
                      DataFrame containing smoothed exchange rate data.
    """
    # 관련 데이터 추출
    # Extract relevant data
    price_infos = data['result']['priceInfos']
    
    # 데이터프레임으로 변환
    # Convert to DataFrame
    df = pd.DataFrame(price_infos)
    df['localDate'] = pd.to_datetime(df['localDate'], format='%Y%m%d')
    df.set_index('localDate', inplace=True)
    df = df[['closePrice', 'highPrice', 'lowPrice']]

    # 데이터의 첫 번째 날짜부터 마지막 날짜까지의 전체 날짜 범위 생성
    # Create a complete date range from the first to the last date in the data
    full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(full_date_range)

    # 선형 보간법을 사용하여 누락된 값을 보간
    # Interpolate missing values using linear interpolation
    for column in ['closePrice', 'highPrice', 'lowPrice']:
        # 유효한 인덱스를 찾고 보간 함수 생성
        # Find valid indexes and create an interpolation function
        valid_idx = df[column].dropna().index
        interp_func = interp1d(valid_idx.astype(np.int64), df.loc[valid_idx, column], kind='linear', fill_value='extrapolate')
        
        # 보간을 적용하여 누락된 값 채우기
        # Apply interpolation to fill missing values
        missing_idx = df[column].index[df[column].isna()]
        df.loc[missing_idx, column] = interp_func(missing_idx.astype(np.int64))

    # localDate 컬럼 추가 (YYYYMMDD 형식)
    # Add localDate column with YYYYMMDD format
    df['localDate'] = df.index.strftime('%Y%m%d')

    return df

def combine_exchange_rate_data(start_date, end_date):
    """
    네이버 API와 yfinance에서 가져온 환율 데이터를 결합하고, 조회 기간에 맞춰 데이터를 반환합니다.
    Combines exchange rate data from Naver API and yfinance, then returns the data for the specified date range.

    Parameters:
        start_date (str): 시작 날짜 ('YYYYMMDD' 형식).
                          Start date in 'YYYYMMDD' format.
        end_date (str): 종료 날짜 ('YYYYMMDD' 형식).
                        End date in 'YYYYMMDD' format.

    Returns:
        pd.DataFrame: 결합된 환율 데이터가 포함된 데이터프레임.
                      DataFrame containing combined exchange rate data.
    """
    # 네이버 API 데이터 가져오기
    # Fetch data from Naver API
    data = fetch_usd_to_krw_data()
    naver_df = create_exchange_rate_dataframe(data)
    naver_df.rename(columns={'closePrice': 'Close', 'highPrice': 'High', 'lowPrice': 'Low'}, inplace=True)
    naver_df['Open'] = naver_df['Close']  # Open 값을 Close로 설정
    naver_df = naver_df[['Open', 'High', 'Low', 'Close', 'localDate']]

    # yfinance 데이터 가져오기
    # Fetch data from yfinance
    start_dt = pd.to_datetime(start_date, format='%Y%m%d')
    end_dt = pd.to_datetime(end_date, format='%Y%m%d')
    yf_df = yf.download("USDKRW=X", start=start_dt, end=end_dt)
    yf_df = yf_df[['Open', 'High', 'Low', 'Close']]

    # 날짜 인덱스 설정
    # Set Date as index
    yf_df.index = pd.to_datetime(yf_df.index)
    naver_df.index = pd.to_datetime(naver_df.index)

    # yfinance 데이터와 네이버 데이터 결합
    # Combine yfinance and Naver data
    combined_df = pd.concat([yf_df, naver_df]).sort_index()

    # 중복된 날짜가 있을 경우 네이버 데이터를 우선 사용
    # Prioritize Naver data in case of overlapping dates
    combined_df = combined_df[~combined_df.index.duplicated(keep='last')]

    # 누락된 값 보간 (선형 보간법 사용)
    # Interpolate missing values using linear interpolation
    combined_df = combined_df.interpolate(method='linear')

    # 조회 기간에 맞게 필터링
    # Filter by the specified date range
    combined_df = combined_df[(combined_df.index >= start_dt) & (combined_df.index <= end_dt)]

    # localDate 컬럼 추가 (YYYYMMDD 형식)
    # Add localDate column with YYYYMMDD format
    combined_df['localDate'] = combined_df.index.strftime('%Y%m%d')

    return combined_df

# 예시 사용법
# Example usage
#start_date = "20231014"
#end_date = "20241015"
#df_combined_exchange_rate = combine_exchange_rate_data(start_date, end_date)
#df_combined_exchange_rate
