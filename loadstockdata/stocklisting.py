import requests
import json
import pandas as pd
from .config import HEADERS

def get_nasdaq_list(stock_code=None):
    """
    나스닥 데이터를 가져오는 함수입니다.
    Fetches NASDAQ data.

    Parameters:
        stock_code (str, optional): 종목코드입니다. 지정하면 해당 종목의 데이터만 반환합니다.
                                    If specified, returns data for the given stock code only.

    Returns:
        pandas.DataFrame: 나스닥 데이터프레임입니다.
                          NASDAQ data as a pandas DataFrame.

    Raises:
        Exception: 통신 오류나 데이터 파싱 오류가 발생한 경우 예외를 발생시킵니다.
                   Raises an exception if a communication error or data parsing error occurs.
    """
    # 요청 헤더 설정
    # Set request headers
    headers = HEADERS
    # API 엔드포인트
    # API endpoint
    url = "https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=0&offset=0&download=true"

    try:
        # 요청 보내기
        # Send request
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # HTTP 에러가 발생하면 예외 발생
                                     # Raise exception if HTTP error occurs

        json_data = response.text  # 취득 데이터 JSON 형식 원본
                                   # Raw JSON data
        obj = json.loads(json_data)

        df = pd.DataFrame(obj['data']['rows'])

        if stock_code:
            # 종목코드로 필터링
            # Filter by stock code
            df = df[df['symbol'] == stock_code.upper()]
        return df

    except requests.exceptions.RequestException as e:
        # 통신 오류가 발생한 경우
        # If communication error occurs
        error_message = f"Communication error occurred: {e} (통신 오류가 발생했습니다: {e})"
        raise Exception(error_message)

    except json.JSONDecodeError as e:
        # JSON 파싱 오류가 발생한 경우
        # If JSON parsing error occurs
        error_message = f"Error parsing data: {e} (데이터를 파싱하는 중 오류가 발생했습니다: {e})"
        raise Exception(error_message)
