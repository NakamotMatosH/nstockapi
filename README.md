
# Custom Stock Analysis Project

## 프로젝트 개요
이 프로젝트는 사용자 맞춤형 주식 분석과 트레이딩 전략 검증을 위해 설계되었습니다. 주식 데이터를 외부 API에서 수집하고, 이를 기반으로 다양한 분석 및 실시간 메시지 알림을 제공합니다.

---

## 주요 모듈 및 함수 설명

### 1. `import_sqlite3.py`
SQLite 데이터베이스 초기화 및 기본 데이터 관리 모듈입니다.

### 2. `loadstockdata` (주식 데이터 로드 및 연산 모듈)
#### 주요 파일 설명
- **`compute.py`**
  - `compute_rsi(dataframe, price_column='closePrice', period=14)`: **RSI(상대강도지수) 계산 함수**  
    입력된 데이터프레임에서 특정 열을 기준으로 RSI 값을 계산합니다.  
  - `compute_moving_average(dataframe, price_column='closePrice', period=20)`: **이동 평균 계산 함수**  
    주식 가격의 이동 평균을 계산합니다.

- **`prices.py`**
  - `retrieve_stock_data(symbol, start_date=None, end_date=None)`: **네이버 API를 이용해 주식 데이터 가져오기**  
    특정 주식의 데이터를 네이버 API에서 수집하며, 실패 시 최대 3번까지 재시도합니다.  
  - `save_to_database(data, table_name)`: **수집된 데이터를 SQLite 데이터베이스에 저장**  

---

### 3. `messageSVC` (실시간 메시지 서비스)
텔레그램 API를 사용해 특정 이벤트 발생 시 사용자에게 알림 메시지를 보냅니다.  
#### 주요 파일 설명
- **`telegram.py`**
  - `send_message_telegram(token, chat_id, text)`: **텔레그램 메시지 전송 함수**  
    - **Parameters**  
      - `token`: 텔레그램 봇 토큰  
      - `chat_id`: 메시지를 보낼 채널 또는 사용자 ID  
      - `text`: 전송할 메시지 내용  

---

### 4. `tradingmodel` (트레이딩 전략 테스트)
트레이딩 전략을 설계하고 과거 데이터를 기반으로 시뮬레이션합니다.  
- `idea.txt`: 새로운 전략 아이디어 기록  
- `todo.txt`: 향후 추가할 기능 목록  

---

## 향후 개선 및 추가할 기능

### 1. 데이터 수집 및 확장
- **다양한 데이터 소스 통합**: Yahoo Finance, Alpha Vantage, Quandl 등의 데이터 소스 통합  
- **암호화폐 및 원자재 데이터 추가**: 비트코인, 이더리움, 원유, 금 데이터 추가  
- **실시간 데이터 스트리밍 기능**: WebSocket을 이용한 실시간 가격 변동 수집  

### 2. 트레이딩 모델 개선
- **머신러닝 기반 전략**: Scikit-learn과 TensorFlow를 이용해 예측 모델 구축  
  - LSTM 시계열 예측  
  - 랜덤 포레스트 및 XGBoost 기반 예측 모델  
- **전략 백테스팅 시스템 구축**: 성능 지표 자동 계산 및 시뮬레이션 기능 추가  

### 3. 사용자 인터페이스 강화
- **웹 기반 대시보드**: Flask 또는 Streamlit을 이용한 실시간 데이터 시각화  
- **보고서 자동 생성 기능**: PDF로 주간/월간 거래 요약 보고서 생성  

### 4. 알림 시스템 확장
- **SMS, 이메일, 슬랙 알림 추가**  
- **조건부 알림 설정** (예: RSI가 30 이하일 때 알림)  

### 5. 최적화 및 자동화
- **데이터베이스 최적화**: PostgreSQL로 전환 고려  
- **트레이딩 자동화**: 조건 충족 시 매수/매도 주문 자동 실행  

---

## 설치 및 실행 방법
1. Python 3.x 설치  
2. 필수 패키지 설치 (`pandas`, `requests`, `sqlite3` 등)  
3. `import_sqlite3.py` 실행으로 데이터베이스 초기화  
   ```bash
   python import_sqlite3.py
   ```

---

## 사용 예제
```python
from loadstockdata.compute import compute_rsi
import pandas as pd

# 예제 데이터 생성
data = {'closePrice': [100, 102, 101, 105, 107, 110, 108, 109, 112, 115]}
df = pd.DataFrame(data)

# RSI 계산
rsi = compute_rsi(df)
print(rsi)
```

---

## 향후 개선 사항
- **시각화 기능 추가**: Matplotlib을 이용한 주식 데이터 시각화  
- **추가 트레이딩 모델 구현**: 머신러닝 기반 모델 추가  
- **다양한 알림 채널 확장**  

---
