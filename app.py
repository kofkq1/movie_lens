from flask import Flask, render_template, url_for, render_template_string, request
import urllib.parse
import re
import sqlite3
import pandas as pd
app = Flask(__name__)
# URL 인코딩 필터 정의

@app.route('/')
def home():
    # 여부분에서 일단 csv파일 읽어오기 주간 csv파일 읽어오기 언제 업데이트가 되지??
    df = pd.read_csv('static/images/updated_weekly_box_office_details.csv')
    # 리뷰에서 긍정비율을 표시하면 좋겟다
    # df에서 사용할 수 있는 칼럼이름
    # movieCd,title,release_date,director,actors,genres,summary,audiAcc
    title = list(df['title'])  # 특정 열의 데이터에 접근
    release_date = list(df['release_date'])
    # director = list(df['director'])
    # actors = list(df['actors'])
    genres = list(df['genres'])
    # 관객수
    audiAcc = list(df['audiAcc'])
    percent = []
    for i in range(1,11):
        # static/images/movies/1/1.csv
        df2 = pd.read_csv(f'static/images/movies/{i}/{i}.csv')
        selected_columns = df2[['sentiment_predicted','Review']]
        # selected_columns의 길이는 어떻게 구하지?
        positive_reviews_df = selected_columns[selected_columns['sentiment_predicted'] == 1]
        # 긍정비율
        percent.append(int(100*(round(len(positive_reviews_df)/len(selected_columns),2))))

            # render_template 기능을 사용하면, 프론트로 변수를 전송할 수 잇음
    return render_template('home.html', num=list(range(10)), title=title, release_date=release_date, genres=genres,percent=percent,audiAcc=audiAcc)
@app.route('/<int:post_id>')
def review(post_id):
    post_id= post_id
    # 배우이미지 파일의 개수를 가져와서 반복문으로 뿌려준다면?
    import glob
    folder_path = f"static/images/movies/{post_id}/actors"

    # 이름규칙으로 가져올지
    # 파일속성이 jpg인 파일 가져올지
    file_count = len(glob.glob(folder_path + '/*.jpg'))


    # poster 가져오기

    # 여부분에서 일단 리뷰csv파일 읽어오기
    df = pd.read_csv(f'static/images/movies/{post_id}/{post_id}.csv')
    # 긍정부정리뷰
    selected_columns = df[['sentiment_predicted','Review','category']]
    positive_reviews_df = selected_columns[selected_columns['sentiment_predicted'] == 1]
    negative_reviews_df= selected_columns[selected_columns['sentiment_predicted'] == 0]

    # 해당 행들에서 'Review' 칼럼의 값 선택 후 리스트로 변환
    positive_reviews_list = positive_reviews_df['Review'].tolist()
    negative_reviews_list = negative_reviews_df['Review'].tolist()
    # 카테고리
    # 긍정리뷰에서만 선택
    # story,directing,actor 칼럼에서 리뷰만
    positive_category_story = positive_reviews_df[positive_reviews_df['category'] == 'story']['Review'].tolist()
    positive_category_directing = positive_reviews_df[positive_reviews_df['category'] == 'directing']['Review'].tolist()
    positive_category_actor = positive_reviews_df[positive_reviews_df['category'] == 'actor']['Review'].tolist()
    # 부정리뷰에서만 선택
    # 부정리뷰에서만
    negative_category_story = negative_reviews_df[negative_reviews_df['category'] == 'story']['Review'].tolist()
    negative_category_directing = negative_reviews_df[negative_reviews_df['category'] == 'directing']['Review'].tolist()
    negative_category_actor = negative_reviews_df[negative_reviews_df['category'] == 'actor']['Review'].tolist()

    # 영화정보 가져오기
    df2 = pd.read_csv('static/images/updated_weekly_box_office_details.csv')
    selected_columns = df2[['title','director','actors','genres','summary','recommend']]
    # 인덱스니까 0-9번 우리는 1-10순위영화
    title=(selected_columns['title'].tolist())[post_id-1]
    director=(selected_columns['director'].tolist())[post_id-1]
    actors=(selected_columns['actors'].tolist())[post_id-1]
    genres=(selected_columns['genres'].tolist())[post_id-1]
    summary=(selected_columns['summary'].tolist())[post_id-1]
    recommend=(selected_columns['recommend'])[post_id-1]
    # str을 list로 변환
    actors = [s for s in actors.split(",") if s]
    # index,Review,category,sentiment_predicted
    # 리뷰에서 긍정비율을 표시하면 좋겟다
    # 영화배우사진이 몇장 있는지 확인해야되는데??file_count
    return render_template('review.html',post_id=post_id,positive_reviews_list=positive_reviews_list,negative_reviews_list=negative_reviews_list
                           ,title=title,director=director,actors=actors,genres=genres,summary=summary,file_count=file_count,recommend=recommend
                           ,positive_category_actor=positive_category_actor,positive_category_directing=positive_category_directing,positive_category_story=positive_category_story
                           ,negative_category_actor=negative_category_actor,negative_category_directing=negative_category_directing,negative_category_story=negative_category_story)


#
#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

def url_encode_filter(s):
    return urllib.parse.quote(s)

# 필터를 Flask 앱에 추가
app.jinja_env.filters['url_encode'] = url_encode_filter

# 파일 이름에서 숫자 추출


# URL에 적합하게 영화 제목 변환
def format_movie_title(title):
    return title.replace(' ', '_').lower()

# @app.route('/<movie_name>')
# def movie(movie_name):
#     movie_folder = f'static/images/movies/{movie_name}'
#     cast_info = []
#     actor_image_folder = os.path.join(movie_folder, 'actors')
#     if os.path.exists(actor_image_folder):
#         for actor_image in os.listdir(actor_image_folder):
#             if actor_image.endswith('.jpg'):
#                 actor_name = os.path.splitext(actor_image)[0]
#                 image_url = os.path.join(actor_image_folder, actor_image).replace('\\', '/')
#                 cast_info.append({"name": actor_name, "image_url": image_url})
#
#     # 포스터 및 감독 이미지는 예시로 하나만 처리합니다.
#     # 실제 애플리케이션에서는 필요에 따라 다른 로직을 적용해야 할 수 있습니다.
#     poster_image_url = ""
#     poster_folder = os.path.join(movie_folder, 'poster')
#     if os.listdir(poster_folder):
#         poster_image_url = os.path.join(poster_folder, os.listdir(poster_folder)[0]).replace('\\', '/')
#
#     return render_template('movie.html', movie_name=movie_name, cast_info=cast_info, poster_image_url=poster_image_url)
