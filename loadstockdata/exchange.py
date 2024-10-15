import requests
import json
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

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

    return df

# 데이터를 가져와 데이터프레임을 생성하는 메인 함수
# Main function to fetch data and create DataFrame
def get_usd_to_krw_dataframe():
    try:
        data = fetch_usd_to_krw_data()
        df = create_exchange_rate_dataframe(data)
        return df
    except requests.exceptions.RequestException as e:
        print(f"데이터를 가져오는 중 오류 발생: {e}\nError fetching data: {e}")
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {e}\nError processing data: {e}")

# 예시 사용법
# Example usage
#df_exchange_rate = get_usd_to_krw_dataframe()
#print(df_exchange_rate)
