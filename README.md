# -Project Title ： 淘寶爬蟲

Introduction：
用AI輔助，完成想在淘寶搜尋特定商品抓取標題、價格、連接網址，最後轉存成excel。

Feature：
1.先手動登入存cookie，手動通過驗證機制。
2.讀取cookie自動登入，自動爬蟲。

Tech Stack：
- python 3.12.9
- anaconda
- selenium
- padas
- openpyxl

Tools Used：
-ChatGPT
-XPATH
-google chrome 擴充功能 XPATH 測試器

Optional：
 - GPT產生的XPAH定位語法需要變更，手動找到可以定位的class或是id，用XPATH測試器輔助找到正確的定位。
 - 經過不斷確認你會發現爬到資訊都是空值，解決方法是確認你執行爬蟲的所在瀏覽器頁面是哪個，預設會是首頁，不是搜尋到商品的那頁，所以先跳轉頁面就可以使用爬蟲。
 - 最後修改 link 找href的位置，先獨立找到標籤a的位置可以抓到商品網址。

