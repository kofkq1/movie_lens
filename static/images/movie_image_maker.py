import csv
import os
import requests
import urllib.parse
import re

# 네이버 Open API 설정
client_id = "l8XfKFIRldZyQp_IfHja"
client_secret = "7A2VMQtKAj"

# CSV 파일 경로
csv_file_path = './updated_weekly_box_office_details.csv'

# 이미지 저장 경로 설정
# 파일 실행위치 기준으로 상대 경로 설정

# image_save_path = '../static/images/movies'
image_save_path = './movies'

# 유효하지 않은 파일/폴더 이름 문자 제거 또는 대체 함수
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', '', filename)  # 유효하지 않은 문자를 제거

# 네이버 이미지 검색 함수
def search_image(query):
    encText = urllib.parse.quote(query)
    url = f"https://openapi.naver.com/v1/search/image?query={encText}&display=1&start=1"
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        res_json = response.json()
        if res_json['items']:
            return res_json['items'][0]['link']
    return None

# 이미지 다운로드 함수
def download_image(url, save_path):
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as img_file:
                img_file.write(response.content)
            return True
    return False

# CSV 파일 읽기 및 이미지 검색 및 다운로드
folder_number = 1  # 영화 폴더 번호 시작
with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # 폴더 번호로 폴더 생성
        movie_folder = os.path.join(image_save_path, str(folder_number))

        # 영화 포스터 이미지 검색 및 다운로드
        poster_folder = os.path.join(movie_folder, 'poster')
        movie_title = sanitize_filename(row['title'])  # 영화 제목은 파일명에만 사용
        poster_url = search_image(f"{movie_title} 포스터")
        download_image(poster_url, os.path.join(poster_folder, f"poster.jpg"))

        # 감독 이미지 검색 및 다운로드
        director_folder = os.path.join(movie_folder, 'director')
        director = sanitize_filename(row['director'].split(", ")[0] if row['director'] else "Unknown")
        director_image_url = search_image(f"{director} 감독")
        download_image(director_image_url, os.path.join(director_folder, f"{folder_number}_director.jpg"))

        # 배우 이미지 검색 및 다운로드
        actor_folder = os.path.join(movie_folder, 'actors')
        actors = row['actors'].split(", ")
        for index, actor in enumerate(actors, start=1):
            actor = sanitize_filename(actor)
            actor_image_url = search_image(f"{actor}")
            if actor_image_url:  # 이미지 URL이 있을 경우만 다운로드 시도
                download_image(actor_image_url, os.path.join(actor_folder, f"{folder_number}_{index}.jpg"))

        print(f"Downloaded images for folder number {folder_number}")
        folder_number += 1  # 다음 영화를 위해 폴더 번호 증가