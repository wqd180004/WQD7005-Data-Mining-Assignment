import pymysql
from datetime import datetime
from selenium import webdriver

databaseName = "stockdatabase"
tableName1 = "StockList"
tableName2 = "StockFinancial"

def getData():

    sql = 'SELECT code from StockList'

    a.execute(sql)

    data = a.fetchall()

    for code in data:
        code = convertTuple(code)
        link = "https://klse.i3investor.com/servlets/stk/fin/" + code + ".jsp"
        print(link)
        driver = webdriver.Chrome(
            executable_path=r"C:\chromedriver.exe")
        driver.get(link)
        tr = driver.find_elements_by_xpath('//tr[contains(@class, "odd") or contains(@class, "even")]')

        for td in tr:
            value = td.text
            value = value.replace("- %", "0%")
            value = value.split(" ")
            if validate(value[1]):
                str_list = list(filter(None, value))
                str_list = "','".join(str_list).strip("'")

                Quarter = value[1]
                id = datetime.strptime(Quarter, '%d-%b-%Y').strftime('%Y%m%d') + code

                data = "'" + id + "','" + code + "','" + str_list + "'"
                #print (data)
                storeData(data)

        driver.quit()


def validate(date_text):
    try:
        if date_text != datetime.strptime(date_text, "%d-%b-%Y").strftime('%d-%b-%Y'):
            raise ValueError
        return True
    except ValueError:
        return False


def storeData(data):

    tableHeader = "ID varchar(256) PRIMARY KEY,Code varchar(256),AnnDate varchar(256),Quarter varchar(256),Revenue varchar(256),PBT varchar(256),NP varchar(256),NPtoSH varchar(256),NPMargin varchar(256),ROE varchar(256),EPS varchar(256),DPS varchar(256),NAPS varchar(256),QoQ varchar(256),YoY varchar(256)"
    tableCol = tableHeader.replace(' varchar(256)', '').replace(' PRIMARY KEY','')
    #print(tableCol)

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
    str = ''.join(tup)
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
