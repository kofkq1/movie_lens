import glob
import pandas as pd
folder_path = "static/images/movies/10/actors"
# 2_1.jpg
# 파일속성으로 가져올지
# 이름규칙으로 가져올지
file_count = len(glob.glob(folder_path + '/*.jpg'))
print(file_count)






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