import matplotlib.pyplot as plt

# 첫 번째 데이터 세트 준비
# train
x1 = [0.274,0.123, 0.131, 0.12, 0.112] # 손실함수
y1= [0,1,2,3,4]
x1 = [0.875, 0.875, 0.938, 0.95, 0.96]#정확도
# test
# 두 번째 데이터 세트 준비
x2 = [0.295,0.285 , 0.289, 0.309, 0.33]# 손실함수 val
x2 = [0.878, 0.888, 0.883, 0.886, 0.88]# 정확도 val
y2= [0,1,2,3,4]

# 첫 번째 데이터 세트로 그래프 그리기
plt.plot(y1,x1, label='train_accuracy')

# 두 번째 데이터 세트로 그래프 그리기
plt.plot( y2,x2, label='test_accuracy')

# 제목과 축 라벨 추가
plt.title('accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')

# 범례 추가
plt.legend()

# 그래프 표시
plt.show()




#
# # 영화정보 가져오기
# df2 = pd.read_csv('static/images/updated_weekly_box_office_details.csv')
# selected_columns = df2[['title','director','actors','genres','summary']]
# title=(selected_columns['title'])
# director=(selected_columns['director'].tolist())[1-1]
# actors=(selected_columns['actors'])[0]
# # str을 list로 변환
#
# my_list = [s for s in actors.split(",") if s]
# print(my_list[0])
# print(selected_columns['actors'])