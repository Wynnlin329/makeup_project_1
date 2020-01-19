from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time
import random
import os
#############################################################################################
def save_jpg():
    with open(jpg_name, 'wb') as f:
        f.write(response.content)
        f.close()
    print(jpg_name)

############################### 這裡先預先設定檔案 位置 與 ig 名稱 並確認網址名稱 ##################################################

url_name_title = "o.min_dyo"
file_name = "o_min_dyo"
filepath = "e:/inst/%s" %(file_name)
if os.path.exists(filepath):
    pass
else:
    os.mkdir(filepath)

#url = "https://www.instagram.com/explore/tags/%s/?hl=zh-tw" %(url_name_title)
url = "https://www.instagram.com/%s/?hl=zh-tw" %(url_name_title)

###################################################################################################################

useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
headers = {'User-Agent':useragent}
chromePath = "E:/Chrome_driver/chromedriver.exe"
browser = webdriver.Chrome(executable_path=chromePath)

browser.get(url)
time.sleep(5)
count_number = 0
photo_list = []

##################################### 先抓取 全部網址並判斷有沒有重複 ######################################

First_soup = BeautifulSoup(browser.page_source ,"lxml")
next_htmls = First_soup.select('div[class="v1Nh3 kIKUG _bz0w"]')
html_list = []
for i in next_htmls:
    print("https://www.instagram.com" + i.a["href"])
    mini_html = i.a["href"]
    html_list.append(mini_html)
#next_htmls = soup.select('span[id = "react-root"] div[class = "Nnq7C weEfm"] div[class="v1Nh3 kIKUG _bz0w"]')
#next_html_error = soup.select('span[id = "react-root"] div[class = "Nnq7C weEfm"] div[class="v1Nh3 kIKUG _bz0w"]')
#next_html_find = soup.find_all('span' ,id = 'react-root')
print(type(next_htmls))
print(len(next_htmls))
print(len(html_list))
lend = 0
double_html = 0
#### j => 8 range | i => 1 大約 100個網址

for i in range(3):
    lend = lend + 10000
    print("目前長度:", lend)

    for j in range(8):
        # 第一段
        html_temp = html_list[-1]
        print("第一段 html_temp : ", html_temp, "\n")
        print("第一段 html_lise[-1] : ", html_list[-1], "\n")
        js = "var q=document.documentElement.scrollTop=%s" % (lend)
        browser.execute_script(js)
        time.sleep(5)
        First_soup = BeautifulSoup(browser.page_source, "html.parser")
        b = First_soup.select('div[class="v1Nh3 kIKUG _bz0w"]')
        for i in b:
            print("https://www.instagram.com" + i.a["href"])
            mini_html = i.a["href"]
            html_list.append(mini_html)
        # for i in html_list:
        #    print(i)
        #    print("")
        print("第二段 html_temp : ", html_temp, "\n")
        print("應該要是新的 第二段 html_lise[-1] : ", html_list[-1], "\n")
        # 解決無法載入區域
        if html_temp == html_list[-1]:
            double_html += 1
            js = "var q=document.documentElement.scrollTop=0"
            browser.execute_script(js)
            time.sleep(5)

            js = "var q=document.documentElement.scrollTop=%s" % (lend)
            browser.execute_script(js)
            time.sleep(5)

            First_soup = BeautifulSoup(browser.page_source, "html.parser")
            b = First_soup.select('div[class="v1Nh3 kIKUG _bz0w"]')
            for i in b:
                print("https://www.instagram.com" + i.a["href"])
                mini_html = i.a["href"]
                html_list.append(mini_html)

    if double_html > 100 :
        break


set_html_list = list(set(html_list))
print(len(set_html_list))
####################### 利用下載下來的網址 List ############################
############################# 進入頁面並下載 ###################################

#計算錯誤次數
pass_error = 0
for p ,next_urls in enumerate(set_html_list):
    print("https://www.instagram.com" + next_urls)
    final_next_url = "https://www.instagram.com" + next_urls
    browser.get(final_next_url)
    next_page_soup = BeautifulSoup(browser.page_source, "lxml")
    naturl_jpg_len = next_page_soup.select('span[id="react-root"] ul[class="YlNGR"] li[class="_-1_m6"]')
    one_jpg = next_page_soup.select('span[id="react-root"] div[class="_97aPb wKWK0"] img')

    try:
        # 2 張以上判斷區
        if len(naturl_jpg_len) > 0 :
            jpg_len = len(naturl_jpg_len) - 2
            m = jpg_len // 3
            n = jpg_len % 3
            # 直接抓取照片位置
            jpg_html = next_page_soup.select('span[id="react-root"] ul[class="YlNGR"] li[class="_-1_m6"] img')
            print("總照片張數: ", len(naturl_jpg_len), "讀取到的img張數: ", len(jpg_html), " ||", " m=", m, " n=", n)

            #先印第一次
            for run1 in jpg_html:
                print(run1["src"])
                src = run1["src"]
                photo_list.append(src)
                #存照片第一區
                count_number += 1
                #存放路徑
                jpg_name = "e:/inst/%s/" %(file_name) + "%s__" %(count_number)  + src.split("/")[-1].split("?")[0]
                response = requests.get(url=src ,headers=headers ,timeout = 30)
                save_jpg()


            for freq_m in range(m):
                for run_click in range(3):
                    browser.find_element_by_class_name("coreSpriteRightChevron").click()
                    time.sleep(random.randint(1, 2))

                next_page_soup = BeautifulSoup(browser.page_source, 'html.parser')
                jpg_html = next_page_soup.select('span[id="react-root"] ul[class="YlNGR"] li[class="_-1_m6"] img')
                # print("總照片張數: " , len(jpg_len) , "讀取到的img張數: " ,len(jpg_html))

                for run1 in jpg_html:
                    print(run1["src"])
                    src = run1["src"]
                    photo_list.append(src)
                    #存照片第二區
                    count_number += 1
                    jpg_name = "e:/inst/%s/" %(file_name) + "%s__" %(count_number)  +src.split("/")[-1].split("?")[0]
                    response = requests.get(url=src, headers=headers, timeout=30)
                    save_jpg()

            for freq_n in range(n):
                browser.find_element_by_class_name("coreSpriteRightChevron").click()
                time.sleep(1)
            next_page_soup = BeautifulSoup(browser.page_source, 'html.parser')
            jpg_html = next_page_soup.select('span[id="react-root"] ul[class="YlNGR"] li[class="_-1_m6"] img')

            for num in range(3 - n, 3):
                print(jpg_html[num]["src"])
                src = jpg_html[num]["src"]
                photo_list.append(src)
                #存照片第三區
                count_number += 1
                jpg_name = "e:/inst/%s/" %(file_name) + "%s__" %(count_number)  + src.split("/")[-1].split("?")[0]
                response = requests.get(url=src ,headers=headers ,timeout = 30)
                save_jpg()
            # soup.find('div',"_5wCQW")["class"]

        #頁面只有 1 張判斷區
        elif len(one_jpg) == 1 :
            next_page_soup = BeautifulSoup(browser.page_source, 'html.parser')
            main_html = next_page_soup.select('span[id="react-root"] div[class="_97aPb wKWK0"] img')
            for run1 in main_html:
                print(run1["src"])
                src = run1["src"]
                photo_list.append(src)
                #存照片第四區
                count_number += 1
                jpg_name = "e:/inst/%s/" %(file_name) + "%s__" %(count_number)  + src.split("/")[-1].split("?")[0]
                response = requests.get(url=src,headers=headers ,timeout = 30)
                save_jpg()

        else:
            pass

    except:
        pass_error += 1
        pass

print(pass_error)
print(count_number)



#browser.quit()
