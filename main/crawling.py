from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
def web_crawling(id, pw):
    URL = "https://okasp.okpos.co.kr/login/login_form.jsp"
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")

    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
    driver.implicitly_wait(time_to_wait=30)
    driver.get(url=URL)
    driver.find_element(By.ID, "user_id").send_keys(id)
    driver.find_element(By.ID, "user_pwd").send_keys(pw)
    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div[2]/div[5]/img').click()

    time.sleep(1)
    handles = driver.window_handles

    size = len(handles)

    main_handle = driver.current_window_handle

    for x in range(size):
        if handles[x] != main_handle:
            driver.switch_to.window(handles[x])
            driver.close()

    driver.switch_to.window(main_handle)
    frame = driver.find_element(By.ID, "MainFrm")
    driver.switch_to.frame(frame)
    driver.find_element(By.XPATH, "/html/body/div[2]/div[4]/div[2]/button[4]").click()

    result = list()
    time.sleep(3)

    for i in range(2, 15):
        try:
            month = driver.find_element(By.XPATH, f"/html/body/div[2]/div[6]/div/div/div/div/div/table/tbody/tr[3]/td/div/div[1]/table/tbody/tr[{i}]/td[7]").text
            price = driver.find_element(By.XPATH, f"/html/body/div[2]/div[6]/div/div/div/div/div/table/tbody/tr[3]/td/div/div[1]/table/tbody/tr[{i}]/td[8]").text
            if month.replace(" ", "") == "":
                continue
            price = price.replace(",", "")
            result.append([month, price])
        except:
            pass

    driver.close()

    return result
