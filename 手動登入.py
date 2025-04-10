from selenium import webdriver
import time
import pickle
import os

# 1. 第一次開啟登入頁，手動登入後儲存 cookies
driver = webdriver.Chrome()
driver.get("https://www.taobao.com")
time.sleep(30)  # 手動登入 + 驗證碼 + 掃碼等操作

# 登入完成後，儲存 cookies
pickle.dump(driver.get_cookies(), open("taobao_cookies.pkl", "wb"))
print("✅ cookies 儲存成功")
driver.quit()
