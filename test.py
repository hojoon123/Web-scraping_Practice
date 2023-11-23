import requests
from bs4 import BeautifulSoup
import mysql.connector

# 크롤링 해서 따오고 테이블 찾기 id 랭킹시스템
url = "https://www.acmicpc.net/ranklist/university"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
table = soup.find("table", {"id": "ranklist"})

#테이블에서 헤더 따서 입력하기(등수, 학교, 인원, 맞은문제, 제출수, 정답비율)
headers = []
for th in table.find_all("th"):
    headers.append(th.text)

# 테이블 열 다 따기(1, 카이스트, 1023, 18570, 609749, 51.324%)
rows = []
for tr in table.find_all("tr"):
    row = []
    # 선택한 열에서 테이블 정보 텍스트 다 끌어다가 넣기
    for td in tr.find_all("td"):
        row.append(td.text.strip())
    if row:
        rows.append(row)
        
print(headers)