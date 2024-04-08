import csv
import requests
from urllib.parse import quote

# KMDB API 키
kmdb_api_key = 'ZW29B6OV5T03ILGT7509'  # 실제 API 키로 교체해야 함

def get_movie_info_kmdb(movie_title):
    # 영화 제목을 URL 인코딩
    encoded_title = quote(movie_title)
    
    # KMDB API URL
    url = f"http://api.koreafilm.or.kr/openapi-data2/wisenut/search_api/search_json2.jsp?collection=kmdb_new2&detail=Y&title={encoded_title}&ServiceKey={kmdb_api_key}"
    
    # API 요청
    response = requests.get(url)
    data = response.json()
    
    # 영화 정보 초기화
    genre = keyword = summary = "정보 없음"
    
    # 응답 데이터에서 영화 정보 추출
    if data['TotalCount'] > 0 and data['Data']:
        first_result = data['Data'][0]['Result'][0]
        genre = first_result.get('genre', '정보 없음')
        keyword = first_result.get('keywords', '정보 없음')
        plot_list = first_result.get('plots', {}).get('plot', [])
        summary = plot_list[0]['plotText'] if plot_list else "정보 없음"
    
    return genre, keyword, summary

# CSV 파일 경로
input_file_path = './weekly_box_office_details.csv'  # 입력 파일 경로
output_file_path = './updated_weekly_box_office_details.csv'  # 출력 파일 경로

# CSV 파일 읽기 및 쓰기
with open(input_file_path, mode='r', newline='', encoding='utf-8') as infile, open(output_file_path, mode='w', newline='', encoding='utf-8') as outfile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames + ['genres', 'keyword', 'summary']  # 새로운 필드 추가
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    
    for row in reader:
        # 영화 제목으로 정보 조회
        genre, keyword, summary = get_movie_info_kmdb(row['title'])
        # 조회한 정보를 행에 추가
        row.update({'genres': genre, 'keyword': keyword, 'summary': summary})
        writer.writerow(row)

print("CSV 파일 업데이트 완료!")
