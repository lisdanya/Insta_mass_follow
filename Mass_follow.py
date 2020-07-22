from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from tkinter import filedialog as fd
from tkinter import Tk
import re


class Parse_follow:
    def __init__(self, LOGIN, PASS, link, quantity):
        self.root = Tk()
        self.webdriver_path = fd.askopenfilename()
        self.file_parse_path = fd.askdirectory()
        self.root.destroy()
        self.browser = webdriver.Chrome(self.webdriver_path)
        self.pers = []
        self.link = link
        self.tag = link.split('/')[3]
        self.LOGIN = LOGIN
        self.PASS = PASS
        self.quantity = quantity
        self.t_scroll = 0.7
        self.t_log = 3

    def logging(self):

        self.browser.get("https://www.instagram.com/")
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(self.t_log)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(
            self.LOGIN)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(
            self.PASS)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
        time.sleep(self.t_log)

    def scroll_prep(self):
        self.browser.get(self.link)
        time.sleep(self.t_log)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        time.sleep(self.t_log)
        self.element = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{6}",
                                    self.element)
        time.sleep(self.t_scroll)
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{4}",
                                    self.element)
        time.sleep(self.t_scroll)
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{3}",
                                    self.element)
        time.sleep(self.t_scroll)
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{2}",
                                    self.element)
        time.sleep(self.t_scroll)

    def scroll(self):
        for i in range(self.quantity // 10):
            print(i)
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",
                                        self.element)
            time.sleep(self.t_scroll)
        for k in range(self.quantity):
            persons = self.browser.find_elements_by_xpath(
                "/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a".format(
                    k))
            for j in range(len(persons)):
                self.pers.append(str(persons[j].get_attribute('href')))

    def write_file(self):
        file = open(r"{0}\{1}.txt".format(self.file_parse_path, self.tag), "w")
        for person in self.pers:
            file.write(person)
            file.write("\n")
        self.browser.close()
        file.close()
        print('/\/\/\/\/\/\/\/\\')


class Subscribe:
    def __init__(self, limit_hour, login, passw):
        self.root = Tk()
        self.webdriver_path = fd.askopenfilename()
        self.file_sub_path = fd.askopenfilename()
        self.root.destroy()
        self.lim = limit_hour
        self.file_parse = self.file_sub_path
        self.log = login
        self.passwd = passw
        self.counter = 0
        self.persons = []

    def find_element(self, element):
        try:
            self.browser.find_element_by_xpath(element)
            existence = 1
        except NoSuchElementException:
            existence = 0
        return existence

    def login(self):
        self.browser = webdriver.Chrome(self.webdriver_path)
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
        file = open(self.file_parse, 'r')
        for pers in file:
            self.persons.append(pers)
        return self.persons

    def filter_person(self):
        privat = '//*[@id="react-root"]/section/main/div/div/article/div[1]/div/h2'
        subscribed = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button'
        send_message = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[1]/div/button'
        post = '//*[@id="react-root"]/section/main/div/header/section/ul/li[1]/span/span'
        no_person = '//*[@id="react-root"]/section/main/div/p'
        count_pers = 0
        filtered = 0
        for person in self.persons:
            count_pers += 1
            self.browser.get(person)
            time.sleep(1)
            if self.find_element(no_person) == 1:
                print(str(count_pers) + ") Not available")
                self.del_subed()
                continue
            posts = self.browser.find_element_by_xpath(post).text
            posts = re.sub(r'\s', '', posts)
            if int(posts) == 0:
                print(str(count_pers) + ") No posts")
                self.del_subed()
                continue
            if self.find_element(privat) == 1:
                try:
                    if self.browser.find_element_by_xpath(
                            privat).text == "This Account is Private" or "Это закрытый аккаунт":
                        print(str(count_pers) + ") Private")
                        self.del_subed()
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
                self.del_subed()
                continue
            else:
                filtered += 1
                self.subs()
                self.del_subed()
                print(str(count_pers) + ") Added  " + str(filtered))
            if filtered == self.lim * 24:
                break

    def del_subed(self):
        self.file = open(self.file_parse, 'r')
        temp = []
        for line in self.file:
            temp.append(line)
        self.file.close()
        count = 0
        self.file = open(self.file_parse, 'w')
        for url in temp:
            count += 1
            if count > 1:
                self.file.write(url)
        self.file.close()

    def subs(self):
        time.sleep(2)
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
        self.counter += 1
        if self.counter % self.lim == 0:
            self.browser.close()
            time.sleep(3600)
            self.login()


class Parse_unfollow:
    def __init__(self, login, passw, quant):
        self.root = Tk()
        self.webdriver_path = fd.askopenfilename()
        self.file_parse_path = fd.askdirectory()
        self.root.destroy()
        self.browser = webdriver.Chrome(self.webdriver_path)
        self.log = login
        self.passwd = passw
        self.t_min = 1
        self.t_log = 3
        self.t_scroll = 0.8
        self.quantity = quant
        self.pers = []
        self.insta = "https://www.instagram.com/"
        self.insta_log = "https://www.instagram.com/accounts/login/"

    def login(self):
        self.browser.get(self.insta)
        self.browser.get(self.insta_log)
        time.sleep(self.t_log)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(
            self.log)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(
            self.passwd)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
        time.sleep(self.t_log)

    def scroll_prep(self):
        self.browser.get("https://www.instagram.com/{}/".format(self.log))
        time.sleep(self.t_log)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[3]/a').click()
        time.sleep(self.t_log)
        self.element = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{6}",
                                    self.element)
        time.sleep(self.t_scroll)
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{4}",
                                    self.element)
        time.sleep(self.t_scroll)
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{3}",
                                    self.element)
        time.sleep(self.t_scroll)
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{2}",
                                    self.element)
        time.sleep(self.t_scroll)

    def scroll(self):
        for i in range(self.quantity // 10):
            print(i)
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight",
                                        self.element)
            time.sleep(self.t_scroll)
        for k in range(self.quantity):
            self.persons = self.browser.find_elements_by_xpath(
                "/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a".format(
                    k))
            for j in range(len(self.persons)):
                self.pers.append(str(self.persons[j].get_attribute('href')))

    def writing(self):
        file = open(r"{0}\{1}_unfollow.txt".format(self.file_parse_path,self.log), "w")
        for person in self.pers:
            file.write(person)
            file.write("\n")
        file.close()
        self.browser.close()
        print('/\/\/\/\/\/\/\/\\')


class Unfollow:
    def __init__(self, limit_hour, login, passw):
        self.root = Tk()
        self.webdriver_path = fd.askopenfilename()
        self.file_unsub_path = fd.askopenfilename()
        self.root.destroy()
        self.lim = limit_hour
        self.file_parse = self.file_unsub_path
        self.log = login
        self.passwd = passw
        self.counter = 0
        self.insta = "https://www.instagram.com/"
        self.insta_log = "https://www.instagram.com/accounts/login/"
        self.persons = []

        self.t_log = 3
        self.t_unsub = 2

    def login(self):
        self.browser = webdriver.Chrome(self.webdriver_path)
        self.browser.get(self.insta)
        self.browser.get(self.insta_log)
        time.sleep(self.t_log)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(
            self.log)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(
            self.passwd)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
        time.sleep(self.t_log)

    def read_from_file(self):
        file = open(self.file_parse, 'r')
        for pers in file:
            self.persons.append(pers)
        return self.persons

    def unsub(self):
        button = '//*[@id="react-root"]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button'
        unfollow = '/html/body/div[4]/div/div/div/div[3]/button[1]'
        for person in self.persons:
            self.counter += 1
            self.browser.get(person)
            time.sleep(1)
            self.browser.find_element_by_xpath(button).click()
            time.sleep(self.t_unsub)
            self.browser.find_element_by_xpath(unfollow).click()
            time.sleep(self.t_unsub)
            self.del_unsubed()
            if self.counter % self.lim == 0:
                self.browser.close()
                time.sleep(3500)
                self.login()

    def del_unsubed(self):
        self.file = open(self.file_parse, 'r')
        temp = []
        for line in self.file:
            temp.append(line)
        self.file.close()
        count = 0
        self.file = open(self.file_parse, 'w')
        for url in temp:
            count += 1
            if count > 1:
                self.file.write(url)
        self.file.close()


choise = int(input(
    "To choose subscribers enter 1: \nTo choose parse subscribe enter 2: \n"
    "To choose unfollow enter 3: \nTo choose parse unfollow enter 4: \n\n"))

error = "/\/\/\/ Error : 1 /\/\/\/"

login = input('Enter login: ')
passw = input('Enter password: ')


if choise == 1:
    number_of_users = int(input('Enter amount of users per hour: '))
    print("Choose file webdriver path\n")
    print("Choose file sub path\n")
    sub = Subscribe(number_of_users, login, passw)
    sub.login()
    sub.read_from_file()
    sub.filter_person()
elif choise == 2:
    number_of_parse_users = int(input('Enter amount of users to parse: '))
    link = input('Enter link on public: ')
    print("Choose file webdriver path\n")
    print("Choose folder sub path\n")
    parse_follow = Parse_follow(login, passw, link, number_of_parse_users)
    parse_follow.logging()
    parse_follow.scroll_prep()
    parse_follow.scroll()
    parse_follow.write_file()
elif choise == 3:
    number_of_users = int(input('Enter amount of users per hour: '))
    print("Choose file webdriver path\n")
    print("Choose file unsub path\n")
    unfollow = Unfollow(number_of_users, login, passw)
    unfollow.login()
    unfollow.read_from_file()
    unfollow.unsub()
elif choise == 4:
    number_of_parse_users = int(input('Enter amount of users to parse: '))
    print("Choose file webdriver path\n")
    print("Choose folser unsub path\n")
    parse_unfollow = Parse_unfollow(login, passw, number_of_parse_users)
    parse_unfollow.login()
    parse_unfollow.scroll_prep()
    parse_unfollow.scroll()
    parse_unfollow.writing()
