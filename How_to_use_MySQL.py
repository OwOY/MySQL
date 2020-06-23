import pymysql
import requests

connection = pymysql.connect(host='127.0.0.1',
                            port=3306,
                            user='root',
                            db='testsql',
                            charset='utf8',
)

cursor = connection.cursor()

# ----------------------------------------------輸入資料------------------------------------------------------------
cursor.execute("INSERT INTO `Table_Name`(`Column`) VALUES ([value-1])")

sql = "INSERT INTO `Table_Name`(`Column`, `Column1`, `Column2`) VALUES(%s,%s,%s)"    #上傳Turple+List格式
args = (['1','2','3'],['4','5','6'])
cursor.executemany(sql, args)

# ----------------------------------------------選擇查看--------------------------------------------------------------
cursor.execute("SELECT * FROM `Table_Name` WHERE `特定欄位` == X")
cursor.execute("SELECT `ID` FROM `Column` WHERE `特定欄位` == X")
cursor.execute(" SELECT  `Column`  FROM `Table_Name` ORDER BY  `特定欄位` DESC ")          # ASC為升幕   DESC為降幕
cursor.execute("SELECT  `Column`  FROM `Table_Name` WHERE  `特定欄位` LIKE  'admin' ")     #將內容有admin的取出
cursor.execute(" SELECT  `Column`  FROM `Table_Name` WHERE  `特定欄位` LIKE  %'adm'% ")    #將內容"含"有adm的資料取出(包括admin、administrator)

# ----------------------------------------------選擇更新--------------------------------------------------------------
cursor.execute("UPDATE `Table_Name` SET `ID`=[value-1] WHERE `特定欄位` == X")

# ----------------------------------------------選擇刪除--------------------------------------------------------------
cursor.execute("DELETE FROM `Table_Name` WHERE `特定欄位` == X")

# ----------------------------------------------清除TABLE-------------------------------------------------------------
cursor.execute("TRUNCATE TALBE `Table_Name`")

# ----------------------------------------------清除TABLE-------------------------------------------------------------
