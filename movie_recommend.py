from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

import pandas as pd
# 데이터 파일 위치 확인 static/images
df = pd.read_csv('./data/movieDataSet.csv')

tf_idf = TfidfVectorizer()
# 결측값을 빈 값으로 대체
df['summary'] = df['summary'].fillna('')
tf_idf_matrix = tf_idf.fit_transform(df['summary'])

cosine_sim = linear_kernel(tf_idf_matrix, tf_idf_matrix)
# 맵핑(mapping)
indices = pd.Series(df.index, index=df['movieCd']).drop_duplicates()

# movieCode
# 171883        0
# 169581        1
# 155665        2
# 165461        3
# 158256        4


#
# # # 영화제목 입력하면 그걸 인덱스 몇번째인지 확인해서 그걸토대로 작동  대신 title을 넣어 검색할 수 있게 수정
# # #
def get_recommendations(index, size, cosine_sim=cosine_sim):
    # movieCode 대신 title을 넣어 검색할 수 있게 수정
    if index not in indices:
        return ['해당 영화가 없습니다']
    # 입력된 무비코드를 기반으로 인덱스를 가져옵니다
    idx = indices[index]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # 당연히 가장 유사한 건 자기 자신이기 때문에 0번 배열은 제외하고 1번 배열부터
    sim_scores = sim_scores[1:size+1]
    movie_indices = [i[0] for i in sim_scores]
    # score = [i[1] for i in sim_scores]
    # 이는 'movieCode' 열의 특정 행들만을 선택하여 반환합니다
    return df['title'].iloc[movie_indices]

# 지금은 무비코드가 아닌 인덱스 기반으로 작동되고 있음
# 강철비 인덱스 입력했을 때
# static/images/weekly_box_office_details.csv
reviews = pd.read_csv(f'static/images/weekly_box_office_details.csv')#영화리뷰csv읽기
nextt=list(reviews['movieCd'])
Recommended_movies =[]
#
for i in nextt:
    print(i)
    a=list(get_recommendations(i, 4))
    Recommended_movies.append(a)
# 추천된 영화제목만 가져와서 처리
print(Recommended_movies)
df2 = pd.read_csv('static/images/updated_weekly_box_office_details.csv')

df2['recommend']= Recommended_movies
df2.to_csv('static/images/updated_weekly_box_office_details.csv', index=False,encoding='utf-8-sig')
