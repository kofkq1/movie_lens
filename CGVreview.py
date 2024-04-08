import time
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')



def get_movie_reviews(url, page_num = 10):

    wd = webdriver.Chrome()
    wd.get(url)

    # writer_list = [] # 작성자
    review_list = [] # 리뷰
    date_list = [] # 작성일

    for page_no in range(1, page_num + 1):
        try:
            page_ul = wd.find_element(By.ID,'paging_point')
            page_a = page_ul.find_element(By.LINK_TEXT, str(page_no))
            page_a.click()
            time.sleep(2)

            reviews = wd.find_elements(By.CLASS_NAME, 'box-comment')
            review_list += [ review.text for review in reviews]

            dates = wd.find_elements(By.CLASS_NAME, 'day')
            date_list += [date.text for date in dates]

            if page_no % 10 == 0: # 현재 페이지가 10페이지일 경우
                next_button = page_ul.find_element(By.CLASS_NAME, 'btn-paging.next')
                next_button.click() # 다음 10개 버튼 누름
                time.sleep(1)
        except NoSuchElementException:
            break
    # 사용자 이름은 필요없음
    movie_review_df = pd.DataFrame({
                                    'Review' : review_list
                                    })
    
    wd.close()
    return movie_review_df
#url입력말고 이름으로 입력하게 하고싶으면?

url = 'http://www.cgv.co.kr/movies/detail-view/?midx=87554'
movie_review_df = get_movie_reviews(url, 10) # 리뷰 받을 페이지 숫자
movie_review_df.to_csv('data/cgvreviews.csv', index=False)