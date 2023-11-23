from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller as AutoChrome
from selenium.webdriver.common.keys import Keys
import time
import pyperclip
import pyautogui
import openpyxl
import pandas as pd
import numpy as np
import re

def updateChrome():
    global driver,searchdriver
    #크롬드라이버 버전 확인
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0] 
    
    options = webdriver.ChromeOptions() # 브라우저 셋팅
    options.add_experimental_option("detach", True) # 브라우저 꺼짐 방지
    options.add_argument('lang=ko_KR') # 사용언어 한국어
    options.add_argument('disable-gpu') # 하드웨어 가속 안함
    #options.add_argument("headless") # 백그라운드 실행
    options.add_experimental_option("excludeSwitches",['enable-logging']) # 불필요한 에러 메세지 삭제
    
    #실행 후 최신 버젼이 아니라서 실행이 안된다면 최신버젼으로 업데이트 후 재실행
    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options = options)
        searchdriver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options = options)

    except:
        AutoChrome.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options = options)
        searchdriver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options = options)

    driver.implicitly_wait(10)
    searchdriver.implicitly_wait(10)

def urlOpen():
    # driver 가져오기
    driver.get("https://www.acmicpc.net/ranklist/university")
    driver.implicitly_wait(10)
    #학교 따오기 용 url
    searchdriver.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B0%80%ED%86%A8%EB%A6%AD%EA%BD%83%EB%8F%99%EB%84%A4%EB%8C%80%ED%95%99%EA%B5%90&oquery=%EC%B6%A9%EC%B2%AD%EB%82%A8%EB%8F%84+%EB%8C%80%ED%95%99&tqi=iug9TlprvTVssRAKFsNssssss%2FR-055184")
    searchdriver.implicitly_wait(10)

def getStudentData():
    global gyeonggi_student,chungbuk_student,chungnam_student,gyeongbuk_student,gyeongnam_student,junbuk_student,junnam_student,gangwon_student,foreign_student,jejudo_student
    student_list = []
    cnt = 0
    while 1:
        cnt += 1
        student_table = driver.find_element(By.XPATH,'//*[@id="ranklist"]')
        for s_tr in student_table.find_elements(By.TAG_NAME,"tr"):
            s_row = []
            s_tds = s_tr.find_elements(By.TAG_NAME,"td")
            for s_td in s_tds:
                s_row.append(s_td.get_attribute('textContent'))
            if s_row:
                student_list.append(s_row)
        try:
            next_page()
        except:
            break
    for i in range(cnt):
        driver.back()
        driver.implicitly_wait(2)
    return student_list

    

def getData():
    global headers, gyeonggi_univercity,chungbuk_univercity,chungnam_univercity,gyeongbuk_univercity,gyeongnam_univercity,junbuk_univercity,junnam_univercity,gangwon_univercity,foreign_univercity,jejudo_univercity
    # table 데이터 가져오기
    table = driver.find_element(By.XPATH,'//*[@id="ranklist"]')
    driver.implicitly_wait(10)
    tr_cnt = 0
    # headers 넣기
    if not headers:
        for th in table.find_elements(By.TAG_NAME,"th"):
            headers.append(th.get_attribute('textContent'))

    # 대학 분류
    for tr in table.find_elements(By.XPATH,'//*[@id="ranklist"]/tbody'):
        tr_cnt += 1
        row = []
        driver.implicitly_wait(10) 
        time.sleep(5)
        tr.find_element(By.XPATH,'//*[@id="ranklist"]/tbody/tr[1]/td[2]').click()
        driver.implicitly_wait(10)
        s_list = getStudentData()
        # for td in tr.find_elements(By.XPATH,'//*[@id="ranklist"]/tbody/tr[{0}]'.format(tr_cnt)):
        #     row.append(td.get_attribute('textContent'))
        # if row:
        #     #등수 빼기
        #     row.pop(0)
        #     #오류 나는 대학 구글로 다시 검색
        #     areaName = getUnivercityAreaFromNaver(row[0])
        #     if re.match('[ㄱ-ㅎㅏ-ㅣ가-힣]', row[0]):
        #         if areaName == '예외':
        #             areaName = getUnivercityAreaFromGoogle(row[0])
            
            
        #     #대학 분류
        #     if '서울' in areaName or '경기' in areaName or '인천' in areaName:
        #         gyeonggi_univercity.append(row)
        #         gyeongbuk_student.extend(s_list)
        #     elif '충청북도' in areaName or '충북' in areaName:
        #         chungbuk_univercity.append(row)
        #         chungbuk_student.extend(s_list)
        #     elif '충청남도' in areaName or '충남' in areaName or '대전' in areaName or '세종' in areaName:
        #         chungnam_univercity.append(row)
        #         chungnam_student.extend(s_list)
        #     elif '경상북도' in areaName or '경북' in areaName or '대구' in areaName:
        #         gyeongbuk_univercity.append(row)
        #         gyeongbuk_student.extend(s_list)
        #     elif '경상남도' in areaName or '경남' in areaName or '부산' in areaName or '울산' in areaName:
        #         gyeongnam_univercity.append(row)
        #         gyeongnam_student.extend(s_list)
        #     elif '전라북도' in areaName or '전북' in areaName:
        #         junbuk_univercity.append(row)
        #         junbuk_student.extend(s_list)
        #     elif '전라남도' in areaName or '전남' in areaName or '광주' in areaName:
        #         junnam_univercity.append(row)
        #         junnam_student.extend(s_list)
        #     elif '강원' in areaName:
        #         gangwon_univercity.append(row)
        #         gangwon_student.extend(s_list)
        #     elif '제주' in areaName:
        #         jejudo_univercity.append(row)
        #         jejudo_student.extend(s_list)
        #     else:
        #         foreign_univercity.append(row)
        #         foreign_student.extend(s_list)
                

def next_page():
    # 다음 페이지
    driver.find_element(By.XPATH,'//*[@id="next_page"]').click()
    driver.implicitly_wait(10)
    
    
def getUnivercityFromNaver():
    global headers, rows
    # 대학 데이터
    table = driver.find_element(By.XPATH,'//*[@id="tab1_menu"]/div[2]')

    # 대학명 넣기
    if not headers:
        for a in table.find_elements(By.TAG_NAME,"a"):
            headers.append(a.get_attribute('textContent'))

def getUnivercityAreaFromGoogle(name):
    #google
    searchdriver.get('https://www.google.com/search?q=%EC%97%B0%EC%84%B8%EB%8C%80%ED%95%99%EA%B5%90&sxsrf=APwXEdfrld2F8gjoQW4rCYwYl7BDTemFWQ%3A1680327779719&ei=Y8QnZLm8K9ff2roP8JG9kAk&ved=0ahUKEwj5-anj_If-AhXXr1YBHfBID5IQ4dUDCA8&uact=5&oq=%EC%97%B0%EC%84%B8%EB%8C%80%ED%95%99%EA%B5%90&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIECCMQJzITCC4QgAQQFBCHAhCxAxDUAhDqBDINCAAQgAQQFBCHAhCxAzIRCC4QgAQQsQMQgwEQxwEQrwEyCwguEIAEEMcBEK8BMgUIABCABDIFCAAQgAQyBQgAEIAEMgsILhCABBDHARCvATIFCAAQgAQyHgguEIAEEBQQhwIQsQMQ1AIQ6gQQ3AQQ3gQQ4AQYAToKCC4QgAQQFBCHAjoLCC4QgAQQsQMQgwE6CAguEIAEELEDOgsIABCABBCxAxCDAToHCCMQ6gIQJzoRCC4QgAQQsQMQgwEQxwEQ0QM6CAgAEIAEELEDOgQIABADOgcIABCKBRBDOhAILhCABBAUEIcCELEDENQCOg0ILhCKBRDHARCvARBDSgQIQRgAUABY_AtgywxoA3ABeAGAAZABiAGlDJIBBDAuMTKYAQCgAQGwAQrAAQHaAQYIARABGBQ&sclient=gws-wiz-serp')
    searchdriver.implicitly_wait(2)
    searchdriver.find_element(By.XPATH,'//*[@id="tsf"]/div[1]/div[1]/div[2]/div/div[2]/input').click()
    pyautogui.hotkey('ctrl', 'a')
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    searchdriver.implicitly_wait(2)
    try:
        univercityAreaName = searchdriver.find_element(By.XPATH,'//*[@id="kp-wp-tab-overview"]/div[1]/div/div/div/div/div/div[5]/div/div/div/span[2]').get_attribute('textContent')
    except:
        univercityAreaName = '예외'
    
    searchdriver.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EA%B0%80%ED%86%A8%EB%A6%AD%EA%BD%83%EB%8F%99%EB%84%A4%EB%8C%80%ED%95%99%EA%B5%90&oquery=%EC%B6%A9%EC%B2%AD%EB%82%A8%EB%8F%84+%EB%8C%80%ED%95%99&tqi=iug9TlprvTVssRAKFsNssssss%2FR-055184")
    searchdriver.implicitly_wait(2)
    return univercityAreaName
    
def getUnivercityAreaFromNaver(name):
    #naver
    searchdriver.find_element(By.XPATH,'//*[@id="nx_query"]').click()
    pyautogui.hotkey('ctrl', 'a')
    pyperclip.copy(name)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    searchdriver.implicitly_wait(2)
    try:
        univercityAreaName = searchdriver.find_element(By.XPATH,'//*[@id="main_pack"]/div[2]/div[2]/div[1]/div/div[2]/dl/div[1]/dd').get_attribute('textContent')
    except:
        univercityAreaName = '예외'
    return univercityAreaName
        


if __name__ =="__main__":
    
    
    #등수, 학교, 인원, 맞은문제, 제출, 정답비율
    headers = []
    #지역별 대학 순위를 위한 배열
    gyeonggi_univercity,chungbuk_univercity,chungnam_univercity,gyeongbuk_univercity,gyeongnam_univercity,junbuk_univercity,junnam_univercity,gangwon_univercity,foreign_univercity,jejudo_univercity = [],[],[],[],[],[],[],[],[],[]
    #지역별 학생 순위를 위한 배열
    gyeonggi_student,chungbuk_student,chungnam_student,gyeongbuk_student,gyeongnam_student,junbuk_student,junnam_student,gangwon_student,foreign_student,jejudo_student = [],[],[],[],[],[],[],[],[],[]

    updateChrome()
    urlOpen()
    getData()
    # while 1:
    #     try:
    #         next_page()
    #         getData()
    #     except:
    #         break
    print(headers)
    print()
    print(gyeonggi_univercity)
    print()
    print(chungbuk_univercity)
    print()
    print(chungnam_univercity)
    print()
    print(gyeongbuk_univercity)
    print()
    print(gyeongnam_univercity)
    print()
    print(junbuk_univercity)
    print()
    print(junnam_univercity)
    print()
    print(gangwon_univercity)
    print()
    print(foreign_univercity)
    print()
    print(jejudo_univercity)
    print()
    
    a,b,c,d,e,f,g,h,i,j = len(gyeonggi_univercity),len(chungbuk_univercity),len(chungnam_univercity),len(gyeongbuk_univercity),len(gyeongnam_univercity),len(junbuk_univercity),len(junnam_univercity),len(gangwon_univercity),len(foreign_univercity),len(jejudo_univercity)

    print(a) 
    print(b)
    print(c) 
    print(d)
    print(e) 
    print(f)
    print(g) 
    print(h)
    print(i) 
    print(j)
    print(a+b+c+d+e+f+g+h+i+j)
    
    print(gyeonggi_student)
    print()
    print(chungbuk_student)
    print()
    print(chungnam_student)
    print()
    print(gyeongbuk_student)
    print()
    print(gyeongnam_student)
    print()
    print(junbuk_student)
    print()
    print(junnam_student)
    print()
    print(gangwon_student)
    print()
    print(foreign_student)
    print()
    print(jejudo_student)
    print()
    driver.quit()
    searchdriver.quit()