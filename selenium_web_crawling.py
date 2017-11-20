from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.ui as ui
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

textfile = open("data/users.txt", "r", encoding="utf8")
users = textfile.read()
users_list = users.split("\n")
user_dic = {}
for user in users_list:
    user_dic[user.split(",")[0]] = user.split(",")[1]
print(user_dic)

textfile = open("data/sisa.txt", "r", encoding="utf8")
sisa = textfile.read()

textfile = open("data/soccer.txt", "r", encoding="utf8")
soccer = textfile.read()

textfile = open("data/star.txt", "r", encoding="utf8")
star = textfile.read()



driver = webdriver.Chrome('D:\chromedriver\chromedriver.exe')

driver.implicitly_wait(3)
# url에 접근한다.
driver.get('http://bidoolgi.net/#/')

wait = ui.WebDriverWait(driver, 10)
driver.find_element_by_class_name('btn-primary').click()
driver.find_element_by_name('email').send_keys('')
wait
driver.find_element_by_name('password').send_keys('')
driver.find_element_by_id('requireLogin').click()

wait.until(
    EC.text_to_be_present_in_element(
        (By.ID, 'requireLogout'),
        '로그아웃'
    )
)

driver.get('http://bidoolgi.net/main.html#/')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
soldiers = soup.findAll("div", { "class" : "soldierCards" })


for one in soldiers:
    soldier_name = one.find('span', {"class": "thumbnailSoldierName"}).text
    user_categories = user_dic[soldier_name].split("/")
    link = one.find('a', {"class":"writeLetter"})
    driver.find_element_by_xpath('//a[@href="'+link.get("href")+'"]').click()

    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, 'goFriendList'),
            '이전'
        )
    )
    for category in user_categories:
        if category == "시사":
            news = sisa
        elif category == "축구":
            news = soccer
        elif category == "연예":
            news = star

        driver.find_element_by_name("articleTitle").send_keys(news)
        driver.find_element_by_name("articleText").send_keys(news)
        driver.find_element_by_name("articlePassword").send_keys("1111")
        driver.find_element_by_id("sendLetterIcon").click()

        wait.until(EC.alert_is_present())

        alert = driver.switch_to.alert
        alert.accept()
        wait.until(lambda driver: driver.find_element_by_class_name('glyphicon-envelope'))

    driver.find_element_by_id("goFriendList").click()

    wait.until(
        EC.text_to_be_present_in_element(
            (By.ID, 'requireLogout'),
            '로그아웃'
        )
    )