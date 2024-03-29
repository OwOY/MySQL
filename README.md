<p align='center'>
  <img height=350px src="https://upload.wikimedia.org/wikipedia/zh/thumb/6/62/MySQL.svg/1200px-MySQL.svg.png"/>
</p>  

------------------------
## Install MySQL
```
apt -y install mysql or apt -y install mariadb-server  (Prefer to use mariadb)
yum -y install mysql or yum -y install mariadb-server  (Prefer to use mariadb)
```
## First time set MySQL
```
sudo mysql_secure_installation
```
## Set use password to login 
```
UPDATE mysql.user SET plugin="mysql_native_password";
```
## reset password 
```
update user set password = PASSWORD('test') where host = 'localhost'
```
## Install pymysql  
```
python -m pip install pymysql  
```
## How to use
### Import
```
import pymysql
```
## Use case
- 連接資料庫  

```
connection = pymysql.connect(host='127.0.0.1',
                            port=3306,
                            user='root',
                            db='testsql',
                            charset='utf8',
)

cursor = connection.cursor()
```
- 創建Table
```
cursor.execute("CREATE TABLE Table_Name(column1 TEXT, column2 TEXT PRIMARY KEY")
```
- 複製Table
```
cursor.execute("CREATE TABLE new_table LIKE old_table")
cursor.execute("INSERT INTO table `new_table` (Select * from `old_table`)")
```
- 新增欄位
```
cursor.execute("ALTER TABLE Table_Name ADD column TEXT")
```
- 輸入資料
```
a = 123
cursor.execute("INSERT INTO `Table_Name`(`Column`) VALUES ([value-1])",(a))

sql = "INSERT INTO `Table_Name`(`Column`, `Column1`, `Column2`) VALUES(%s,%s,%s)"    #上傳Turple+List格式
args = (['1','2','3'],['4','5','6'])
cursor.executemany(sql, args)
```
- 選擇查看
>> cursor.execute("SELECT * FROM `Table_Name` WHERE `特定欄位` == X")  
>> cursor.execute("SELECT `ID` FROM `Table_Name` WHERE `特定欄位` == X")  
>> cursor.execute(" SELECT  `Column`  FROM `Table_Name` ORDER BY  `特定欄位` DESC ")          # ASC為升幕   DESC為降幕  
>> cursor.execute("SELECT  `Column`  FROM `Table_Name` WHERE  `特定欄位` LIKE  'admin' ")     #將內容有admin的取出  
>> cursor.execute(" SELECT  `Column`  FROM `Table_Name` WHERE  `特定欄位` LIKE  '%adm%' ")    #將內容"含"有adm的資料取出(包括admin、administrator)  
>> cursor.execute("SELECT `A`.'Name' FROM `Table_Name` AS `A` , `Table_Name` AS `B`")        #暫存Table  
>> cursor.execute("Select distinct col_name FROM table_name")                                #查詢特定欄位不同值  

- 選擇更新
```
cursor.execute("UPDATE `Table_Name` SET `ID`=[value-1] WHERE `特定欄位` == X")
```
- 更新特定條件的值(XY轉換)  
```
cursor.execute("UPDATE `Table_Name` SET `特定欄位`= CASE `特定欄位` WHEN 'X' THEN 'Y' ELSE 'X'END;")  
cursor.execute("UPDATE `Table_Name` SET `特定欄位`= CASE `特定欄位` WHEN 'X' THEN 'Y' WHERE 'Y' THEN 'X'END;")  
```
- 選擇刪除
```
cursor.execute("DELETE FROM `Table_Name` WHERE `特定欄位` == X")
```
- 刪除Column
```
cursor.execute("ALTER TABLE `Table_Name` Drop `特定欄位`")
```
- 清除TABLE
```
cursor.execute("TRUNCATE TALBE `Table_Name`")
```
- 刪除TABLE
```
cursor.execute("DROP TABLE `Table_Name`")
```
- 連結TABLE
```
cursor.execute("SELECT * FROM `Table_Name_A` inner join `Table_Name_B` on `Table_Name_A`.`特定欄位` = `Table_Name_B`.`特定欄位`")
```
- 尋找重複值
```
cursor.execute("SELECT * FROM `Table_Name` GROUP BY '特定欄位' having count(*) !=1 ")
```
-------------------------------
- 確認修改  
connection.commit()    
- 關閉連線  
connection.close()       

- 若要用變數呼叫TABLE   可使用Python語法   
f'{TABLE_NAME}

# Bonus
## 選取SQL字段 SUBSTRING
```
select substring(f'{column}', 1, 4) from table_name # 取 column 欄位的第一個字，取4位數。 
```
>>> 20220318 > 2022
## 選取所有欄位中最大值 GREATEST
```
select * from table_name where GREATEST(column1, column2 , column3) > 90
```
|column1|column2|column3|  
|--|--|--|
|6|5|2022|
## 取得欄位為空補值
```
select nal(column1, 0), nal(column2, 'test') from table_name
```
