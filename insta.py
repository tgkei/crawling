# -*- coding: utf-8 -*-
from selenium import webdriver
from urllib.request import urlretrieve
from urllib.parse import quote_plus
from selenium.common.exceptions import NoSuchElementException as NOERROR

import platform
import pickle
import os
from pathlib import Path
import time
from datetime import datetime

_BASE_URL = "https://www.instagram.com/"
_USER_ID = "jh.cpp"
_url = _BASE_URL + quote_plus(_USER_ID)

_SRC_DIR = os.getcwd() + "/resources"
_IMG_DIR = _SRC_DIR + "/img"

data = {}

_xpath_base = {
    "one": "/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/",
    "many": "/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/div/ul/li[{}]/div/div/div/div/div[1]/",
}


def set_driver():
    _DRIVER_PATH = Path(os.getcwd())
    chromedriver = "chromedriver"
    if platform.system() == "Windows":
        chromedriver += ".exe"
    return webdriver.Chrome(_DRIVER_PATH / chromedriver)


def to_main_page(driver):
    driver.get(_url)
    driver.implicitly_wait(3)


def login(driver):
    driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
    ).click()
    driver.find_element_by_name("username").send_keys("dlehgus5656@naver.com")
    driver.find_element_by_name("password").send_keys("akdntm1212!")
    driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]'
    ).click()


def click_first_image(driver):
    driver.find_element_by_class_name("_9AhH0").click()


def crawl(driver):
    while True:  # should be changed later. while img_exits
        time.sleep(1)

        _overlap_photos = driver.find_elements_by_class_name("Yi5aA")

        if not _overlap_photos:
            img_name = _save_image(driver)
        else:
            img_name = _save_images(driver, len(_overlap_photos))

        _hashtags = _find_hashtag(driver)

        if isinstance(img_name, list):
            for img in img_name:
                data[img] = _hashtags
        else:
            data[img_name] = _hashtags
        try:
            nextbtn = driver.find_element_by_class_name(
                "_65Bje.coreSpriteRightPaginationArrow"
            )
            if nextbtn.text in ("다음", "Next"):
                nextbtn.click()
        except:
            break
    print("crawler successfully done")
    driver.close()


def _save_image(driver):
    extensions = ["div[1]/img", "img"]
    for ext in extensions:
        xpath = _xpath_base["one"] + ext
        try:
            photo = driver.find_element_by_xpath(xpath).get_attribute("src")
            break
        except NOERROR:
            continue
    return _save(photo)


def _save_images(driver, num_images):
    extensions = ["div[1]/img", "img"]
    _img_name = []
    for n in range(num_images):
        try:
            video = driver.find_element_by_class_name("PyenC")
            continue
        except NOERROR:
            for ext in extensions:
                xpath = _xpath_base["many"] + ext
                try:
                    photo = driver.find_element_by_xpath(
                        xpath.format(str(n + 1))
                    ).get_attribute("src")
                    break
                except NOERROR:
                    continue

            _img_name.append(_save(photo))

            try:
                driver.find_element_by_class_name("coreSpriteRightChevron").click()
            except NOERROR:
                break
    return _img_name


def _save(photo):
    _cur_time = str(datetime.now())[:-4] + ".jpg"

    try:
        urlretrieve(photo, _IMG_DIR + "/" + _cur_time)
    except:
        print("name:", _cur_time)
        print(photo)
    return _cur_time


def _find_hashtag(driver):
    try:
        driver.find_element_by_class_name("EizgU").click()
    except NOERROR:
        print("No comments")
    try:
        matched_elements = driver.find_elements_by_class_name("xil3i")
        hashtags = []

        for matched_element in matched_elements:
            hashtag = matched_element.text
            hashtags.append(hashtag)
        return hashtags

    except NOERROR:
        print("No hashtag in this post")


if __name__ == "__main__":
    driver = set_driver()
    to_main_page(driver)
    login(driver)
    click_first_image(driver)
    crawl(driver)

    with open(_SRC_DIR + "/data.pickle", "wb") as f:
        pickle.dump(data, f)
