from selenium import webdriver
from urllib.request import urlopen
from urllib.parse import quote_plus
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import datetime
import csv
import urllib.parse
import urllib.request

# 인스타그램 태그를 입력하여 해당 태그에 대한 검색 결과 웹 페이지를 띄움.
baseUrl = 'https://www.instagram.com/'
plusUrl = input('검색할 user_id를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)
driver = webdriver.Chrome() # 크롬 웹 드라이버
driver.get(url) # 크롬에서 url를 가져옴

driver.implicitly_wait(3) # 페이지가 로딩될 때 까지 암묵적으로 기다린다.
# 로그인 버튼을 누르고 ID 와 PASSWORD를 입력한 후 로그인 버튼을 다시 누른다.
driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click() 
driver.find_element_by_name('username').send_keys("dlehgus5656@naver.com")
driver.find_element_by_name('password').send_keys("akdntm1212!")
driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
driver.find_element_by_class_name('_9AhH0').click()

while True: 
    time.sleep(1)

    overlap_photo = driver.find_elements_by_class_name("Yi5aA")
    
    if(len(overlap_photo) == 0):
        try:
            photo = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/div[1]/img').get_attribute('src')
            photo_time = driver.find_element_by_class_name('_1o9PC').get_attribute('datetime')
            photo_time = photo_time.split('.')
            photo_time = photo_time[0].replace('-','_').replace('T','_').replace(':','_')
            urllib.request.urlretrieve(photo, photo_time + ".jpg")
        except NoSuchElementException:
            photo = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/img').get_attribute('src')
            photo_time = driver.find_element_by_class_name('_1o9PC').get_attribute('datetime')
            photo_time = photo_time.split('.')
            photo_time = photo_time[0].replace('-','_').replace('T','_').replace(':','_')
            urllib.request.urlretrieve(photo, photo_time + ".jpg")

    else:
        for n in range(len(overlap_photo)):
            try:
                video = driver.find_element_by_class_name('PyenC')
                break
            except NoSuchElementException:
                temp = n + 1 
                if(temp != len(overlap_photo)): # 묶음사진 중 마지막 사진 전 사진들의 xpath
                    photo = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/div/ul/li["+str(temp)+"]/div/div/div/div/div[1]/div[1]/img").get_attribute('src')
                else: # 묶음사진 중 마지막 사진의 xpath
                    photo = driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/div/ul/li["+str(temp)+"]/div/div/div/div/div[1]/img").get_attribute('src')
                photo_time = driver.find_element_by_class_name('_1o9PC').get_attribute('datetime')
                photo_time = photo_time.split('.')
                photo_time = photo_time[0].replace('-','_').replace('T','_').replace(':','_')
                urllib.request.urlretrieve(photo, photo_time + '_' +str(temp)+ '_' + '.jpg')

                try:
                    driver.find_element_by_class_name('coreSpriteRightChevron').click()
                except NoSuchElementException:
                    break

    try:
        nextbtn = driver.find_element_by_class_name('_65Bje.coreSpriteRightPaginationArrow')
        if(nextbtn.text == "다음"):
            nextbtn.click()
    except:
        break

driver.close()