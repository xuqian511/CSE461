# 引入 requests 模組
import requests
print("hi")
# 使用 GET 方式下載普通網頁
#r = requests.get('http://courses.cs.washington.edu/courses/cse461/15au/assignments/project2/simple.html')
r = requests.get('http://www.google.com')
#這裡我們以 GET 下載 Google 的網頁後，將結果儲存於 r 這個變數中，首先確認一下從伺服器傳回的狀態碼：
# 伺服器回應的狀態碼
print(r.status_code)
print(r.headers)
print(r.history)
#200
#如果顯示 200 就代表沒問題。我們也可以利用以下這個判斷式來檢查狀態碼：
# 檢查狀態碼是否 OK
if r.status_code == requests.codes.ok:
    print("OK")
#在確認狀態碼沒問題之後，接著即可放心使用抓回來的資料，如果要查看原始的網頁 HTML 程式碼，可以從 r.text 取得：
# 輸出網頁 HTML 原始碼
#print(r.text)
