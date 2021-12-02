import csv
from selenium import webdriver, common
from bs4 import BeautifulSoup  # pip install bs4
import random
from time import sleep
import requests
import json

# py -m pip install --upgrade pip

#my_profile = webdriver.FirefoxProfile(
#    r"C:\Users\Hardi\AppData\Roaming\Mozilla\Firefox\Profiles\j62wgvhz.default"
#)
#binary = FirefoxBinary("C:/Program Files/Mozilla Firefox/firefox.exe")
#options = webdriver.FirefoxOptions()
#options.set_preference(
#    "general.useragent.override",
#    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:90.0) Gecko/20100101 Firefox/90.0",
#)
## set headless mode on True False
#options.set_headless(True)
#driver = webdriver.Firefox(
#    firefox_profile=my_profile, firefox_binary=binary, options=options
#)

#URL = "https://www.flashscore.ru/table-tennis/others-men/liga-pro/fixtures/"


#def get_html(url):
#    try:
#        driver.get(url)
#        time.sleep(2)

#        with open("output_selenium_pro.html", "w", encoding="utf=8") as file:
#            file.write(driver.page_source)
#    except Exception as ex:
#        print(ex)


#def parse():
#    get_html(URL)
#    with open("output_selenium_pro.html", encoding="utf=8") as file:
#        src = file.read()
#    #find_matches(src)

#    driver.quit()
#    driver.close()


#parse()


url = "https://coinmarketcap.com/ru/"
#
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 11_0 like Mac OS X) AppleWebKit/604.1.34 (KHTML, like Gecko) Version/11.0 Mobile/15A5341f Safari/604.1"
}

def parse_src():
    req = requests.get(url, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    data = soup.find("a", {"href": "/ru/currencies/dogecoin/markets/"}).text
    return data

def parse_src1():
    req = requests.get("https://www.blockchain.com/prices/api/coin-list-page?limit=20&page=0&tsym=USD", headers=headers)
    src = req.text    
    data = req.json()
    dogecoin = [x for x in data["Data"] if x["CoinInfo"]["Name"] == "DOGE"][0]
    return dogecoin["DISPLAY"]["USD"]["PRICE"]

#print(src)

#with open("index.html", "w") as file:
#    file.write(src)

#with open("index.html") as file:
#    src = file.read()

if __name__== "__main__":
    try:
        print("Dogecoin rate: ", parse_src() )
        print("Dogecoin rate: ", parse_src1() )
    except Exception as ex:
        print(ex)


print("Dogecoin rate: ", parse_src1() )