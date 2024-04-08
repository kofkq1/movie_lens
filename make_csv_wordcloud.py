import os

import pandas as pd
# 매주 업데이트 되는 영화 순위에 올라와 있는 영화제목에 해당하는 영화내용 가져오기
# 리뷰분석
# classification 파일 위치 확인
from classification import ClassificationDeployArguments
args = ClassificationDeployArguments(
    pretrained_model_name="beomi/kcbert-base",#학습시킨 데이터 모델
    #  학습파일저장경로 확인
    downstream_model_dir="./data",
    max_seq_length=128,
)
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained(
    args.pretrained_model_name,
    do_lower_case=False,
)
import torch
fine_tuned_model_ckpt = torch.load(
    args.downstream_model_checkpoint_fpath,
    map_location=torch.device("cpu")
)#체크포인트 불러오기
from transformers import BertConfig
pretrained_model_config = BertConfig.from_pretrained(
    args.pretrained_model_name,
    num_labels=fine_tuned_model_ckpt['state_dict']['model.classifier.bias'].shape.numel(),
)
#어떤걸로 (분류 단어생성) bert사용할 지
from transformers import BertForSequenceClassification
model = BertForSequenceClassification(pretrained_model_config)
model.load_state_dict({k.replace("model.", ""): v for k, v in fine_tuned_model_ckpt['state_dict'].items()})
model.eval()
def classification(sentence):
    inputs = tokenizer(
        [sentence],
        max_length=args.max_seq_length,
        padding="max_length",
        truncation=True,
    )
    with torch.no_grad():
        outputs = model(**{k: torch.tensor(v) for k, v in inputs.items()})
        prob = outputs.logits.softmax(dim=1)
        positive_prob = round(prob[0][1].item(), 4)
        negative_prob = round(prob[0][0].item(), 4)
        pred = 1 if torch.argmax(prob) == 1 else 0
    return (sentence,pred)

from wordcloud import WordCloud

#리뷰 csv파일을 읽어서 데이터프레임으로 만들기
# ㄱㅣ본저장경로
# static/images/movies/1/1.csv
# static/images/movies/2/2.csv


# 리뷰분석결과
#저장위치 맡게 변경
for i in range(1,11):
    print(i)
    # precondition:영화리뷰가 폴더별로 csv형식으로 저장되어있어야함
    reviews = pd.read_csv(f'./static/images/movies/{i}/{i}.csv')#영화리뷰csv읽기
    lst=reviews['Review'].tolist()#list
    predicted_sentiments = []
    # 이중 for문 반복인자 확인
    for j in lst:
        print((j))
        # Null값처리
        # 리뷰를 읽어오다보니 내용이 없는것도 끼어있음
        if len(j)==0:
            continue
        else:
            predicted_sentiment=classification(j)[1]
            predicted_sentiments.append(predicted_sentiment)
    reviews["sentiment_predicted"] = predicted_sentiments
    #영화리뷰분석결과csv저장
    # postcondition: 영화리뷰csv에 sentiment_predicted칼럼이 생성되고 그에 맞는 값들 채워짐
    reviews.to_csv(f'./static/images/movies/{i}/{i}.csv', index=False,encoding='utf-8-sig')#



# 워드클라우드
#     precondition:영화리뷰가 csv형태에서 df로 변환되어야됨
# 나눔고딕 폰트 파일의 경로 지정
    nanum_gothic_font_path = 'NanumGothic.ttf'

    wordcloud_directory = f'static/images/movies/{i}'


    #긍정리뷰
    def color(word,random_state=None,**kwargs):
        return 'rgb(0,0,200)' #blue
    # # df 형태는 기본적으로 object라서
    positive_reviews = reviews[reviews["sentiment_predicted"] == 1]["Review"]
    # 그냥하면 안되고 문자열 형식으로 바꿔주고 난 다음에 생성가능
    positive_reviews= ' '.join(positive_reviews)
    # print(positive_reviews)


    # 긍정 리뷰 워드 클라우드 생성 (단어 10개) 해결
    positive_wordcloud = WordCloud(
        font_path=nanum_gothic_font_path,
        width=800,
        height=400,
        background_color='white',
        prefer_horizontal=True,
        min_word_length=2,
        max_words=10,
        color_func=color


    ).generate(positive_reviews)
    positive_wordcloud.to_file(os.path.join(wordcloud_directory, "positive_wordcloud.jpg"))


    # 부정리뷰
    def color(word,random_state=None,**kwargs):
        return 'rgb(200,0,0)' #red
    # df_ground_truth에서 sentiment_predicted가 0인 리뷰만 추출
    negative_reviews = reviews[reviews["sentiment_predicted"] == 0]["Review"]
    # 그냥하면 안되고 문자열 형식으로 바꿔주고 난 다음에 생성가능
    negative_reviews= ' '.join(negative_reviews)

    # # 부정 리뷰 워드 클라우드 생성
    negative_wordcloud = WordCloud(
        font_path=nanum_gothic_font_path,
        width=800,
        height=400,
        background_color='white',
        prefer_horizontal=True,
        min_word_length=2,
        max_words=10,
        color_func=color
    ).generate(negative_reviews)

    # 워드 클라우드 이미지 저장
    negative_wordcloud.to_file(os.path.join(wordcloud_directory, "negative_wordcloud.jpg"))






    # top 10
    import matplotlib.pyplot as plt

    from konlpy.tag import Okt
    from collections import Counter
    #불용어 정하기 영화제목 등
    # 긍정리뷰
    # precondition: 리뷰가 문자열형태로 전달되어야함
    voc =positive_reviews
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
    plt.savefig(f'static/images/movies/{i}/positive.png')
    # 생성된 그래프를 화면에 출력하고, 내부적으로 그래프를 생성하기 위해 사용했던 메모리를 정리(clear)하는 역할

    plt.show()

    #
    # 부정리뷰에서 많이 나온 단어보여주기


    voc = negative_reviews
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
    plt.savefig(f'static/images/movies/{i}/negative.png')
    # 생성된 그래프를 화면에 출력하고, 내부적으로 그래프를 생성하기 위해 사용했던 메모리를 정리(clear)하는 역할

    plt.show()
