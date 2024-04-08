# 긍정리뷰에서 많이 나온 단어보여주기

# # 언급된 수 konply로 하거나 SOYNLP

# java home 경로설정 필요 konlpy 사용하려면
import matplotlib.pyplot as plt

from konlpy.tag import Okt
from collections import Counter
import make_csv_wordcloud
#불용어 정하기 영화제목 등
# 긍정리뷰
# precondition: 리뷰가 문자열형태로 전달되어야함
voc = make_csv_wordcloud.positive_reviews
okt_pos = Okt().pos(voc, norm=True)    # 형태소 분석
words = [x for x, y in okt_pos if y in ['Noun']  ]  # 명사만 추출
lst=['영화','관람','우리','부분','진짜']# 불용어 넣어서 사용 ex)영화제목
words=[x for x in words if len(x)>1 ] # 한 글자 이상만
words = [x for x in words if x not in lst ]
count = Counter(words).most_common(10)   # 빈도수 기반
print(count)


#레이블 한글로

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False
# x축에 레이블을 추가합니다.
count=dict((x,y) for x,y in count)
# 바 형태로 제공
plt.bar(count.keys(), count.values())

#레이블 한글로
# x축에 레이블을 추가합니다.
plt.xlabel('순위')

# y축에 레이블을 추가합니다.
# frequency를 가로로 출력하기위해서
plt.text(-0.05, 0.5, '빈도수', rotation=0, va='center', ha='right', transform=plt.gca().transAxes)

# 차트에 제목을 추가합니다.
plt.title('긍정 리뷰에서 자주언급된 단어')
# 저장하고
plt.savefig('positive.png')
# 생성된 그래프를 화면에 출력하고, 내부적으로 그래프를 생성하기 위해 사용했던 메모리를 정리(clear)하는 역할

plt.show()

#
# 부정리뷰에서 많이 나온 단어보여주기


voc = make_csv_wordcloud.negative_reviews
okt_pos = Okt().pos(voc, norm=True)    # 형태소 분석
words = [x for x, y in okt_pos if y in ['Noun']  ]  # 명사만 추출
lst=['영화','관람','우리','부분','진짜']# 불용어 넣어서 사용 ex)영화제목
words=[x for x in words if len(x)>1 ] # 한 글자 이상만
words = [x for x in words if x not in lst ]
count = Counter(words).most_common(10)   # 빈도수 기반
print(count)


#레이블 한글로

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False
# x축에 레이블을 추가합니다.
count=dict((x,y) for x,y in count)
# 바 형태로 제공
plt.bar(count.keys(), count.values())

#레이블 한글로
# x축에 레이블을 추가합니다.
plt.xlabel('순위')

# y축에 레이블을 추가합니다.
# frequency를 가로로 출력하기위해서
plt.text(-0.05, 0.5, '빈도수', rotation=0, va='center', ha='right', transform=plt.gca().transAxes)

# 차트에 제목을 추가합니다.
plt.title('부정 리뷰에서 자주언급된 단어')
# 저장하고
plt.savefig('negative.png')
# 생성된 그래프를 화면에 출력하고, 내부적으로 그래프를 생성하기 위해 사용했던 메모리를 정리(clear)하는 역할

plt.show()


