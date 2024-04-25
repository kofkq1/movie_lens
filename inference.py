# 매주 업데이트 되는 영화 순위에 올라와 있는 영화제목에 해당하는 영화내용 가져오기
# 여기가 경량화 코드
import time
class ClassificationArguments:

    def __init__(
            self,
            pretrained_model_name=None,
            downstream_model_dir=None,
            downstream_model_checkpoint_fpath=None,
            max_seq_length=128,
    ):
        self.pretrained_model_name = pretrained_model_name
        self.max_seq_length = max_seq_length
        self.downstream_model_dir=downstream_model_dir,
        self.downstream_model_checkpoint_fpath = downstream_model_checkpoint_fpath
        # 없어도됨
        print(f"model is ready")

#         실행환경설정
args = ClassificationArguments(
    pretrained_model_name="beomi/kcbert-base",#학습시킨 데이터 모델
    #  학습파일저장경로 확인
    downstream_model_dir="./data",
    max_seq_length=128,
    downstream_model_checkpoint_fpath="data/epoch=1-val_loss=0.27.ckpt"

)
# 토크나이저 설정
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained(
    args.pretrained_model_name,
    do_lower_case=False,


)
#모델 불러오기
import torch
fine_tuned_model_ckpt = torch.load(
    args.downstream_model_checkpoint_fpath,
    map_location=torch.device("cpu"),
)
#모델 설정불로오기
from transformers import BertConfig
# BertConfig.get_config_dict()
pretrained_model_config = BertConfig.from_pretrained(
    # hugginface에서 제공하는 bert모델이어야지만 사용가능
    args.pretrained_model_name,
    # 2개의 라벨로 분류 (긍정, 부정)
    #  최종적으로 분류해야 할 범주의 수를 나타냅니다.
    num_labels=2,
)
# 생성자에 전달된 pretrained_model_config는 사전에 정의된 BERT 모델 구성을 담고 있으며, 이 구성에는 예를 들어 모델이 예측해야 할 레이블의 개수(num_labels)와 같은 중요한 정보가 포함됩니다.
# 이 과정을 통해 특정 시퀀스 분류 작업을 위한 BERT 모델이 초기화됩니다.
#어떤 task로 (분류 ,단어생성,qa) bert 사용할 지-layer 추가
# 분류 작업에 필요한 출력 레이어가 추가되어 있습니다.
from transformers import BertForSequenceClassification
model = BertForSequenceClassification(pretrained_model_config)
# 세부 조정된(fine-tuned) 모델의 체크포인트에서 상태 딕셔너리(state_dict)를 불러와 현재 모델에 적용합니다.
# fine_tuned_model_ckpt['state_dict']는 세부 조정된 모델의 가중치와 매개변수를 담고 있는 딕셔너리입니다.
# k.replace("model.", ""): v는 체크포인트의 키 이름에서 "model." 접두사를 제거하여 현재 모델의 상태 딕셔너리와 일치시키는 과정을 나타냅니다.
# 이는 체크포인트와 모델의 매개변수 이름이 정확히 일치하지 않을 때 필요한 조정입니다.
# ('model.classifier.weight', tensor([[ 0.0148, -0.0061,  0.0014,  ...,  0.0114, -0.0156,  0.0084],
#                                     [ 0.0156, -0.0034, -0.0146,  ...,  0.0338, -0.0164,  0.0060]])), ('model.classifier.bias', tensor([ 0.0005, -0.0005]))])
# 가중치와 매개변수전달
model.load_state_dict({k.replace("model.", ""): v for k, v in fine_tuned_model_ckpt['state_dict'].items()})
# 모델을 평가 모드로 설정 dropout 및 batchnorm 을 비활성화
model.eval()


import torch
from captum.attr import IntegratedGradients

def inference_fn_with_attribution(sentence):
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

    integrated_gradients = IntegratedGradients(model)
    attributions, _ = integrated_gradients.attribute(
        inputs["input_ids"], target=pred, return_convergence_delta=True
    )

    # 단어별 attribution 값 출력
    word_attributions = [round(attr.item(), 2) for attr in attributions[0]]
    word_attribution_pairs = list(zip(inputs.input_ids[0], word_attributions))

    # 단어와 attribution 값 출력
    for word, attribution in word_attribution_pairs:
        if word != tokenizer.pad_token_id:
            print(f"{tokenizer.decode([word])}: {attribution}")
# 예시 사용
print(inference_fn_with_attribution("이 영화 노잼이네요"))

import pandas as pd
# #저장위치 맡게 변경
# for i in range(1,11):
#     reviews = pd.read_csv(f'./static/images/movies/{i}/{i}.csv')#영화리뷰csv읽기
#     lst=reviews['Review'].tolist()#list
#     predicted_sentiments = []
#     # 이중 for문 반복인자 확인
#     for j in lst:
#         print(inference_fn(j))
#         predicted_sentiment=inference_fn(j)[1]
#         predicted_sentiments.append(predicted_sentiment)
#     reviews["sentiment_predicted"] = predicted_sentiments
#     reviews.to_csv(f'./static/images/movies/{i}/{i}.csv', index=False,encoding='utf-8-sig')
    #영화리뷰분석결과csv저장

# print(inference_fn("이게 돈받고 파는거냐"))
# validationset
# import requests
# # 167378686  잠 이부분이 영화별로 부여된 아이디
# # 대상 URL 범죄도시2
# #반복문으로
# positive=[]
# negative=[]
# neutral=[]
# all=[]
# #  'https://comment.daum.net/apis/v1/posts/149513756/comments?parentId=0&offset=10&limit=30&sort=RECOMMEND&isInitial=false&hasNext=true' 다음영화 transformer
# for i in range(14):
#     offset=i*100
#     url=f'https://comment.daum.net/apis/v1/posts/149662594/comments?parentId=0&offset={offset}&limit=100&sort=LATEST&isInitial=false&hasNext=false'
#     # HTTP GET 요청을 보내고 응답을 받습니다.
#     time.sleep(2)
#     response = requests.get(url)
#     # response.ok
#     data = response.json()
#
#     for i in data:
#
#         score=i['rating']
#         if score>=7:
#             positive.append((i['content'],i['rating']))
#         elif score==5 or score==6 :
#             neutral.append((i['content'],i['rating']))
#             #1,2,3,4
#         else:
#             negative.append((i['content'],i['rating']))
# # inference_fn한 결과와 함께 저장
# positive_count=0
# negative_count=0
# for i in positive:
#      if inference_fn(i[0])[1]==1:
#          positive_count+=1
# for i in negative:
#     if inference_fn(i[0])[1]==0:
#         negative_count+=1
# #   positive 리스트에서 inference_fn(i[0])[1]==1 인 비율을 구하고싶어
# print(positive_count/len(positive))
# print(negative_count/len(negative))


#     print(inference_fn(i[0]),i[1])
# for i in negative:
#     print(inference_fn(i[0]),i[1])

# def inference_fn(sentence):
#     inputs = tokenizer(
#         [sentence],
#         max_length=args.max_seq_length,
#         padding="max_length",
#         truncation=True,
#
#     )
# with torch.no_grad():
#     outputs = model(**{k: torch.tensor(v) for k, v in inputs.items()})
# prob = outputs.logits.softmax(dim=1)
# positive_prob = round(prob[0][1].item(), 4)
# negative_prob = round(prob[0][0].item(), 4)
# pred = 1 if torch.argmax(prob) == 1 else 0
# return (sentence,pred)