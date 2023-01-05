from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from threading import Lock, Thread
from setting import *


def wait(func):
    """
    一个用于实现等待的修饰器
    :param func: 代入函数
    :return: func
    """

    def wait_func(*args, **kwargs):
        time.sleep(SLEEP_TIME)
        func(*args, **kwargs)
        time.sleep(SLEEP_TIME)

    return wait_func


class XueXiTong:
    lock = Lock()

    @staticmethod
    def get_no_ui_browser():
        """
        获得一个无界面浏览器对象
        :return: Chrome
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        path = r"C:\Users\17627\AppData\Local\Google\Chrome\Application\chrome.exe"

        chrome_options.binary_location = path

        browser = webdriver.Chrome(chrome_options=chrome_options)

        return browser

    @staticmethod
    def get_browser():
        """
        获得一个有界面浏览器对象（用于展示或者调试）
        :return:  Chrome
        """
        return webdriver.Chrome()

    @wait
    def sion_in(self):
        """
        用于实现登录
        :return: None
        """
        self.browser.get(SION_IN_URL)

        # 寻找登录的信息框
        self.input_user = self.browser.find_element(By.XPATH, XPATH_SION_IN_URL)
        self.input_password = self.browser.find_element(By.XPATH, XPATH_SION_IN_PASSWORD)
        self.sion_in_button = self.browser.find_element(By.XPATH, XPATH_SION_IN_BUTTON)

        # 填入基本信息
        self.input_user.send_keys(USER)
        self.input_password.send_keys(PASSWORD)
        time.sleep(1)  # 填入信息后再等待一下
        self.sion_in_button.click()
        print("登录成功")

    def switch_to(self, window_num=None):
        """
        用于切换界面
        :return: None
        """
        if window_num is None:
            self.browser.switch_to.window(self.browser.window_handles[-1])  # 默认跳转到最新界面
        else:
            self.browser.switch_to.window(self.browser.window_handles[window_num])  # 跳转到指定界面

        # print(self.browser.current_url)

    def open_curriculum(self, url):
        """
        用于打开的课程
        :param url: 课程链接
        :return: None
        """

        js = f'window.open("{url}");'
        self.browser.execute_script(js)

        self.switch_to()

        print(self.browser.title)

        n = len(self.browser.find_elements(By.XPATH, '//div[@class="catalog_title"]'))

        for i in range(n):
            # 存在元素的过时引用，所以需要每一次重新作出选择
            button = self.browser.find_elements(By.XPATH, XPATH_CURRICULUM)[i]
            title = self.browser.find_elements(By.XPATH, XPATH_TITLE)[i].get_attribute('title')

            self.browser.execute_script("arguments[0].click();", button)
            print(f"页面《{title}》已完成，句柄：", self.browser.current_url)

            # time.sleep(1)
            self.browser.back()
            self.browser.back()
            time.sleep(0.5)

    def open_curriculum_multithreading(self, url):
        """
        用于打开的课程，多线程实现
        :param url: 课程链接
        :return: None
        """
        self.lock.acquire()  # 加锁

        js = f'window.open("{url}");'
        self.browser.execute_script(js)
        window_num = len(self.browser.window_handles) - 1

        self.switch_to()

        print(self.browser.title)

        n = len(self.browser.find_elements(By.XPATH, '//div[@class="catalog_title"]'))
        # print("当前句柄", self.browser.window_handles)

        self.lock.release()  # 解锁

        for i in range(n):
            self.lock.acquire()  # 加锁

            self.switch_to(window_num)  # 先跳转到自己的界面

            # 存在元素的过时引用，所以需要每一次重新作出选择
            button = self.browser.find_elements(By.XPATH, XPATH_CURRICULUM)[i]
            title = self.browser.find_elements(By.XPATH, XPATH_TITLE)[i].get_attribute('title')

            self.browser.execute_script("arguments[0].click();", button)

            self.browser.back()
            self.browser.back()

            self.lock.release()  # 解锁

            print(f"页面《{title}》已完成，句柄：", self.browser.current_url)
            time.sleep(0.5)

    def __init__(self, is_multithreading=True):

        self.browser = self.get_browser()  # 获取一个浏览器对象

        self.browser.implicitly_wait(IMPLICITLY_WAIT)  # 设置隐式等待的时间
        self.sion_in()  # 登录

        # 当作为单线程使用
        if is_multithreading:
            for curriculum in CURRICULUMS:
                self.open_curriculum(curriculum)

        # 作为多线程展示
        else:
            children = []
            for curriculum in CURRICULUMS:
                children.append(Thread(target=self.open_curriculum_multithreading, args=(curriculum,)))
                children[-1].start()
            flag = True

            # 动态判断是否已经全部结束了
            while flag:
                time.sleep(1)  # 每隔1秒就去判断一下线程们的存活情况
                flag = False
                for child in children:
                    flag = True if child.is_alive() else flag

    def __del__(self):
        self.browser.quit()


if __name__ == '__main__':
    XueXiTong()
