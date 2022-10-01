from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from data import username, password
import time
import random
from selenium.common.exceptions import NoSuchElementException
import requests
import os


class InstagramBot():
    """Instagram Bot """

    def __init__(self, username, password):

        self.username = username
        self.password = password
        self.browser = webdriver.Chrome("../chromedriver/chromedriver")

    # Browser close method
    def close_browser(self):

        self.browser.close()
        self.browser.quit()

    # login method
    def login(self):

        browser = self.browser
        browser.get('https://www.instagram.com')
        time.sleep(random.randrange(3, 5))

        username_input = browser.find_element(By.NAME, 'username')
        username_input.clear()
        username_input.send_keys(username)

        time.sleep(2)

        password_input = browser.find_element(By.NAME, 'password')
        password_input.clear()
        password_input.send_keys(password)

        password_input.send_keys(Keys.ENTER)
        time.sleep(10)

    # method of checking whether an element is on the page by xpath
    def xpath_exists(self, url):

        browser = self.browser
        try:
            browser.find_element(By.XPATH, url)
            exist = True
        except NoSuchElementException:
            exist = False
            return exist

    # the method collects threads on all user posts
    def get_all_posts_urls(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print("Такого Користувача не існує, проверьте URL")
            self.close_browser()
        else:
            print("Користувач знайдено, ставим лайки!")
            time.sleep(2)

            posts_count = int(browser.find_element(By.XPATH,
                "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[1]/div/span").text.replace(",",""))
            if posts_count>50:
                posts_count=50
            loops_count = int(posts_count / 12)
            print(loops_count)

            posts_urls = []
            for i in range(0, loops_count):
                hrefs = browser.find_elements(By.TAG_NAME,'a')
                hrefs = [item.get_attribute('href') for item in hrefs if "/p/" in item.get_attribute('href')]

                for href in hrefs:
                    posts_urls.append(href)

                browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.randrange(2, 4))
                print(f"Ітерация #{i}")

            file_name = userpage.split("/")[-2]

            with open(f'{file_name}.txt', 'a') as file:
                for post_url in posts_urls:
                    file.write(post_url + "\n")

            set_posts_urls = set(posts_urls)
            set_posts_urls = list(set_posts_urls)

            with open(f'{file_name}_set.txt', 'a') as file:
                for post_url in set_posts_urls:
                    file.write(post_url + '\n')

    # the method puts likes according to the strength of the user
    def put_many_likes(self, userpage):

        browser = self.browser
        self.get_all_posts_urls(userpage)
        file_name = userpage.split("/")[-2]
        time.sleep(4)
        browser.get(userpage)
        time.sleep(4)

        with open(f'{file_name}_set.txt') as file:
            urls_list = file.readlines()

            for post_url in urls_list[0:4]:
                try:

                    browser.get(post_url)
                    time.sleep(2)

                    like_button = "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button/div[2]"
                    browser.find_element(By.XPATH,like_button).click()
                        # time.sleep(random.randrange(80, 100))
                    time.sleep(2)
                    print(f"Лайк на пост: {post_url} успішно поставлений!")

                except:
                    print(f"Лайк на пост: {post_url} Вже Стоїть!")
                    continue

    # method for account parsing, collection of forces on Readers' profiles
    def get_all_followers(self, userpage):

        browser = self.browser
        browser.get(userpage)
        time.sleep(4)
        file_name = userpage.split("/")[-2]

        # Creat file with Followers
        if os.path.exists(f"{file_name}"):
            print(f"Папка {file_name} уже существует!")
        else:
            print(f"Создаём папку пользователя {file_name}.")
            os.mkdir(file_name)

        wrong_userpage = "/html/body/div[1]/section/main/div/h2"
        if self.xpath_exists(wrong_userpage):
            print(f"Пользователя {file_name} не існує, перевірте URL")
            self.close_browser()
        else:
            print(f"Пользователь {file_name} успешно знайдений, начинаем скачувати силки на Читачів!")
            time.sleep(2)

            followers_button = browser.find_element(By.XPATH,
                                                    "/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div/header/section/ul/li[2]/a/div")
            followers_count = followers_button.text.replace(",", "")
            followers_count = int(followers_count.split(' ')[0])
            print(f"Кількість читачів: {followers_count}")
            time.sleep(2)

            loops_count = int(followers_count / 12)
            print(f"Число Ітераций: {loops_count}")
            time.sleep(4)

            followers_button.click()
            time.sleep(4)

            followers_ul = browser.find_element(By.XPATH,
                                                "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]")

            try:
                followers_urls = []
                for i in range(1, loops_count + 1):
                    browser.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", followers_ul)
                    time.sleep(random.randrange(2, 4))
                    print(f"Ітерация #{i}")
                print(followers_ul)
                all_urls_divv = browser.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[1]/div")
                all_urls_divvv = all_urls_divv.find_elements(By.TAG_NAME,"a")

                for url in all_urls_divvv:
                    url = url.get_attribute("href")
                    followers_urls.append(url)

                set_fillowers_urls = set(followers_urls)
                set_fillowers_urls = list(set_fillowers_urls)
                # saving all Followers without repetition
                with open(f"{file_name}/{file_name}_set.txt", "a") as text_file:
                    count_folowers=0
                    for folower_url in set_fillowers_urls:
                        text_file.write(folower_url + "\n")
                        count_folowers+=1
                        print("Усі Акаунти збережені !")
                    print("Читачів",count_folowers)
                # reading file with Followers
                with open(f"{file_name}/{file_name}_set.txt", "r") as text_file:
                    file_followers = text_file.readlines()
                    # We give likes to every follower
                    for likes_follow in file_followers:
                        self.put_many_likes(likes_follow)
                        continue

                print(file_followers)


            except Exception as ex:
                print(ex)
                self.close_browser()

        self.close_browser()







my_bot = InstagramBot(username, password)
my_bot.login()
my_bot.get_all_followers("https://www.instagram.com")# Account link that you want to share with Readers and share photos with them