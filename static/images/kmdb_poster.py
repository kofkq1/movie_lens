import requests
from urllib.parse import quote
import os
# 사용안하는 파일
url = 'https://ncache.ilbe.com/files/attach/new/20201013/377678/11207239912/11294630674/13056e962a2e68ed45f89301575eae0f_11294630731.jpeg'
response = requests.get(url, verify=False)

# KMDB API 키 설정
kmdb_api_key = 'ZW29B6OV5T03ILGT7509'

def get_movie_details(movie_title):
    # 영화 제목을 URL 인코딩
    encoded_title = quote(movie_title)
    
    # KMDB에서 영화 제목으로 검색
    search_url = f"http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json.jsp?collection=kmdb_new2&detail=N&title={encoded_title}&ServiceKey={kmdb_api_key}"
    
    # 검색 API 요청
    search_response = requests.get(search_url)
    search_data = search_response.json()
    
    if search_data.get('Data') and search_data['Data'][0].get('Result'):
        first_result = search_data['Data'][0]['Result'][0]
        movie_id = first_result.get('movieId')
        movie_seq = first_result.get('movieSeq')
        
        # 상세 정보 조회 URL 구성
        detail_url = f"http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json.jsp?collection=kmdb_new2&detail=Y&movieId={movie_id}&movieSeq={movie_seq}&ServiceKey={kmdb_api_key}"
        
        # 상세 정보 API 요청
        detail_response = requests.get(detail_url)
        detail_data = detail_response.json()
        
        if detail_data.get('Data') and detail_data['Data'][0].get('Result'):
            detail_first_result = detail_data['Data'][0]['Result'][0]
            posters = detail_first_result.get('posters', '').split('|')[0]  # 포스터 URL 추출
            return posters
    return None

def download_image(url, save_path):
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image saved to {save_path}")
        else:
            print(f"Failed to download image from {url}")
    else:
        print("No image URL provided")

# 영화 제목 지정
movie_title = "파묘"

# 포스터 URL 가져오기
poster_url = get_movie_details(movie_title)

# 포스터 이미지 저장 경로 설정
image_save_path = './movie_posters'
save_path = os.path.join(image_save_path, movie_title.replace(" ", "_") + '_poster.jpg')

# 포스터 이미지 다운로드
if poster_url:
    download_image(poster_url, save_path)
else:
    print(f"Poster URL not found for '{movie_title}'.")
