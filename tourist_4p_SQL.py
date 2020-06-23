import requests
import json
import prettytable as pt
from bs4 import BeautifulSoup
import os
import pymysql
import time

connection = pymysql.connect(host='127.0.0.1',
                            port=3306,
                            user='root',
                            db='testsql',
                            charset='utf8',
)

cursor = connection.cursor()

i = 1

args = []
args1 = []
requests = requests.Session()

while i<11:
    p = requests.post(
        'https://www.4p.com.tw/EW/Services/SearchListData.asp',
        headers = {
                    'Host': 'www.4p.com.tw',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                    'Accept': '*/*',
                    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                    'Accept-Encoding': 'gzip, deflate',
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'X-Requested-With': 'XMLHttpRequest',
                    'Content-Length': '244',
                    'Origin': 'https://www.4p.com.tw',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Referer': 'https://www.4p.com.tw/EW/GO/GroupList.asp',
                    'Cookie': 'ASPSESSIONIDAGQSRRAB=ILDNJDEDFCBFFLJMGFDEEPGH; ASPSESSIONIDCWSTADDQ=OAGIFMODLHFBPPENFIBDHNJN'
        },
        data = {
                    'displayType':'G',
                    'orderCd':'1',
                    'pageALL':i,
                    'pageGO':'1',
                    'pagePGO':'1',
                    'waitData':'false',
                    'waitPage':'false',
                    'SrcCls':'D',
                    'beginDt':'2020/06/22',
                    'endDt':'2020/12/22',
                    'allowJoin':'1',
                    'allowWait':'1'
        }
    )

    a = json.loads(p.text)['All']
    Link = []
    for b in a:
        Product_Type = b['SubCdAnm']
        Product_ID = b['GrupCd']
        Product_Name = b['GrupSnm']
        Product_Day = b['GrupLn']
        Product_Date = b['LeavDt']
        Product_Date_day = b['WeekDay']
        Product_Price = b['SaleAm']
        Product_Total_Seat = b['EstmYqt']
        Product_Remaining_Seat = b['SaleYqt']
        Product_Link = 'https://www.4p.com.tw'+b['Url']
# --------------------------------------------------------------------------------------------------------
#         Product_imgLink = 'https://www.newamazing.com.tw'+b['ImgUrl']     圖片連結
#         Product_SignUplink = 'https://www.newamazing.com.tw'+b['SignUpLink']['Url']      註冊連結
# --------------------------------------------------------------------------------------------------------
        args.append([Product_ID,Product_Day,Product_Name,Product_Date+'('+Product_Date_day+')',Product_Price,Product_Remaining_Seat,Product_Total_Seat])
        
        p1 = requests.get(
            Product_Link,
            headers = {
                        'Host': 'www.4p.com.tw',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate',
                        'Referer': 'https://www.4p.com.tw/EW/GO/GroupList.asp?displayType=G&subCd=&orderCd=1&pageALL=3&pageGO=1&pageGI=&pagePGO=1&waitData=false&waitPage=false&mGrupCd=&SrcCls=D&tabList=&regmCd=&regsCd=&beginDt=2020%2F06%2F22&endDt=2020%2F12%2F22&portCd=&tdays=&bjt=&carr=&allowJoin=1&allowWait=1&ikeyword=',
                        'DNT': '1',
                        'Connection': 'keep-alive',
                        'Cookie': 'ASPSESSIONIDAGQSRRAB=ILDNJDEDFCBFFLJMGFDEEPGH; ASPSESSIONIDCWSTADDQ=OAGIFMODLHFBPPENFIBDHNJN',
                        'Upgrade-Insecure-Requests': '1',
                        'Cache-Control': 'max-age=0'
                })
        p1.encoding = 'utf8'
        data1 = BeautifulSoup(p1.text,'lxml')
        # ---------------------------------------------------------------------------------------------------------
        day = data1.find_all('span',class_='tw_day')
        day = [D.text.strip() for D in day]
        # ---------------------------------------------------------------------------------------------------------
        eat = data1.find_all('dl',class_='dl-horizontal')
        eat = [E.text.strip().replace('\n',' ') for E in eat]
        # ---------------------------------------------------------------------------------------------------------
        location = data1.find_all('h4',class_='col-xs-12 col-sm-12 col-md-11 col-lg-11 day_title_right')
        location = [L.text.strip() for L in location]
        # ---------------------------------------------------------------------------------------------------------
        restin = data1.find_all('p',{'name':'itnHtl'})
        restin = [R.text.strip() for R in restin]
        # ---------------------------------------------------------------------------------------------------------
        content = data1.find_all('div',class_='col-xs-12 col-sm-12 col-md-12 col-lg-12 day_content')
        content = [C.text.strip() for C in content]
        # ---------------------------------------------------------------------------------------------------------
        # deadLine = data1.find_all('li',class_='col-xs-12 col-sm-12 col-md-2 col-lg-2 deadline')
        # deadLine = [D.text.strip() for D in deadLine]
        # ------------------------------------簡易版...大小月待修正--------------------------------------------------
        departureLine = data1.find_all('li',class_='col-xs-12 col-sm-12 col-md-2 col-lg-2 departure_date')
        departureLine_d = [DD.text.strip().split('/')[-1] for DD in departureLine]
        departureLine_ym = [('/').join(DYM.text.strip().split('/')[:-1]) for DYM in departureLine]
        # ---------------------------------------------------------------------------------------------------------
        for j in range(len(day)):
            try:
                GoDate = departureLine_ym[0]+'/'+str(int(departureLine_d[0])+j)
                args1.append([Product_ID,GoDate,day[j],Product_Name,content[j],eat[j],location[j],restin[j]])
            except:
                args1.append([Product_ID,GoDate,day[j],Product_Name,content[j],eat[j],location[j],'回家~'])
    i+=1           
sql = "INSERT INTO `tourist_4p`(`TourID`, `Day`, `Title`, `GoDate`, `Price`, `RemainSeat`, `TotalSeat`)VALUES(%s,%s,%s,%s,%s,%s,%s)"
sql1 = "INSERT INTO `tourist_4p_info`(`TourID`, `GoDate`, `Day`, `Title`, `Content`, `Eat`, `Location`, `Hotel`)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
cursor.executemany(sql, args)
cursor.executemany(sql1, args1)
connection.commit()   
connection.close()
    