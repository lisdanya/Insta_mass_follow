from selenium import webdriver
import time


class Unfollow:

    def __init__(self, limit_hour, file_unsub, login, passw):
        self.lim = limit_hour
        self.file_parse = file_unsub
        self.log = login
        self.passwd = passw
        self.counter = 0
        self.insta = "https://www.instagram.com/"
        self.insta_log = "https://www.instagram.com/accounts/login/"
        self.persons = []

        self.t_log = 3
        self.t_unsub = 2

    def login(self):
        self.browser = webdriver.Chrome("D:\Programming\instagram\chromedriver.exe")
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
                time.sleep(20)
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

file_unsub = input('enter parsed file with subs: ')
choise = int(input(
    "To choose Zayka enter 1: \nTo choose Blank enter 2: \nTo choose Drop enter 3: \nTo choose your account enter 4: "))
number_of_users = int(input('Enter amount of users per hour: '))
error = "/\/\/\/ Error : 1 /\/\/\/"
passw = ''
login = ''
if choise == 1:
    login = '__yourzayka'
    passw = '55555dan'
elif choise == 2:
    login = '_._.b.l.a.n.k.__'
    passw = '55555dan'
elif choise == 3:
    login = '____drop1'
    passw = 'Yez7k5D7'
elif choise == 4:
    login = input('Enter login: ')
    passw = input('Enter password: ')
else:
    print(error)
account = Unfollow(number_of_users, file_unsub, login, passw)
account.login()
account.read_from_file()
account.unsub()

