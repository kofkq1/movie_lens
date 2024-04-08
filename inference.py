# 매주 업데이트 되는 영화 순위에 올라와 있는 영화제목에 해당하는 영화내용 가져오기
from ratsnlp.nlpbook.classification import ClassificationDeployArguments
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
def inference_fn(sentence):
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
import pandas as pd
#저장위치 맡게 변경
for i in range(1,11):
    reviews = pd.read_csv(f'./static/images/movies/{i}/{i}.csv')#영화리뷰csv읽기
    lst=reviews['Review'].tolist()#list
    predicted_sentiments = []
    # 이중 for문 반복인자 확인
    for j in lst:
        print(inference_fn(j))
        predicted_sentiment=inference_fn(j)[1]
        predicted_sentiments.append(predicted_sentiment)
    reviews["sentiment_predicted"] = predicted_sentiments
    reviews.to_csv(f'./static/images/movies/{i}/{i}.csv', index=False,encoding='utf-8-sig')
    #영화리뷰분석결과csv저장