from selenium import webdriver
import time
from config import *


browser = webdriver.Chrome("D:\Programming\instagram\chromedriver.exe")
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
browser.get('https://www.instagram.com/anime/')
time.sleep(3)
browser.find_element_by_xpath(
    '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
time.sleep(5)
element = browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{6}", element)
time.sleep(0.8)
browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{4}", element)
time.sleep(0.8)
browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{3}", element)
time.sleep(0.8)
browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{2}", element)
time.sleep(0.8)
pers = []
t = 0.7
num_scrol = 0
count = 1000
for i in range(count // 10):
    print(i)
    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", element)
    # persons=browser.find_elements_by_xpath("//*[@id="f92aa7e9228218"]/div/div/a")
    # // *[ @ id = "f108c0b1fb9c588"] / div / div / a
    # // *[ @ id = "f34171513039be8"] / div / div / a
    time.sleep(t)
for k in range(count):
    persons = browser.find_elements_by_xpath(
        "/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a".format(k))
    for j in range(len(persons)):
        pers.append(str(persons[j].get_attribute('href')))
    time.sleep(t)
# for person in pers:
# browser.get(person)
# time.sleep(5)
# browser.find_element_by_xpath(
#     '//*[@id="react-root"]/section/main/div/header/section/div[2]/div/span/span[1]/button').click()
# time.sleep(1)
file = open("anime.txt", "w")
for person in pers:
    file.write(person)
    file.write("\n")
file.close()

# def main():
#     login(PASS, LOGIN)
#
#
#
# if __name__=='__main__':
#     main()
