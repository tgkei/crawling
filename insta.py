#-*- coding: utf-8 -*-
from selenium import webdriver
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from selenium.common.exceptions import NoSuchElementException as NOERROR

import pickle
import os
from pathlib import Path
import time
from datetime import datetime

_BASE_URL = 'https://www.instagram.com/'
_USER_ID = "jh.cpp"
_url = _BASE_URL+ quote_plus(_USER_ID)

_SRC_DIR = os.getcwd()+"/resources"
_IMG_DIR = _SRC_DIR+"/img"

data = {}

def set_driver():
    _DRIVER_PATH = Path(os.getcwd())
   
    return webdriver.Chrome(_DRIVER_PATH/"chromedriver")

def to_main_page(driver):
    driver.get(_url)
    driver.implicitly_wait(3) 

def login(driver):
    driver.find_element_by_xpath('//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button').click()
    driver.find_element_by_name('username').send_keys("dlehgus5656@naver.com")
    driver.find_element_by_name('password').send_keys("akdntm1212!")
    driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()

def click_first_image(driver):
    driver.find_element_by_class_name('_9AhH0').click()

def crawl(driver):
    while True: # should be changed later. while img_exits
        time.sleep(0.05)
    
        _overlap_photos = driver.find_elements_by_class_name("Yi5aA")
    
        if not _overlap_photos:
            _save_one_image(driver)
        else:
            _save_images(driver, len(_overlap_photos))
    
        try:
            nextbtn = driver.find_element_by_class_name('_65Bje.coreSpriteRightPaginationArrow')
            if nextbtn.text in ("다음", "Next"):
                nextbtn.click()
        except:
            break
    print("crawler successfully done")
    driver.close()

def _save_one_image(driver): 
    try:
        photo = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/div[1]/img').get_attribute('src')
    except NOERROR:
        photo = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/img').get_attribute('src')
    _save(photo) 

def _save_images(driver, num_images):
    for n in range(num_images):
        try:
            video = driver.find_element_by_class_name('PyenC')
            continue
        except NOERROR: 
            try:
                photo = driver.find_element_by_xpath(f"/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/div/ul/li[{str(n+1)}]/div/div/div/div/div[1]/div[1]/img").get_attribute('src')
            except NOERROR: 
                photo = driver.find_element_by_xpath(f"/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/div/ul/li[{str(n+1)}]/div/div/div/div/div[1]/img").get_attribute('src')
            
            _save(photo)

            try:
                driver.find_element_by_class_name('coreSpriteRightChevron').click()
            except NOERROR:
                break

def _save(photo):
    _cur_time = str(datetime.now())[:-4]+".jpg"

    if photo not in data:
        data[_cur_time] = "tmp"
    
    urlretrieve(photo, _IMG_DIR+"/"+_cur_time)

if __name__=="__main__":
    driver = set_driver()
    to_main_page(driver)
    login(driver)
    click_first_image(driver) 
    crawl(driver)
    with open(_SRC_DIR+"/data.pickle", "wb") as f:
        pickle.dump(data, f)
