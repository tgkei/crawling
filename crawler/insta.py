# -*- coding: utf-8 -*-
"""
crawling instagram
"""
import platform
import pickle
import os
from pathlib import Path
import time
from datetime import datetime

from urllib.request import urlretrieve
from urllib.parse import quote_plus

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException as NOERROR


_BASE_URL = "https://www.instagram.com/"
_USER_ID = "jh.cpp"
_URL = _BASE_URL + quote_plus(_USER_ID)

_SRC_DIR = os.getcwd() + "/resources"
_IMG_DIR = _SRC_DIR + "/img"

# pylint: disable=C0103
data = {}
# pylint: disable=C0103
driver = None

# pylint: disable=line-too-long
_XPATH_BASE = {
    "one": "/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[1]/",
    "many": "/html/body/div[4]/div[2]/div/article/div[1]/div/div/div[2]/div/div/div/div/ul/li[{}]/div/div/div/div/div[1]/",
}


def set_driver():
    """
    set Chromedriver
    """
    global driver  # pylint: disable=W0603
    _driver_path = Path(os.getcwd())
    chromedriver = "chromedriver"
    if platform.system() == "Windows":
        chromedriver += ".exe"
    driver = webdriver.Chrome(_driver_path / chromedriver)


def to_main_page():
    """
    get into user page
    """
    global driver  # pylint: disable=W0603
    driver.get(_URL)
    driver.implicitly_wait(3)


def login():
    """
    login
    """
    global driver  # pylint: disable=W0603
    driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
    ).click()
    driver.find_element_by_name("username").send_keys("dlehgus5656@naver.com")
    driver.find_element_by_name("password").send_keys("akdntm1212!")
    driver.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]'
    ).click()


def click_first_image():
    """
    get into first image
    """
    global driver  # pylint: disable=W0603
    driver.find_element_by_class_name("_9AhH0").click()


def crawl():
    """
    crawl while there is image
    """
    global driver  # pylint: disable=W0603
    while True:  # should be changed later. while img_exits
        time.sleep(1)

        _overlap_photos = driver.find_elements_by_class_name("Yi5aA")

        if not _overlap_photos:
            img_name = _save_image()
        else:
            img_name = _save_images(len(_overlap_photos))

        _hashtags = _find_hashtag()

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
        except:  # pylint: disable=W0702
            break
    print("crawler successfully done")
    driver.close()


def _save_image():
    """
    save image if there is only one image in post
    """
    global driver  # pylint: disable=W0603
    extensions = ["div[1]/img", "img"]
    for ext in extensions:
        xpath = _XPATH_BASE["one"] + ext
        try:
            photo = driver.find_element_by_xpath(xpath).get_attribute("src")
            break
        except NOERROR:
            continue
    return _save(photo)


def _save_images(num_images):
    """
    save images if there are many images in post
    """
    global driver  # pylint: disable=W0603
    extensions = ["div[1]/img", "img"]
    _img_name = []
    for n in range(num_images):
        try:
            driver.find_element_by_class_name("PyenC")
            continue
        except NOERROR:
            for ext in extensions:
                xpath = _XPATH_BASE["many"] + ext
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
    """
    save image with unique name
    _________________________________
    return image name
    """
    _cur_time = str(datetime.now())[:-4] + ".jpg"

    try:
        urlretrieve(photo, _IMG_DIR + "/" + _cur_time)
    except:  # pylint: disable=W0702
        print("name:", _cur_time)
        print(photo)
    return _cur_time


def _find_hashtag():
    """
    crawl hashtag
    """
    global driver  # pylint: disable=W0603
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
    set_driver()
    to_main_page()
    login()
    click_first_image()
    crawl()

    with open(_SRC_DIR + "/data.pickle", "wb") as f:
        pickle.dump(data, f)
