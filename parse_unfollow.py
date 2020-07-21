from selenium import webdriver
import time


class Parse:
    def __init__(self, login, passw, quant):
        self.log = login
        self.passwd = passw
        self.browser = webdriver.Chrome("D:\Programming\instagram\chromedriver.exe")
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
        file = open(r"D:\Programming\instagram\unsub\{}_unfollow.txt".format(self.log), "w")
        for person in self.pers:
            file.write(person)
            file.write("\n")
        file.close()
        self.browser.close()
        print('/\/\/\/\/\/\/\/\\')


yourzayka = Parse('_._.b.l.a.n.k.__', '55555dan', 100)
yourzayka.login()
yourzayka.scroll_prep()
yourzayka.scroll()
yourzayka.writing()
