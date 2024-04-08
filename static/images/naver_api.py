import os
import sys
import urllib.request
import json

client_id = "l8XfKFIRldZyQp_IfHja"
client_secret = "7A2VMQtKAj"
encText = urllib.parse.quote(input())
url = "https://openapi.naver.com/v1/search/image?query=" + encText

request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

# User-Agent 추가
request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

response = urllib.request.urlopen(request)

response = urllib.request.urlopen(request)
rescode = response.getcode()

# 이미지 저장 경로
# 이미지 저장 경로
savePath = "./review_ai_analysis/static/images/movies/actors"  # 현재 디렉토리 내의 images 폴더 사용

# 폴더가 없으면 생성
if not os.path.exists(savePath):
    os.makedirs(savePath)

if(rescode==200):
    response_body = response.read()
    result = json.loads(response_body)
    img_list = result['items']

    for i, img_list in enumerate(img_list, 1):
        
        # 이미지링크 확인
        print(img_list['link'])

        # 저장 파일명 및 경로
        FileName = os.path.join(savePath, f"image{i}.jpg")
        
        # 파일명 출력 
        print('full name : {}'.format(FileName))
        
        # 이미지 다운로드 URL 요청
        urllib.request.urlretrieve(img_list['link'], FileName)

    # 다운로드 완료 시 출력
    print("--------download succeeded--------")

else:
    print("Error Code:" + rescode)