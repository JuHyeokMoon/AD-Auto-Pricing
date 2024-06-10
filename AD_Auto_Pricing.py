from selenium import webdriver
from bs4 import BeautifulSoup
import pyperclip
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import warnings
import time
import configparser as parsers
import random
from datetime import datetime

warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings(action='ignore')

def price_control(price,max_price):
    driver = webdriver.Chrome()
    driver.get('https://searchad.naver.com/')
    time.sleep(3)

    tag_id = driver.find_element(By.NAME,'id')
    tag_pw = driver.find_element(By.NAME,'pw')

    # 아이디 복사
    tag_id.click()
    pyperclip.copy(userid)
    time.sleep(1)
    tag_id.send_keys(Keys.CONTROL, 'v')        # 윈도우
    # tag_id.send_keys(Keys.COMMAND, 'v')        # 맥
    time.sleep(1)

    # 비밀번호 복사
    tag_pw.click()
    pyperclip.copy(userpw)
    time.sleep(1)
    tag_pw.send_keys(Keys.CONTROL, 'v')
    # tag_pw.send_keys(Keys.COMMAND, 'v')
    time.sleep(1)

    # 로그인 버튼 클릭
    driver.find_element(By.CSS_SELECTOR,'#container > main > div.login_before > div.spot > home-login > div > div > fieldset > span > button').click()
    time.sleep(3)

    # 광고 플랫폼 버튼 클릭
    driver.find_element(By.CSS_SELECTOR,'#container > my-screen > div > div.spot > div > my-screen-board > div > div.top > ul > li:nth-child(1) > a > span').click()
    time.sleep(5)
    # driver.to_switch( driver.window_handles[1] )
    driver.switch_to.window(driver.window_handles[-1])  #새로 연 탭으로 이동
    time.sleep(3)

    # 주력캠페인 클릭
    driver.find_element(By.CSS_SELECTOR,'#root > div.sc-gKlEGG.bnBKUD > div.sc-jwrfVR.cbmsAI > div > div.sc-gRzACx.htmGqi > div:nth-child(3) > ul > li.active > div > div > div > div > ul > div:nth-child(4) > div > li:nth-child(12) > a').click()
    time.sleep(3)

    # 주간(주력) 클릭        
    driver.find_element(By.CSS_SELECTOR,'#grp-a001-02-000000026668544').click()
    time.sleep(3)

    # 현재 입찰가 가져오기
    my_input = driver.find_element(By.XPATH,'/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div[1]/div/div/div[3]/table/tbody/tr[3]/td[6]/span/span')
    current_value = my_input.text
    current_value = current_value.replace(",", "") 
    current_value = int(current_value.strip("'"))  
    next_value = int(current_value) + price

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    # 현재 입찰가 클릭
    td_tag = driver.find_element(By.XPATH,"/html/body/div[1]/div/div[2]/div/div[1]/div[4]/div/div[1]/div/div/div[3]/table/tbody/tr[3]/td[6]")
    span_tag = td_tag.find_element(By.TAG_NAME,"span")
    span_tag.click()
    time.sleep(3)
    # driver.execute_script("arguments[0].click();", span_tag)
    # time.sleep(3)
    
    input_box = driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(8) > div > div > div > div > div > div > input')
    input_box.click()
    time.sleep(2)

    # 광고료 MAX 값 확인하여 초과시 변경 없이 return
    ad_price = input_box.get_attribute('value')
    if int(ad_price) >= max_price:
        print(f"현재 광고료 {ad_price} 이 최대값 {max_price}원을 초과")
        driver.quit()
        return  

    input_box.clear()                           
    input_box.send_keys(Keys.CONTROL + "A")
    # input_box.send_keys(Keys.COMMAND + "A")
    time.sleep(1)
    input_box.send_keys(next_value)
    time.sleep(2)

    # 변경 버튼 클릭
    driver.find_element(By.CSS_SELECTOR,'body > div:nth-child(8) > div > div > div > div > div > div > span > button.btn.btn-primary').click()
    return next_value


def searching(seq, price):
    print('[동작 시간] '+time.strftime('%Y.%m.%d - %H:%M'))

    # 네이버 쇼핑에서 제품 검색한 주소 (2PAGE)
    url = "https://search.shopping.naver.com/search/all?adQuery=%EB%B9%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%84%B0&frm=NVSHATC&origQuery=%EB%B9%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%84%B0&pagingIndex=2&pagingSize=40&productSet=total&query=%EB%B9%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%84%B0&sort=rel&timestamp=&viewType=list"
    # url = "https://search.shopping.naver.com/search/all?query=%EB%B9%94%ED%94%84%EB%A1%9C%EC%A0%9D%ED%84%B0&cat_id=&frm=NVSHATC"
    driver = webdriver.Chrome()
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    # 광고 블록들 중 제목들 수집
    ad_divs = soup.find_all("div", {"class": "adProduct_item__1zC9h"})
    article_list = []
    for section in ad_divs:
        article = section.find("div", class_="adProduct_title__amInq")
        article_title = article.find("a", class_="adProduct_link__NYTV9 linkAnchor").text
        article_list.append(article_title)
    # print(results)
    driver.quit()

    # seq가 포함된 문자열 인덱스 찾기
    index = -1 
    for i, s in enumerate(article_list):
        if seq in s:
            index = i
            break
    
    if index == Top-1 :                             # 4등(Top-1)에 있으면 가격 내림
        price = -50
        current_price = price_control(price)
        print(f"Price Down!!  {current_price} !!")
    elif index > Top-1 :                            # 4등 보다 아래에 있면 가격 올림
        price = 50
        current_price = price_control(price)
        print(f"Price Up!!  {current_price} !!")
    elif index < Top-1 :                            # 4등 보다 위에 있으면 가격 내림
        price = -50
        current_price = price_control(price)
        print(f"Price Down!!  {current_price} !!")
    else :                                          # 광고 리스트에 없는 경우 
        print("Warning !!!")
        print(f"{seq} is not found !!!")
        print("-----------------------------------------------------")


def check_time_and_run():
    # 현재 요일과 시간을 확인
    now = datetime.now()
    current_hour = now.hour
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    current_day = days[now.weekday()]
    
    # 현재 요일이 time_list 딕셔너리에 있으면 해당 요일의 시간 리스트를 가져옴
    if current_day in time_list:
        # 현재 시간이 해당 요일의 시간 리스트에 있으면 작업 실행
        if current_hour in time_list[current_day]:
            searching(seq, price)
    #     else:
            # print(f"{current_hour} 시간에는 동작 X.")
    # else:
    #     print(f"{current_day} 은 동작 X")


# 폴더 절대 경로
path="C:/Users/MoonJu/Documents/macro"

# 아이디 비밀번호 불러오기
properties = parsers.ConfigParser()
properties.read(f"{path}/config.ini")
userid = str(properties['macro']['user'])
userpw = str(properties['macro']['password'])

time_list = {'Sun': [0,21,22,23],   # 0~1시, 21~22시, 22~23시, 23~24시 동작
             'Mon': [0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,21,22,23],
             'Tue': [0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,21,22,23],
             'Wed': [0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,21,22,23],
             'Thu': [0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,21,22,23],
             'Fri': [0,5,6,7,8,9,10,11,12,13,14,15,16,17,18,21,22,23],
             'Sat': [0,21,22,23]}

seq = ""            # 쇼핑 광고 Top 위치에 검색할 단어
price = 50          # 변동할 가격
max_price = 2000    # 가격 최대값
Top = 4

# 3분 ~ 7분 랜덤 동작
while True:
    check_time_and_run()
    time.sleep(random.randint(3*60, 7*60))

