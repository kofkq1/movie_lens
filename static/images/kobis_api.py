import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import re

# 유효하지 않은 파일/폴더 이름 문자 제거 또는 대체 함수
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)  # 유효하지 않은 문자를 제거

# 영화 상세 정보 조회 함수
def get_movie_info(api_key, movie_id):
    url = f"https://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieInfo.xml?key={api_key}&movieCd={movie_id}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

    # 영화 기본 정보 추출
    movie_info = {
        'movieCd': movie_id,
        'title': sanitize_filename(soup.find('movieNm').text),
        'release_date': soup.find('openDt').text,
        'director': sanitize_filename(soup.find('director').find('peopleNm').text) if soup.find('director') else 'Unknown',
        'actors': ", ".join([sanitize_filename(actor.find('peopleNm').text) for actor in soup.find_all('actor')[:10]]),
        'audiAcc': soup.find('audiAcc').text if soup.find('audiAcc') else '0'  # 누적관객수 추가
    }

    return movie_info

# 주간 박스오피스 정보 조회 함수 수정
def fetch_weekly_box_office(api_key, target_date):
    url = f"http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchWeeklyBoxOfficeList.xml?key={api_key}&targetDt={target_date}&weekGb=0"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')

    movies = []
    for item in soup.find_all('weeklyBoxOffice'):
        movie_id = item.find('movieCd').text
        movie_info = get_movie_info(api_key, movie_id)
        # 누적 관객수(audiAcc) 추가
        movie_info['audiAcc'] = item.find('audiAcc').text if item.find('audiAcc') else '0'
        movies.append(movie_info)

    return movies

# API 키와 대상 날짜 설정, 주간 박스오피스는 보통 일요일을 기준으로 조회
api_key = '2d27705d955e1888ad6d1a54594f3560&'
last_sunday = datetime.now() - timedelta(days=datetime.now().weekday() + 1)  # 가장 최근의 일요일 계산
target_date = last_sunday.strftime("%Y%m%d")

# 영화 정보 가져오기
movies = fetch_weekly_box_office(api_key, target_date)

# CSV 파일로 저장
csv_file_path = './weekly_box_office_details.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as file:
    fieldnames = ['movieCd', 'title', 'release_date', 'director', 'actors', 'audiAcc']  # 필드명 설정
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    for movie in movies:
        writer.writerow(movie)

print(f"Data saved to {csv_file_path}")
