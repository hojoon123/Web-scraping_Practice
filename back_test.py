from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller as AutoChrome
from selenium.webdriver.common.keys import Keys
import requests

# 크롬 업데이트
def updateChrome():
    global driver
    # 크롬드라이버 버전 확인
    chrome_ver = AutoChrome.get_chrome_version().split('.')[0]

    options = webdriver.ChromeOptions()  # 브라우저 셋팅
    options.add_experimental_option("detach", True)  # 브라우저 꺼짐 방지
    options.add_argument('lang=ko_KR')  # 사용언어 한국어
    options.add_argument('disable-gpu')  # 하드웨어 가속 안함
    # options.add_argument("headless") # 백그라운드 실행
    options.add_experimental_option("excludeSwitches", ['enable-logging'])  # 불필요한 에러 메세지 삭제

    # 실행 후 최신 버젼이 아니라서 실행이 안된다면 최신버젼으로 업데이트 후 재실행
    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)

    except:
        AutoChrome.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe', options=options)

    driver.implicitly_wait(10)

# 과랭킹
def getSwRank(user_id):
    driver.get("https://www.acmicpc.net/group/ranklist/16900")
    driver.implicitly_wait(10)
    cnt = 0
    while 1:
        try:
            cnt += 1
            student_id = driver.find_element(By.XPATH, f'// *[ @ id = "ranklist"] / tbody / tr[{cnt}] / td[2] / a').text

            if user_id == student_id:
                swRank = int(driver.find_element(By.XPATH, f'// *[ @ id = "ranklist"] / tbody / tr[{cnt}] / td[1]').text)
                return swRank

        except:
            return




# 목포 랭킹
def getMokpoRank(user_id):
    driver.get("https://www.acmicpc.net/school/ranklist/275")
    driver.implicitly_wait(10)
    cnt = 0

    while 1:
        cnt += 1
        try:
            student_id = driver.find_element(By.XPATH, f'//*[@id="ranklist"]/tbody/tr[{cnt}]/td[2]/a').text
            if user_id == student_id:
                mokpo_rank = int(driver.find_element(By.XPATH, f'// *[ @ id = "ranklist"] / tbody / tr[{cnt}] / td[1]').text)
                return mokpo_rank
        except:
            return



# 전체 등수
def getAllRank(user_id):
    driver.get(f"https://www.acmicpc.net/user/{user_id}")
    driver.implicitly_wait(10)
    allRank = int(driver.find_element(By.XPATH,'// *[ @ id = "statics"] / tbody / tr[1] / td').text)
    driver.implicitly_wait(10)

    return allRank

# 맞은 문제
def getSolvedPS():
    solvedPS = int(driver.find_element(By.XPATH, '// *[ @ id = "u-solved"]').text)
    driver.implicitly_wait(10)

    return solvedPS

# solved data
def solvedData(user_id):
    arr = []
    try:
        api_key = "123"
        url = f"https://solved.ac/api/v3/user/show?apiKey={api_key}&handle={user_id}"
        response = requests.get(url).json()
    except:
        return ['솔브드x', '미인증', '미인증', '미인증']

    arr.append(response['rank'])
    tier = response['tier']
    # 12345 브론즈54321 678910 실버54321 등등..
    #
    cnt = 0
    if tier % 5 == 0:
        tier -= 1
        cnt += 1

    if tier // 5 == 0:
        out_tier = "Bronze"
    elif tier // 5 == 1:
        out_tier = "Silver"
    elif tier // 5 == 2:
        out_tier = "Gold"
    elif tier // 5 == 3:
        out_tier = "Platinum"
    elif tier // 5 == 4:
        out_tier = "Diamond"
    elif tier // 5 == 5:
        out_tier = "Ruby"
    else:
        out_tier = "UnRank"

    if cnt:
        tier += 1

    if out_tier != "UnRank":
        if tier % 5 == 0:
            out_tier += str(1)
        else:
            out_tier += str(6 - (tier % 5))

    arr.append(out_tier)
    arr.append(response['rating'])
    arr.append(response['exp'])


    return arr

def ranking_check():
    global students_data
    for i in range(len(students_data)):
        for j in range(len(students_data)):
            if students_data[i][0] == pre_students[j][0]:
                # 등수만
                for k in range(2, 6):
                    if pre_students[j][k] == None or pre_students[j][k] in ['솔브드x', '미인증']:
                        continue
                    if students_data[i][k] != pre_students[j][k]:
                        tmp = students_data[i][k] - pre_students[j][k]
                        if tmp < 0:
                            tmp = str(abs(tmp)) + '^'
                        elif tmp > 0:
                            tmp = '-' + str(tmp)
                        students_data[i][k] = str(students_data[i][k]) + f'({tmp})'
                # 맞은문제, 레이팅
                dataList = [6, 8]
                growth = 0
                for k in dataList:
                    if pre_students[j][k] in ['솔브드x', '미인증']:
                        continue
                    if students_data[i][k] != pre_students[j][k]:
                        increased_value = students_data[i][k] - pre_students[j][k]
                        growth += increased_value
                        tmp = '+' + str(increased_value)
                        students_data[i][k] = str(students_data[i][k]) + f'({tmp})'
                # 맞은문제 + 레이팅 증가량 성장률에 넣기
                students_data[i][10] = growth

                break

if __name__ == '__main__' :

    students = [['황성민','qq221qq'], ['최승현','csh7099'], ['정헌수','ggb05224'], ['강호준','rhzn5512'],
                ['박건홍','awaw643'], ['한동효','byung2000'], ['배재현','cyclebae'], ['정유태','dage8044'],
                ['함지수','hjsu0825'], ['홍승우','hsw2689'], ['오제욱','ink21'], ['김도은','kdeun8485'],
                ['김태랑','ktr040415'], ['김민규','lidersy961'], ['박지은','pju615'], ['고다은','rhekdms0507'],
                ['강민지','rkdalswl403'], ['정희주','wjdgm2479'], ['김서현','lskxw'],['임진호','njlcs3501'],
                ['이민우','dlaksen99'],['김혜원','kimwon23'],['이건원','syrjsdnjs']]

    pre_students = [
        ["정헌수", "ggb05224", 1, 1, 2736, 7982, 596, "Gold1", 1487, 4755462, 0],
        ["김태랑", "ktr040415", 2, 3, 3820, 15963, 508, "Gold3", 1206, 1883656, 0],
        ["황성민", "qq221qq", 3, 5, 5137, 10676, 439, "Gold2", 1383, 3383272, 0],
        ["강호준", "rhzn5512", 4, 7, 7301, 11936, 364, "Gold2", 1337, 2580391, 0],
        ["최승현", "csh7099", 5, 8, 8223, 23673, 341, "Gold4", 974, 1205011, 0],
        ["김민규", "lidersy961", 6, 11, 12186, 16657, 274, "Gold3", 1186, 5645897, 0],
        ["오제욱", "ink21", 7, 12, 13315, "솔브드x", 260, "미인증", "미인증", "미인증", 0],
        ["정희주", "wjdgm2479", 8, 20, 26207, 31735, 169, "Silver1", 757, 489420, 0],
        ["정유태", "dage8044", 9, 21, 28034, 33813, 160, "Silver1", 705, 441086, 0],
        ["고다은", "rhekdms0507", 10, 24, 30060, 48501, 152, "Silver3", 419, 145155, 0],
        ["배재현", "cyclebae", 11, 28, 42029, 52418, 116, "Silver4", 363, 109967, 0],
        ["함지수", "hjsu0825", 12, 38, 70625, 63585, 70, "Silver5", 242, 65049, 0],
        ["홍승우", "hsw2689", 13, 39, 72616, 63113, 68, "Silver5", 246, 65135, 0],
        ["박지은", "pju615", 14, 40, 74735, 66300, 66, "Silver5", 219, 57927, 0],
        ["한동효", "byung2000", 15, 41, 76925, 70626, 64, "Bronze1", 187, 44982, 0],
        ["김도은", "kdeun8485", 16, None, 91776, 69452, 53, "Bronze1", 196, 52076, 0],
        ["강민지", "rkdalswl403", 17, 51, 105742, "솔브드x", 44, "미인증", "미인증", "미인증", 0],
        ["박건홍", "awaw643", 18, 63, 168408, "솔브드x", 20, "미인증", "미인증", "미인증", 0],
        ["임진호", "njlcs3501", 19, None, 169994, 95625, 19, "Bronze5", 43, 11154, 0],
        ["이민우", "dlaksen99", 20, 67, 173455, 84298, 19, "Bronze4", 104, 190034, 0],
        ["김서현", "lskxw", 21, None, 241661, 105333, 7, "UnRank", 13, 3360, 0],
        ['이건원', 'syrjsdnjs', 22, 59, 311553, '솔브드x', 2, '미인증', '미인증', '미인증', 0],
        ['김혜원', 'kimwon23', 23, 76, 311553, '솔브드x', 2, '미인증', '미인증', '미인증', 0],
    ]
    students_data = [['Noname', 'id', int(0), int(0), int(0), int(0), int(0), 'tier', int(0), int(0), int(0)] for i in range(len(students))]
    data_list = ["이름", "아이디", "학과등수", "목대등수", "전체등수", "티어등수", "맞은문제", "티어", "레이팅", "경험치", "성장률"]
    # 이름 아이디 과등수 목대등수 전체등수 솔브드등수 맞은문제 티어 레이팅 경험치 성장률
    # 0     1     2     3       4       5       6       7    8      9 10
    # 일주일 전 데이터와 비교 한달 전 데이터와 비교 등등
    # 솔브드 등수와 문제 수를 적절히 조화해서 이전대비 성장 정도 측정
    # 확인할 수 있게 만들기
    updateChrome()

    print(*data_list)
    # arr에 하나씩 순서대로 정보 추가
    for i in range(len(students)):
        students_data[i][0] = students[i][0] # name 넣기
        students_data[i][1] = students[i][1] # id 넣기
        students_data[i][3] = getMokpoRank(students[i][1]) # 목대 등수
        students_data[i][2] = getSwRank(students[i][1]) # 과 등수
        students_data[i][4] = getAllRank(students[i][1])  # 전체등수 넣기
        students_data[i][6] = getSolvedPS() # 맞은 문제 넣기
        sd = solvedData(students[i][1]) # 랭크 티어 레이팅 경험치
        students_data[i][5] = sd[0] # 솔브드등수
        students_data[i][7] = sd[1] # 티어
        students_data[i][8] = sd[2] # 레이팅
        students_data[i][9] = sd[3] # 경험치
        # students_data[i][10]  # 성장률
    students_data.sort(key=lambda x: x[2])
    for i in range(len(students)):
        print(*students_data[i])
    ranking_check()
    for i in range(len(students)):
        print(*students_data[i])
    driver.quit()