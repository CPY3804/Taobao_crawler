from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pickle
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd  # 新增 pandas 套件的導入


#pip install selenium pandas openpyxl

def load_cookies(driver, cookies_path="taobao_cookies.pkl"):
    """載入 cookies 並登入"""
    driver.get("https://taobao.com")  # ⚠️ 必須打開對的 domain
    time.sleep(2)

    with open(cookies_path, "rb") as f:
        cookies = pickle.load(f)

    for cookie in cookies:
        # 避免 selenium 拋錯：刪掉 cookie 中的 'sameSite' 與 'expiry'
        cookie.pop('sameSite', None)
        cookie.pop('expiry', None)
        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(f"⚠️ Cookie 加載失敗: {cookie.get('name')}，原因：{e}")

    driver.refresh()
    time.sleep(3)
    print("✅ Cookies 已加載，頁面已刷新")

def search_product(driver, keyword):
    """根據關鍵字搜尋商品"""
    search_input = driver.find_element(By.ID, "q")
    search_input.clear()
    search_input.send_keys(keyword)
    time.sleep(random.randint(1, 3))
    driver.find_element(By.XPATH, '//*[@id="J_TSearchForm"]/div[2]/button').click()
    print(f"✅ 已搜尋「{keyword}」")


def scrape_products(driver):
    """抓取搜尋結果頁面上的所有商品資訊"""
    try:
        # 等待商品元素載入（class="item" 是每個商品外層）
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "item")]'))
        )
    except Exception as e:
        print(f"❌ 等待商品載入超時：{e}")
        return []

    # 切換到新分頁（如果搜尋結果是在新分頁）
    driver.switch_to.window(driver.window_handles[-1])

    # 獲取所有商品元素
    products = driver.find_elements(By.XPATH, '//div[@id="content_items_wrapper"]/div')  # 所有商品的 div 標籤

    results = []
    for idx, product in enumerate(products):  # 移除 max_count 限制
        try:
            title_el = product.find_element(By.XPATH, './/div[contains(@class, "title")]')
            price_el = product.find_element(By.XPATH, './/div[contains(@class, "priceInt")]')
            link_el = product.find_element(By.XPATH, './/a')  # 假設 a 標籤包含商品連結

            title = title_el.text.strip()
            price = price_el.text.strip()
            link = link_el.get_attribute('href')
            results.append({
                "title": title,
                "price": price,
                "link": link
            })

        except Exception as e:
            print(f"❌ 第 {idx+1} 筆資料出錯：{e}")
            continue

    print("\n📦 抓取到的商品資訊如下：\n")
    for i, item in enumerate(results, 1):
        print(f"{i}. [{item['title']}]")
        print(f"   💰 價格：{item['price']} 元")
        print(f"   🔗 連結：{item['link']}\n")

    # 將結果保存到 Excel 文件
    if results:
        df = pd.DataFrame(results)  # 將結果轉換為 pandas 的 DataFrame
        df.to_excel("商品資料"+word+".xlsx", index=False)  # 保存為 Excel 文件
        print("✅ 商品資訊已成功導出至商品資料.xlsx")
    else:
        print("⚠️ 沒有抓取到任何商品資訊，無法生成 Excel 文件。")

    return results




if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)

    load_cookies(driver)

    word = input("請輸入要搜尋的商品：")

    search_product(driver, word)

    scrape_products(driver)


    input("請按 Enter 關閉瀏覽器...")
    driver.quit()
