import requests
import json
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import yfinance as yf

def fetch_gold_data():
    """
    네이버 API에서 지난 3개월간의 금 시세 데이터를 가져옵니다.
    Fetches gold price data for the past 3 months from Naver API.

    Returns:
        dict: 금 시세 데이터가 포함된 JSON 응답.
              JSON response containing gold price data.
    """
    url = 'https://m.stock.naver.com/front-api/chart/pricesByPeriod'
    params = {
        'reutersCode': 'GCcv1',
        'category': 'metals',
        'chartInfoType': 'futures',
        'scriptChartType': 'candleDay'
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return json.loads(response.content)

def create_gold_dataframe(data):
    """
    가져온 금 시세 데이터로부터 데이터프레임을 생성하고 누락된 날짜를 채웁니다.
    Creates a DataFrame from the fetched gold price data and fills missing dates.

    Parameters:
        data (dict): 금 시세 정보를 포함한 JSON 데이터.
                     JSON data containing gold price information.

    Returns:
        pd.DataFrame: 스무딩된 금 시세 데이터가 포함된 데이터프레임.
                      DataFrame containing smoothed gold price data.
    """
    # 관련 데이터 추출
    price_infos = data['result']['priceInfos']
    
    # 데이터프레임으로 변환
    df = pd.DataFrame(price_infos)
    df['localDate'] = pd.to_datetime(df['localDate'], format='%Y%m%d')
    df.set_index('localDate', inplace=True)
    df = df[['closePrice', 'highPrice', 'lowPrice', 'openPrice']]

    # 데이터의 첫 번째 날짜부터 마지막 날짜까지의 전체 날짜 범위 생성
    full_date_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
    df = df.reindex(full_date_range)

    # 선형 보간법을 사용하여 누락된 값을 보간
    for column in ['closePrice', 'highPrice', 'lowPrice', 'openPrice']:
        valid_idx = df[column].dropna().index
        interp_func = interp1d(valid_idx.astype(np.int64) // 10**9, df.loc[valid_idx, column], kind='linear', fill_value='extrapolate')
        missing_idx = df[column].index[df[column].isna()]
        df.loc[missing_idx, column] = interp_func(missing_idx.astype(np.int64) // 10**9)

    # localDate 컬럼 추가 (YYYYMMDD 형식)
    df['localDate'] = df.index.strftime('%Y%m%d')

    return df

def combine_gold_data(start_date, end_date):
    """
    네이버 API와 yfinance에서 가져온 금 시세 데이터를 결합하고, 조회 기간에 맞춰 데이터를 반환합니다.
    Combines gold price data from Naver API and yfinance, then returns the data for the specified date range.

    Parameters:
        start_date (str): 시작 날짜 ('YYYYMMDD' 형식).
                          Start date in 'YYYYMMDD' format.
        end_date (str): 종료 날짜 ('YYYYMMDD' 형식).
                        End date in 'YYYYMMDD' format.

    Returns:
        pd.DataFrame: 결합된 금 시세 데이터가 포함된 데이터프레임.
                      DataFrame containing combined gold price data.
    """
    # 네이버 API 데이터 가져오기
    data = fetch_gold_data()
    naver_df = create_gold_dataframe(data)
    naver_df.rename(columns={'closePrice': 'Close', 'highPrice': 'High', 'lowPrice': 'Low', 'openPrice': 'Open'}, inplace=True)
    naver_df = naver_df[['Open', 'High', 'Low', 'Close', 'localDate']]

    # yfinance 데이터 가져오기
    start_dt = pd.to_datetime(start_date, format='%Y%m%d')
    end_dt = pd.to_datetime(end_date, format='%Y%m%d')
    yf_df = yf.download("GC=F", start=start_dt, end=end_dt)
    yf_df = yf_df[['Open', 'High', 'Low', 'Close']]

    # 날짜 인덱스 설정 (tz-naive로 변환)
    yf_df.index = pd.to_datetime(yf_df.index).tz_localize(None)
    naver_df.index = pd.to_datetime(naver_df.index).tz_localize(None)

    # yfinance 데이터와 네이버 데이터 결합
    combined_df = pd.concat([yf_df, naver_df]).sort_index()

    # 중복된 날짜가 있을 경우 네이버 데이터를 우선 사용
    combined_df = combined_df[~combined_df.index.duplicated(keep='last')]

    # 누락된 값 보간 (선형 보간법 사용)
    combined_df = combined_df.infer_objects(copy=False)  # 객체 타입을 적절한 타입으로 변환
    combined_df = combined_df.interpolate(method='linear', axis=0)  # 보간 실행

    # 조회 기간에 맞게 필터링
    combined_df = combined_df[(combined_df.index >= start_dt) & (combined_df.index <= end_dt)]

    # localDate 컬럼 추가 (YYYYMMDD 형식)
    combined_df['localDate'] = combined_df.index.strftime('%Y%m%d')

    return combined_df

# 사용 예시
if __name__ == "__main__":
    start_date = '20240101'
    end_date = '20241001'
    gold_data = combine_gold_data(start_date, end_date)
    print(gold_data)
