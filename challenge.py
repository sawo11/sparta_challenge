# 기본 라이브러리 불러오기
import pandas as pd
import requests

# API 요청
url = 'http://api.gwangju.go.kr/xml/stationInfo'
params ={'serviceKey' : '서비스키' }
response = requests.get(url, params=params)

# XML 데이터 파싱
root = ET.fromstring(response.text)

# 데이터 저장용 딕셔너리 초기화
row_dict = {
    'BUSSTOP_ID': [], 'BUSSTOP_NAME': [], 'NAME_E': [],
    'LONGITUDE': [], 'LATITUDE': [], 'ARS_ID': [], 'NEXT_BUSSTOP': []
}

#  XML 데이터 순회 및 데이터 추출
for station in root.findall('.//STATION_LIST/STATION'):
    for child in station:
        if child.tag in row_dict:  # 딕셔너리에 있는 태그만 처리
            row_dict[child.tag].append(child.text)
    
    # 누락된 데이터 처리
    for key in row_dict:
        if len(row_dict[key]) < len(row_dict['BUSSTOP_ID']):  # 가장 긴 리스트에 맞춰 길이 보정
            row_dict[key].append(None)

# DataFrame 생성
df = pd.DataFrame(row_dict)

# 결과 확인
df.head()
