from selenium import webdriver
import time

#directory 설정
import os
os.chdir("C:\\Users\\lucia\\Downloads")

#크롬드라이버 파일 directory에 위치시키기
driver = webdriver.Chrome()
driver.get("http://www.naver.com")
driver.implicitly_wait(3) #암묵적으로 웹 자원을 (최대) 3초 기다리기

#큰따옴표 안에 따옴표를 글자열 끝으로 인식하기 때문에 백슬래시를 넣어 표기 \" 
newsSection = driver.find_element_by_xpath("//*[@id=\"NM_FAVORITE\"]/div[1]/ul[2]/li[2]/a")
newsSection.click()


from selenium.webdriver.common.keys import Keys

#주소1 : copy->xpath
searchBox = driver.find_element_by_xpath("//*[@id=\"lnb.searchForm\"]/fieldset/input[1]")
searchBox.send_keys("규제")
searchBox.send_keys(Keys.ENTER)

#주소2: 직접 입력
searchBox = driver.find_element_by_xpath("//form[@id='lnb.searchForm']/fieldset/input[1]")
searchBox.send_keys("규제")
searchBox.send_keys(Keys.ENTER)

#창 위치변경
driver.switch_to.window(driver.window_handles[1]) 

#네이버 뉴스 링크는 표준화가 되어있음
f = open("urllist.txt", "wt") # wt write text 쓰는파일 오픈

for iPages in range(3):
    aList = driver.find_elements_by_xpath("//a")
    for a in aList:
        url = a.get_attribute("href") #"href"가 포함된 부분 추출
        if url.startswith("https://news.naver.com/main/read.nhn"):
            print(url)
            f.write(url)
            f.write('\n') #줄바꿈 기호
    nextButton=driver.find_elements_by_xpath("//div[@id='main_pack']/div/div/a[@class='next']")
    if len(nextButton)==0:
        break
    nextButton[0].click()
f.close()

f = open("urllist.txt", "rt") #readint text 읽기
f2 = open("articleTexts.txt", "wt", encoding="utf-8")

while True:
    line = f.readline()
    if not line: break

    url = line.replace('\n', '')
    
    print(url)
    driver.get(url)

    contentsList = driver.find_elements_by_xpath("//div[@id='articleBodyContents']")
    
    if len(contentsList)==0: continue  #뒤에것을 실행하지 않고 넘어가기
    contents = contentsList[0]
    print(contents.text)
    f2.write(contents.text)
    f2.write('\n')

f.close()
f2.close()

#time.sleep(2)
driver.quit()

