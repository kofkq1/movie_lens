# concat실행후 중복되는 데이터 제거-일주일에 한번씩 업데이트 되다보니 중복되는 데이터가 생김
import pandas as pd

# CSV 파일을 데이터프레임으로 읽기
df = pd.read_csv('data/movieDataSet.csv')

# 'title' 열에 중복된 값이 있는 행을 제거 (첫 번째 발생을 제외하고 모든 중복 제거)
df_unique = df.drop_duplicates(subset='title', keep='first')

# 결과를 확인


# 필요하다면 정제된 데이터프레임을 새로운 CSV 파일로 저장
df_unique.to_csv('data/movieDataSet.csv', index=False)