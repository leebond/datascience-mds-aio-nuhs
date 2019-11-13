# -*- coding: utf-8 -*-
"""
Created on Wed Oct 30 09:22:42 2019

@author: david
"""
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
driver = webdriver.Chrome('C:/Users/david/Documents/chromedriver/chromedriver.exe')

http = "http://hcidirectory.sg/hcidirectory/"
driver.get(http)

def getNumbers(data):
    return re.findall(r'[0-9]+', data)

def splitContactNum(contact):
    try:
        tel, fax = contact.split('\n')
        tel = getNumbers(tel)[0]
        fax = getNumbers(fax)[0]
        return tel, fax
    except ValueError:
        tel = getNumbers(contact)[0]
        return tel, None


df = pd.DataFrame(columns=['Clinic', 'Address', 'Telephone', 'Fax', 'Operating Hours'])
end = False
cnt = 0
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="moreSearchOptions"]') )).click()
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="criteria"]/table/tbody/tr[2]/td/label') )).click()
WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="search_btn_left"]') )).click()

while (end == False):
    result_listings = driver.find_elements_by_class_name('name')
    for i in range(3, len(result_listings)+1 ):
        GPnameXpath = '//*[@id="results"]/div/div[' + str(i) + ']/div[1]/span[1]'
        GPname = driver.find_element_by_xpath(GPnameXpath).text
        contactXpath = '//*[@id="results"]/div/div[' + str(i) + ']/div[1]/span[2]'
        contact = driver.find_element_by_xpath(contactXpath).text
        tel, fax = splitContactNum(contact)
        addressXpath = '//*[@id="results"]/div/div[' + str(i) + ']/div[2]/span'
        address = driver.find_element_by_xpath(addressXpath).text
        operatingHrsXpath = '//*[@id="results"]/div/div[' + str(i) + ']/div[3]/span'
        operatingHrs = driver.find_element_by_xpath(operatingHrsXpath).text
#        print(GPname, address)
        df = df.append({'Clinic': GPname, 'Address': address, 'Telephone': tel, 'Fax': fax, 'Operating Hours': operatingHrs}, ignore_index=True)
        if cnt % 100 == 0:
            print(cnt)
        cnt += 1
    
    nextArrow = '//*[@id="PageControl"]/div[2]'
    nextArrowClass = driver.find_element_by_xpath(nextArrow).get_attribute("class") ## returns 'r_arrow' or 'r_arrow_none' if element cannot be found

    if nextArrowClass == 'r_arrow_none':
        end = True
    elif nextArrowClass == 'r_arrow':
#        driver.execute_script("arguments[0].scrollIntoView();", driver.find_element_by_xpath(nextArrow))
#        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, nextArrow) ))
#        driver.execute_script("arguments[0].click();", driver.find_element_by_xpath(nextArrow))
        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.XPATH, nextArrow) )).click()


print(df.shape)
driver.quit()
df.to_csv("GPClinicsHCI.csv", index = False)