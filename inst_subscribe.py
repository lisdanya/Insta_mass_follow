from selenium import webdriver
import time
from config import *
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import re

browser = webdriver.Chrome("D:\Programming\instagram\chromedriver.exe")


def find_element(element):
    try:
        browser.find_element_by_xpath(element)
        existence = 1
    except NoSuchElementException:
        existence = 0
    return existence


# link_group = input("input link: ")
# count = int(input("input count person: "))
# link_person = "https://www.instagram.com/d_n_sl/"

def login(PASS, LOGIN):
    browser.get("https://www.instagram.com/")
    browser.get("https://www.instagram.com/accounts/login/")
    time.sleep(3)
    browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(
        LOGIN)
    browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(
        PASS)
    browser.find_element_by_xpath(
        '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
    time.sleep(3)


def read_from_file(path):
    file = open(path, 'r')
    persons = []
    for pers in file:
        persons.append(pers)
    return persons


def filter_person(persons):
    privat = '//*[@id="react-root"]/section/main/div/div/article/div[1]/div/h2'
    subscribed = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button'
    send_message = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/button'
    post = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span'
    # posts1 = '//*[@id="react-root"]/section/main/div/div[4]/article/div[1]/div[2]/div[1]/div'
    # posts2 = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div[2]/div[1]/div'
    count_pers = 0
    filtered = 0
    filtered_persons = []
    for person in persons:
        count_pers += 1
        browser.get(person)
        time.sleep(2)
        time.sleep(3)
        posts = browser.find_element_by_xpath(post).text
        posts = re.sub(r'\s', '', posts)
        if int(posts) == 0:
            # if (browser.find_element_by_xpath(
            #         posts1).text == 'Публикаций пока нет' or 'No Posts Yet') or (
            #         browser.find_element_by_xpath(
            #             posts2).text == 'Публикаций пока нет' or 'No Posts Yet'):
            print(str(count_pers) + ") No posts")
            continue
        if filtered == 10:
            break
        if find_element(privat) == 1:
            try:
                if browser.find_element_by_xpath(
                        privat).text == "This Account is Private" or "Это закрытый аккаунт":
                    print(str(count_pers) + ") Private")
                    continue
            except StaleElementReferenceException:
                print("/\/\/\/ Error : 1 /\/\/\/")
        elif find_element(subscribed) == 1:
            try:
                if browser.find_element_by_xpath(
                        send_message).text == 'Отправить сообщение' or 'Message':
                    print(str(count_pers) + ") Subscribed")
            except  StaleElementReferenceException:
                print("/\/\/\/ Error : 1 /\/\/\/")
            continue
        else:
            filtered += 1
            filtered_persons.append(person)
            print(str(count_pers) + ") Added")
    return filtered_persons


def subs(filtered_persons):
    counter=0
    for person in filtered_persons:
        counter+=1
        browser.get(person)
        time.sleep(2)
        stor = '//*[@id="react-root"]/section/main/div/div[3]'
        if find_element(stor) == 1:
            browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div[3]/article/div/div/div[1]/div[1]').click()
        else:
            browser.find_element_by_xpath(
                '//*[@id="react-root"]/section/main/div/div[2]/article/div/div/div[1]/div[1]').click()
        time.sleep(2)
        browser.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
        browser.find_element_by_xpath(
            '/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()
        time.sleep(1)
        if counter==30:
            break


def main():
    login(PASS, LOGIN)
    while True:
        subs(filter_person(read_from_file(path='D:\Programming\instagram\\anime_public100.txt')))
        time.sleep(3600)



if __name__ == '__main__':
    main()
