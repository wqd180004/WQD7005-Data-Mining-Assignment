from lxml import html
import requests
import pymysql
#from googletrans import Translator
#import goslate
from datetime import datetime
import re

databaseName = "stockdatabase"
tableName1 = "StockList"
tableName2 = "StockNewsHeadline"

def getData():
    sql = 'SELECT code from StockList'

    a.execute(sql)

    data = a.fetchall()

    for code in data:
        code = convertTuple(code)
        link = "https://www.klsescreener.com/v2/news/stock/" + code
        print(link)
        crawler = AppCrawler(link, code, 0)
        crawler.crawl()


class AppCrawler:
    def __init__(self, starting_url, code, depth):
        self.starting_url = starting_url
        self.code= code
        self.depth = depth
        self.apps = []

    def crawl(self):
        self.get_app_from_link(self.starting_url, self.code)
        return

    def get_app_from_link(self, link, code):
        start_page = requests.get(link)
        tree = html.fromstring(start_page.text)

        table = tree.xpath('//div[@class="article flex-1"]')
        for div in table:
            txt = div.xpath('.//div//text()')
            link = div.xpath('.//div//a')[0]
            link = "https://www.klsescreener.com" + link.get('href')
            headline = txt[0]
            chinese = re.findall(r'[\u4e00-\u9fff]+', headline)

            #translator = goslate.Goslate()
            #language = translator.detect(headline)
            if (chinese):
                pass
            else:
            #    translator = Translator()
            #    translations = translator.translate(headline)
            #    headline = translations.text
                headline = headline.replace("'","")
                source = txt[-2]
                date = txt[-1].split(" -")[0]
                date = date[:-2]
                dt = datetime.strptime(date, '%d %b, %Y %H:%M').strftime('%Y%m%d%H%M')
                id = source + dt + code
                data = "'" + id + "','" + code + "','" + headline + "','" + source + "','" + date + "','" + link + "'"
                storeData(data)

        return


def storeData(data):

    tableHeader = "ID varchar(256) PRIMARY KEY,Code varchar(256),Headline varchar(15000),Source varchar(256),Date varchar(256),URL varchar(256)"
    tableCol = "ID,Code,Headline,Source,Date,URL"

    # connect to database created
    #conn = pymysql.connect(host='localhost', user='root', password='', db=databaseName)
    #a = conn.cursor()

    # create table
    a.execute("SET sql_notes = 0; ")
    a.execute("create table IF NOT EXISTS " + tableName2 + "(" + tableHeader + ");")
    a.execute("SET sql_notes = 1; ")

    # insert data
    a.execute("insert ignore into " + tableName2 + "(" + tableCol + ") values(" + data + ")")

# Python3 code to convert tuple
# into string
def convertTuple(tup):
    str =  ''.join(tup)
    return str

startTime = datetime.now();
print("Task Start...")
print(startTime)
conn = pymysql.connect(host='localhost', user='root', password='', db=databaseName)
a = conn.cursor()

getData()

# Commit your changes in the database
conn.commit()

# disconnect from server
conn.close()
endtime = datetime.now();
print("Task End! ")
print(endtime)
