from selenium import webdriver
import time


class Parse:
    def __init__(self, LOGIN, PASS, quantity):
        self.browser = webdriver.Chrome("D:\Programming\instagram\chromedriver.exe")
        self.pers = []
        self.LOGIN = LOGIN
        self.PASS = PASS
        self.quantity = quantity

    def logging(self):

        self.browser.get("https://www.instagram.com/")
        self.browser.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input').send_keys(
            self.LOGIN)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]/div/label/input').send_keys(
            self.PASS)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[4]').click()
        time.sleep(3)

    def scroll_prep(self):
        self.browser.get('https://www.instagram.com/{}/'.format(self.LOGIN))
        time.sleep(3)
        self.browser.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/div/header/section/ul/li[2]/a').click()
        time.sleep(5)
        self.element = self.browser.find_element_by_xpath('/html/body/div[4]/div/div/div[2]')
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{6}", self.element)
        time.sleep(0.8)
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{4}", self.element)
        time.sleep(0.8)
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{3}", self.element)
        time.sleep(0.8)
        self.browser.execute_script(f"arguments[0].scrollTop = arguments[0].scrollHeight/{2}", self.element)
        time.sleep(0.8)

    def scroll(self):
        t = 0.7
        for i in range(self.quantity // 10):
            print(i)
            self.browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", self.element)
            time.sleep(t)
        for k in range(self.quantity):
            persons = self.browser.find_elements_by_xpath(
                "/html/body/div[4]/div/div/div[2]/ul/div/li[{}]/div/div[1]/div[2]/div[1]/a".format(k))
            for j in range(len(persons)):
                self.pers.append(str(persons[j].get_attribute('href')))
            time.sleep(t)

    def write_file(self):
        file = open("anime_public100.txt", "w")
        for person in self.pers:
            file.write(person)
            file.write("\n")
        file.close()


data = Parse("_._.b.l.a.n.k.__", "55555dan", 70)
data.logging()
data.scroll_prep()
data.scroll()
data.write_file()
