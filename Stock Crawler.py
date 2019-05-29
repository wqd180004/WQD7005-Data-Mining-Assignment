from lxml import html
from selenium import webdriver
from datetime import datetime
import requests
import pymysql
import os


def getData():
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U","V", "W", "X", "Y", "Z", "0-9"]
    #alphabet = ["S", "T", "U","V", "W", "X", "Y", "Z", "0-9"]
    for alpha in alphabet:
        print(alpha + " in progress...")
        driver = webdriver.Chrome(
            executable_path=r"C:\chromedriver.exe")
        driver.get("https://www.thestar.com.my/business/marketwatch/stock-list/?alphabet=" + alpha)
        companyLinks = driver.find_elements_by_xpath('//div[@id="active"]//a')
        for link in companyLinks:
            value = link.get_attribute('href')
            # print(value)
            crawler = AppCrawler(value, 0)
            crawler.crawl()
        driver.quit()

class AppCrawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url)
        return

    def get_app_from_link(self, link):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

        name = tree.xpath('//h1[@class="stock-profile f16"]/text()')[0]
        code = tree.xpath('//li[@class="f14"]/text()')[1]
        board = tree.xpath('//li[@class="f14"]/text()')[0]
        weekhigh = tree.xpath('//li[@class="f14"]/text()')[2]
        weeklow = tree.xpath('//li[@class="f14"]/text()')[3]
        date = tree.xpath('//span[@id="slcontent_0_ileft_0_datetxt"]/text()')[0]
        time = tree.xpath('//span[@id="slcontent_0_ileft_0_timetxt"]/text()')[0]
        tdopen = tree.xpath('//td[@id="slcontent_0_ileft_0_opentext"]/text()')[0]
        tdhigh = tree.xpath('//td[@id="slcontent_0_ileft_0_hightext"]/text()')[0]
        tdlow = tree.xpath('//td[@id="slcontent_0_ileft_0_lowtext"]/text()')[0]
        tdlastdone = tree.xpath('//td[@id="slcontent_0_ileft_0_lastdonetext"]/text()')[0]
        if (tree.xpath('//td[@id="slcontent_0_ileft_0_chgtext"]/span')):
            tdchgtext = tree.xpath('//td[@id="slcontent_0_ileft_0_chgtext"]/span/text()')[0]
        else:
            tdchgtext = tree.xpath('//td[@id="slcontent_0_ileft_0_chgtext"]/text()')[0]
        tdchgpercenttrext = tree.xpath('//td[@id="slcontent_0_ileft_0_chgpercenttrext"]/text()')[0]
        tdvolume = tree.xpath('//td[@id="slcontent_0_ileft_0_voltext"]/text()')[0]
        tdbuyvol = tree.xpath('//td[@id="slcontent_0_ileft_0_buyvol"]/text()')[0]
        tdsellvol = tree.xpath('//td[@id="slcontent_0_ileft_0_sellvol"]/text()')[0]

        board = board[3:]
        code = code[3:]
        weekhigh = weekhigh[3:]
        weeklow = weeklow[3:]
        date = date[10:].replace(" |", "")
        dt = datetime.strptime(date + " " + time, '%d %b %Y %I:%M %p').strftime('%Y%m%d%H%M')

        # unique id to store in database using format: date (yyyymmdd) + time (hhmm) + stock Code
        idno = dt + code

        data = ""
        data += "'" + idno
        data += "','" + name
        data += "','" + code
        data += "','" + board
        data += "','" + date
        data += "','" + time
        data += "','" + weekhigh
        data += "','" + weeklow
        data += "','" + tdopen
        data += "','" + tdhigh
        data += "','" + tdlow
        data += "','" + tdlastdone
        data += "','" + tdchgtext
        data += "','" + tdchgpercenttrext
        data += "','" + tdvolume
        data += "','" + tdbuyvol
        data += "','" + tdsellvol
        data += "'"
        # print(data)
        storeData(data)

        return


def storeData(data):
    databaseName = "StockDatabase"
    tableName = "StockPrice"
    tableHeader = "ID varchar(256) PRIMARY KEY, Name varchar(256), Code varchar(256), Board varchar(256), Date varchar(256), Time varchar(256), 52WeekHigh varchar(256), 52WeekLow varchar(256), Open varchar(256), High varchar(256), Low varchar(256), Last varchar(256), Chg varchar(256), ChgPercent varchar(256), Volume varchar(256), BuPerVol varchar(256), SellPerVol varchar(256)"
    tableCol = tableHeader.replace(' varchar(256)', '').replace(' PRIMARY KEY','')
    if not os.path.exists(databaseName + '.db'):
        conn = pymysql.connect(host='localhost', user='root', password='')

        a = conn.cursor()

        # For creating create db
        # Below line  is hide your warning
        a.execute("SET sql_notes = 0; ")
        # create db here....
        a.execute("create database IF NOT EXISTS " + databaseName)

    # connect to database created
    conn = pymysql.connect(host='localhost', user='root', password='', db=databaseName)
    a = conn.cursor()

    # create table
    a.execute("SET sql_notes = 0; ")
    a.execute("create table IF NOT EXISTS " + tableName + "(" + tableHeader + ");")
    a.execute("SET sql_notes = 1; ")

    # insert data
    a.execute("insert ignore into " + tableName + "(" + tableCol + ") values(" + data + ")")

    # Commit your changes in the database
    conn.commit()

    # disconnect from server
    conn.close()


print("Task Start...")
getData()
print("Task End!")
