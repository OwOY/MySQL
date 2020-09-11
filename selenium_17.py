import selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
import pymysql
from txt import txt
import re
import datetime

# ------------------------------------------------------------------------------------
class db:
    def use_my_sql():
        connection = pymysql.connect(host='192.168.1.73',
                                    password = 'mJAbt84j3jK3nteX',
                                    user='crawler',
                                    db='crawler',
                                    charset='utf8'
        )

        return connection.cursor()
        
    def use_17_sql():
        connection = pymysql.connect(host='192.168.1.73',
                                    password = 'j8Te3pm3nTGdshtA',
                                    user='post_17',
                                    db='post_17',
                                    charset='utf8'
        )

        return connection.cursor()
        
    def post_17_sql():
        connection = pymysql.connect(host='192.168.1.73',
                                    password = 'j8Te3pm3nTGdshtA',
                                    user='post_17',
                                    db='post_17',
                                    charset='utf8'
        )

        return connection.cursor()

# ------------------------------------------------------------------------------------

def login_ready_to_post(driver, username, password):
    driver.get('https://db.forum.jingm.com/member.php?mod=logging&action=login')
    sleep(2)
    driver.maximize_window()
    sleep(2)
    driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
    sleep(1)
    driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
    sleep(1)
    driver.find_element_by_xpath(r'/html/body/div[4]/div/div[2]/div/div[2]/div[1]/div[1]/form/div/div[6]/table/tbody/tr/td/button').click()
    sleep(2)
    

    return driver




def SQL_DATA(Table, SQL_command_select):
    
    cursor = db.use_my_sql()
    
    title_list = []
    article_list = []
    
    cursor.execute(f"SELECT title, content FROM `{Table}`{SQL_command_select}")
    SQL_list = cursor.fetchall()
    for SQL in SQL_list:
        title_list.append(SQL[0])
        article_list.append(SQL[1])
  
    return title_list, article_list




def insert_SQL(title, url):
    
    cursor = db.post_17_sql()
    cursor.execute('INSERT INTO `POST`(`subject`, `url`, `posttime`) VALUES (%s,%s,%s)',(title, url, str(datetime.datetime.now())))
    print(title, url, datetime.datetime.now())

# def check_SQL_not_same(title):
      
#     cursor = db.use_17_sql()
#     cursor.execute('SELECT `subject` FROM `POST`')
#     title_SQL_list = cursor.fetchall()
    
   
    
#     if title in title_SQL_list:
#         retrun continue
    
    
    

def auto_post(driver, article_content, title_content):
    
    # check_SQL_not_same(title_content)
    
    driver.get('https://db.forum.jingm.com/forum.php?mod=post&action=newthread&fid=38')
    sleep(2)
    
    # ----------------------------------選擇分類-----------------------------------------
    driver.find_element_by_xpath("//*[@id='typeid_ctrl']").click()    
    sleep(2)
    driver.find_element_by_xpath("//li[text()='网路正妹']").click()    
    sleep(2)
    driver.find_element_by_xpath("//*[@id='subject']").send_keys(title_content)    #輸入標題
    sleep(2)
    
    # ---------------------------------------------------------------------------------
    try:
        driver.find_element_by_xpath("//*[@id='e_simple'][text()='高级']").click()     #高級按鈕
        sleep(2)
        driver.find_element_by_xpath("//input[@id='e_switchercheck']").click()     #純文本設定
        sleep(2)
    except:
        pass
    
    
    i = 0
    
    
    
    runtime = len(article_content)
    times = 0
    first_hide = 5
    last_hide = runtime-5
    
    for content in article_content:
        
        if times == first_hide:
            driver.find_element_by_xpath('//*[@id="subject"]').send_keys(Keys.TAB+'[hide]')
            
        if times == last_hide:
            driver.find_element_by_xpath('//*[@id="subject"]').send_keys(Keys.TAB+'[/hide]')
            
        if 'db.forum' in content:
            
            driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/table/tbody/tr[2]/td[2]/div/div[3]/div[1]/div[1]/span/div[2]/input').send_keys(f'/home/docker/Documents/crawler-jkf/images/网路美女/{title_content}/{str(i)}.jpg')
            sleep(2)
                
                
            try:     #避免圖檔太大
                img = driver.find_element_by_xpath(f'//tr//td//a[@title="{i}.jpg"]')
                img = img.get_attribute('id').replace('imageattach','')
                imgur = f'[attachimg]{img}[/attachimg]'
                
                driver.find_element_by_xpath('//*[@id="subject"]').send_keys(Keys.TAB+imgur+Keys.RETURN)
                sleep(2)
            except:
                pass
            
            i+=1
            
            
            sleep(3)
            
        elif '推文章' in content:
            break
        elif '文/' in content:
            break
        elif '文＼' in content:
            break
        elif '▶' == content:
            break
        else:
            content = txt.remove_keywords(r'remove_keywords.txt', content)
            content = content.replace('传送门','')
            
            driver.find_element_by_xpath('//*[@id="subject"]').send_keys(Keys.TAB+'[size=3][font=微软雅黑]'+content+'[/font][/size]'+Keys.RETURN)
            sleep(3)
        times += 1
    driver.find_element_by_xpath('//*[@id="subject"]').send_keys(Keys.TAB+'点击链接回首页看更多相关资讯：\nhttps://forum.17po.cn/')
    sleep(3)
    
    driver.find_element_by_xpath('//button[@id="postsubmit"]').click()        
    # ActionChains(driver).move_to_element(driver.find_element_by_xpath('//button[@id="postsubmit"]')).click().perform()
    sleep(8)
    url = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div[2]/div[1]/div[1]/table[1]/tbody/tr/td/div[1]/span[2]/a').get_attribute('href') 
      
    insert_SQL(title_content, url)



def article_content_ETL(x):
    
    article_content = x.replace("['",'').split("']")
    article_content = [b.strip() for b in article_content]  
    article_content = ''.join(article_content)
    article_content = (re.split('.jpg|.png|http://',article_content))
    
    return article_content
    
    
    
    
    
    

    
if __name__ == '__main__':
    
    
    username = r'admin'
    password = r'admin'
    driver = webdriver.Firefox()
    login_ready_to_post(driver, username, password)
    
    
    title_list = SQL_DATA('网路美女', '')[0]
    article_list = SQL_DATA('网路美女', '')[1]
    
    
    
    for article_content, title in zip(article_list, title_list):
        
        article_content = article_content_ETL(article_content)
        
        auto_post(driver, article_content, title)
                
            
