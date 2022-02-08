import random
from time import sleep
import pandas as pd
from selenium import webdriver

'''
El dataframe de salida deberá contener los siguientes campos:
Post,Caption,Date,likesComment,IdFatherComment,IdChildComment,Username
IdFatherComment es el id de un comment_base directo al posts y IdChildComment es el id de un comment_base hecho sobre otro comment_base
'''

driver = webdriver.Chrome('./chromedriver.exe')

driver.get('http://www.instagram.com/p/B166OkVBPJR/')

xpath_button =  '//ul[contains(@class, "XQXOT")]//div[contains(@class, "NUiEW")]/button'
button = driver.find_element_by_xpath(xpath_button)
for i in range(round(1480/15)):
    try:
        button.click()
        sleep(random.uniform(8.0, 10.0))
        button = driver.find_element_by_xpath(xpath_button)
    except:
        break

comments = driver.find_elements_by_xpath('//ul[contains(@class, "Mr508 ")]')
data = []

for comment in comments:
    comment_base = comment.find_elements_by_xpath('.//div[contains(@class, "C4VMK")]/span')[0]
    date = comment.find_elements_by_xpath('.//a[contains(@class, "gU-I7")]/time')[0]
    username = comment.find_elements_by_xpath('.//div[contains(@class, "C4VMK")]//h3[contains(@class, "_6lAjh ")]//div[contains(@class, "ItkAi")]')[0]
    likes_element = comment.find_elements_by_xpath('.//div[contains(@class, "uL8Hv")]/button')[0]
    list_likes = likes_element.text.split(' ')
    likes_count = '0'
    if list_likes[-1] == 'gusta' or list_likes[-1] == 'like':
        likes_count = list_likes[0]
    
    data.append([
        comment_base.text, 
        comment_base.parent.title,
        date.get_attribute("datetime"), 
        likes_count, 
        0, 
        comment_base.id, 
        username.text
    ])

df = pd.DataFrame(data,
                  columns=['Post', 'Caption', 'Date', 'likesComment', 'IdFatherComment', 'IdChildComment', 'Username'])
df.to_csv('comments.csv', index=False)

sleep(1)
driver.quit()