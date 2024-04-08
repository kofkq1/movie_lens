#점수분포 보여주는 기능
import make_csv_wordcloud
from collections import Counter


import matplotlib.pyplot as plt

ratings = [d['rating'] for d in make_csv_wordcloud.comments]

# 'rating'의 값을 세고, 결과를 사전 형태로 반환합니다.
count = Counter(ratings)
print(count)
# 바 차트를 생성합니다.
#레이블 한글로
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False
plt.bar(count.keys(), count.values())

#레이블 한글로
# xticks method에 x좌표가 담긴 list를 전달해주면 전달한 list에 있는 값대로 x축이 표시됩니다

# x축에 레이블을 추가합니다.
plt.xlabel('평점')

# y축에 레이블을 추가합니다.
# frequency를 가로로 출력하기위해서
plt.text(-0.05, 0.5, '빈도수', rotation=0, va='center', ha='right', transform=plt.gca().transAxes)

# 차트에 제목을 추가합니다.
plt.title('평점 분포')

# xticks method에 x좌표가 담긴 list를 전달해주면 전달한 list에 있는 값대로 x축이 표시됩니다
plt.xticks([1,2,3,4,5,6,7,8,9,10])
# 저장하고
plt.savefig('plot.png')

# 생성된 그래프를 화면에 출력하고, 내부적으로 그래프를 생성하기 위해 사용했던 메모리를 정리(clear)하는 역할

plt.show()
