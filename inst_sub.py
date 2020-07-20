from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import re


class Subscribe:

    def __init__(self, limit_hour, file_sub, login, passw):
        self.lim = limit_hour
        self.file = file_sub
        self.log = login
        self.passwd = passw

    def find_element(self, element):
        try:
            self.browser.find_element_by_xpath(element)
            existence = 1
        except NoSuchElementException:
            existence = 0
        return existence

    # link_group = input("input link: ")
    # count = int(input("input count person: "))
    # link_person = "https://www.instagram.com/d_n_sl/"

    def login(self):
        self.browser = webdriver.Chrome("D:\Programming\instagram\chromedriver.exe")
        time.sleep(2)
        self.browser.get("https://www.instagram.com/")
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(
            self.log)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(
            self.passwd)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
        time.sleep(3)

    def read_from_file(self):
        file = open(self.file, 'r')
        self.persons = []
        for pers in file:
            self.persons.append(pers)
        return self.persons

    def filter_person(self):
        privat = '//*[@id="react-root"]/section/main/div/div/article/div[1]/div/h2'
        subscribed = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button'
        send_message = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/button'
        post = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span'
        no_person = '//*[@id="react-root"]/section/main/div/p'
        # posts1 = '//*[@id="react-root"]/section/main/div/div[4]/article/div[1]/div[2]/div[1]/div'
        # posts2 = '//*[@id="react-root"]/section/main/div/div[3]/article/div[1]/div[2]/div[1]/div'
        count_pers = 0
        filtered = 0
        self.filtered_persons = []
        for person in self.persons:
            count_pers += 1
            self.browser.get(person)
            time.sleep(1)
            if self.find_element(no_person) == 1:
                print(str(count_pers) + ") Not available")
                # try:
                #     if self.browser.find_element_by_xpath(no_person).text== "The link you followed may be broken, or the page may have been removed. ":
                #         print(str(count_pers) + ") Not available")
                # except NoSuchElementException:
                #     print("/\/\/\/ Error : 1 /\/\/\/")
                continue
            posts = self.browser.find_element_by_xpath(post).text
            posts = re.sub(r'\s', '', posts)
            if int(posts) == 0:
                print(str(count_pers) + ") No posts")
                continue
            if self.find_element(privat) == 1:
                try:
                    if self.browser.find_element_by_xpath(
                            privat).text == "This Account is Private" or "Это закрытый аккаунт":
                        print(str(count_pers) + ") Private")
                        continue
                except StaleElementReferenceException:
                    print("/\/\/\/ Error : 1 /\/\/\/")
            elif self.find_element(subscribed) == 1:
                try:
                    if self.browser.find_element_by_xpath(
                            send_message).text == 'Отправить сообщение' or 'Message':
                        print(str(count_pers) + ") Subscribed")
                except StaleElementReferenceException:
                    print("/\/\/\/ Error : 1 /\/\/\/")
                continue
            else:
                filtered += 1
                self.filtered_persons.append(person)
                print(str(count_pers) + ") Added  " + str(filtered))
            if filtered == self.lim * 24:
                break
        return self.filtered_persons

    def write_filtered(self):
        self.file = open(self.log + '.txt', 'w')
        for i in self.filtered_persons:
            self.file.write(i)
            # self.file.write("\n")
        # self.file.close()

    def del_subed(self):
        # cou = 0
        # for line in self.file:
        #     cou += 1
        #     line==''
        #     if cou == self.counter:
        #         break
        self.file = open(self.log + '.txt', 'r')
        temp = []
        for line in self.file:
            temp.append(line)
        count = 0
        self.file.close()
        self.file = open(self.log + '.txt', 'w')
        for i in temp:
            count += 1
            if count >= self.counter:
                self.file.write(i)
                # self.file.write('\n')
        self.file.close()

    def subs(self):
        self.counter = 0
        self.file = open(self.log + '.txt', 'r')

        for person in self.file:
            self.counter += 1
            self.browser.get(person)
            time.sleep(5)
            stor = '//*[@id="react-root"]/section/main/div/div[3]'
            if self.find_element(stor) == 1:
                self.browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[3]/article/div/div/div[1]/div[1]').click()
            else:
                self.browser.find_element_by_xpath(
                    '//*[@id="react-root"]/section/main/div/div[2]/article/div/div/div[1]/div[1]').click()
            time.sleep(3)
            self.browser.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/article/header/div[2]/div[1]/div[2]/button').click()
            self.browser.find_element_by_xpath(
                '/html/body/div[4]/div[2]/div/article/div[3]/section[1]/span[1]/button').click()
            time.sleep(2)
            if self.counter == self.lim:
                self.del_subed()
                self.browser.close()
                time.sleep(30)
                self.login()
                # time.sleep(3600)


url = input('enter url: ')
choise = int(input("To choose Zayka enter 1: \nTo choose Blank enter 2: \nTo choose Drop enter 3:"))
crush = int(input('Restart after crush? '))
number_of_users = int(input('Enter amount of users: '))
if choise == 1:
    yourzayka = Subscribe(number_of_users, url, '__yourzayka', '55555dan')
    if crush == 1:
        yourzayka.subs()
    elif crush == 0:
        yourzayka.login()
        yourzayka.read_from_file()
        yourzayka.filter_person()
        yourzayka.write_filtered()
        yourzayka.subs()

elif choise == 2:
    blank = Subscribe(number_of_users, url, '_._.b.l.a.n.k.__', '55555dan')
    if crush == 1:
        blank.subs()
    elif crush == 0:
        blank.login()
        blank.read_from_file()
        blank.filter_person()
        blank.write_filtered()
        blank.subs()

elif choise == 3:
    drop = Subscribe(number_of_users, url, '____drop1', 'Yez7k5D7')
    if crush == 1:
        drop.subs()
    elif crush == 0:
        drop.login()
        drop.read_from_file()
        drop.filter_person()
        drop.write_filtered()
        drop.subs()
