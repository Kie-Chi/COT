import time
import sys
import getpass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException,ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import logging
import Runner

def explicit_click(browser, selector: str):
    try:
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        browser.find_element(By.CSS_SELECTOR, selector).click()
        return True
    except (TimeoutException, ElementNotInteractableException) as e:
        # print(e)
        time.sleep(0.1)
        try:
            browser.execute_script(f'document.querySelector("{selector}").click();')
        except Exception as e:
            # print("JavaScript execute ERROR too")
            # print(e)
            return False
    return False


def explicit_fill(browser, selector: str, text: str, keys=None):
    try:
        # 点击元素
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        browser.find_element(By.CSS_SELECTOR, selector).click()
        # 输入文本
        element = browser.find_element(By.CSS_SELECTOR, selector)
        element.clear()  # 清除之前的文本
        element.send_keys(text)  # 输入新文本
        if keys:
            element.send_keys(keys)
    except (TimeoutException, ElementNotInteractableException) as e:
        # print(e)
        time.sleep(0.1)
        try:
            # 使用JavaScript来模拟点击和输入
            browser.execute_script(f"document.querySelector('{selector}').click();")
            browser.execute_script(f"document.querySelector('{selector}').value = '{text}';")
        except Exception as e:
            # print("JavaScript execute ERROR too")
            # print(e)
            pass
def get_pic():
    usr = input("Usr:")
    password = getpass.getpass("PassWord:")
    projects = ["Pre", "P0", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "P8"]    
    chrome_options = Options()  
    chrome_options.add_argument("--headless")  # 启用无头模式
    chrome_options.add_argument("--disable-logging")  # 禁用日志
    chrome_options.add_argument("--log-level=3")  # 设置最低日志级别
    logging.getLogger('tensorflow').setLevel(logging.ERROR)
    logging.getLogger("selenium").setLevel(logging.WARNING)
    browser = webdriver.Chrome(options=chrome_options)
    browser.get("http://cscore.buaa.edu.cn/#/problem?ProblemId=334&PieId=1202")
    explicit_click(browser, ".v-btn__content .align-center")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"iframe#loginIframe")))
    browser.switch_to.frame('loginIframe')
    time.sleep(1)
    explicit_fill(browser, "div.content-con-box:nth-of-type(1) div.item:nth-of-type(1) input", usr)
    time.sleep(1)
    explicit_fill(browser, "div.content-con-box:nth-of-type(1) div.item:nth-of-type(3) input", password)
    time.sleep(1)
    explicit_click(browser, "div.content-con-box:nth-of-type(1) div.item:nth-of-type(7) input")
    try:
        explicit_click(browser, ".v-btn__content .align-center")
    except:
        pass
    browser.get("http://cscore.buaa.edu.cn/#/account")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-list-item__subtitle")))
    name = browser.find_element(By.CSS_SELECTOR, "div.v-list-item__subtitle")
    name = name.text
    browser.get("http://cscore.buaa.edu.cn/#/exams-list")
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.v-card__text span.v-chip__content")))
    passes = browser.find_elements(By.CSS_SELECTOR, "div.v-card__text span.v-chip__content")
    passes = [_pass.text for _pass in passes]
    passes = passes[::-1]
    ind = 0
    for _pass in passes:
        print(f"{projects[ind]}: {_pass}")
        if _pass == "通过":
            ind += 1
    width = browser.execute_script("return document.body.parentNode.scrollWidth")
    height = browser.execute_script("return document.body.parentNode.scrollHeight")
    # 调整窗口大小以匹配整个页面
    browser.set_window_size(width, height)

    screenshot = browser.get_screenshot_as_png()
    with open(f"{name}-CO冒险之旅.png","wb") as file:
        file.write(screenshot)
    browser.quit()

def gift():
    pre_print()
    print_out("你好，我是COT！")
    pre_print()
    print_out("首先祝贺你通过了我设下的所有考验，想必你已经顺利通关计算机组成了！")
    pre_print()
    print_out("")

def first():
    pre_print()
    print_out("还记得我们第一次相遇吗？")
    pre_print()
    print_out("")

def pre_print():
    Runner.print_colored("COT> ", 96, end="")

def print_out(text="", fg_color=97, bg_color=None, style=None, end="\n", delay=0.1):
    for char in text:
        Runner.print_colored(char, fg_color=fg_color, bg_color=bg_color, style=style, end="", flush=True)
        time.sleep(delay)
    print(end, end="")

if __name__ == "__main__":
    gift()