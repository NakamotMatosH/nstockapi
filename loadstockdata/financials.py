import requests
import pandas as pd
import json
import re



def fetch_financial_data(item_code):
    """
    특정 종목의 연간 재무요약정보를 가져와 데이터프레임으로 변환하는 함수입니다.
    Fetches annual financial summary information for a specific stock and converts it into a DataFrame.

    Parameters:
        item_code (str): 종목 코드.
                         Stock item code.

    Returns:
        pd.DataFrame: 재무 데이터를 담고 있는 데이터프레임.
                      DataFrame containing financial data.
    
    Note:
        국내 주식과 외국 주식 간에 재무 데이터의 구조가 다를 수 있습니다. 
        예를 들어, 삼성전자(005930)와 테슬라(TSLA.O)의 재무 요약 정보를 비교하면 
        외국 주식의 경우 일부 컬럼이 없거나 이름이 다르게 나타날 수 있습니다. 
        이는 API에서 제공하는 데이터의 차이 때문에 발생하며, 특히 다음과 같은 차이점이 있습니다:
        - 일부 컬럼 (예: 'ROE', '부채비율', 'EPS' 등) 외국 주식의 재무 정보에서 누락될 수 있음.
        - 외국 주식의 경우 '세전순이익', 'EBITDA' 등의 추가적인 항목이 포함될 수 있음.
        따라서, 재무 데이터를 비교하거나 처리할 때 이러한 차이점을 고려해야 합니다.
    """
    # API 호출하여 JSON 데이터 가져오기
    # Fetch JSON data from API
    isKRX=False
    if re.match(r'^\d{6}$', item_code):
        url = f'https://m.stock.naver.com/api/stock/{item_code}/finance/annual'
        isKRX=True
    else:
        url = f'https://api.stock.naver.com/stock/{item_code}/finance/annual'
        isKRX=False


    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # 기간 정보 추출
    # Extract period information
    if isKRX:
        periods = {entry['key']: entry['title'] for entry in data['financeInfo']['trTitleList']}
        financial_rows = data['financeInfo']['rowList']
    else:
        periods = {entry['key']: entry['title'] for entry in data['trTitleList']}
        financial_rows = data['rowList']

    # 재무 데이터 추출
    # Extract financial data


    # 재무 데이터를 딕셔너리로 변환 후 데이터프레임 생성
    # Convert financial data to dictionary and create DataFrame
    financial_data = {}
    for row in financial_rows:
        title = row['title']
        financial_data[title] = {periods[key]: value['value'] for key, value in row['columns'].items()}

    df = pd.DataFrame(financial_data)

    if isKRX:
      return df[::-1]
    else:
      return df


