from lxml import html
import requests
import pymysql


def getData():
    alphabet = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "0"]
    #alphabet = ["A"]
    for alpha in alphabet:
        print(alpha + " in progress...")
        companylinks = "https://www.malaysiastock.biz/Listed-Companies.aspx?type=A&value=" + alpha
        crawler = AppCrawler(companylinks, 0)
        crawler.crawl()

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

        table = tree.xpath('//table[@id="MainContent_tStock"]/tr')
        for td in table:
            txt = td.xpath('.//td//text()')
            #print(txt)
            if (txt):
                shortname = txt[0].split(" ")[0]
                code = txt[0].split(" ")[1]
                code = code[code.find("(")+1:code.find(")")]
                if (len(txt[1])<=5):
                    board = txt[1]
                    name = txt[2].replace("'", "")
                    sector = txt[3]
                else:
                    board = '';
                    name = txt[1].replace("'", "")
                    sector = txt[2]
                data = "'" + code + "','" + shortname + "','" + name + "','" + board + "','" + sector + "'"
                #print(data)
                storeData(data)

        return


def storeData(data):
    databaseName = "stockdatabase"
    tableName = "StockList"
    tableHeader = "Code varchar(256) PRIMARY KEY,ShortName varchar(256),Name varchar(256),Board varchar(256),Sector varchar(256)"
    #tableCol = tableHeader.replace(' varchar(256)', '')
    tableCol = "Code,ShortName,Name,Board,Sector"

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
