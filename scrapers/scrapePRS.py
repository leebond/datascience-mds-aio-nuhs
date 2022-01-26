# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 09:42:02 2019

@author: david
"""

import re
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
driver = webdriver.Chrome('C:/Users/david/Documents/chromedriver/chromedriver.exe')
http = "https://prs.moh.gov.sg/prs/internet/profSearch/mshowSearchSummaryByName.action?hpe=SMC"
driver.get(http)

WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="getSearchSummary"]/div[3]/div[1]/fieldset/div/div/fieldset/div[4]/button') )).click()


df = pd.DataFrame(columns=['Doctor', 'MRN', 'Type of Register',  'First Registration Type', \
                           'First Registration Date', 'Current Registration Type', \
                           'Current Registration Date', 'Practising Certificate Start Date' , \
                           'Practising Certificate End Date', 'Register of Specialists Entry Date', \
                           'Register of Family Physician Entry Date', \
                           'Primary Place of Practice', 'Address of Practice', 'Telephone'])

df_qualifications = pd.DataFrame() # columns=['MRN', 'Qualification']

end = False
cnt = 0  

def splitNameMRN(text):
    try:
        mrnRegex = re.search(r"M\w?\d+\w?", text)
        mrn = mrnRegex.group()
        mIndex = mrnRegex.span()[0]
        name = text[0: (mIndex - 2)] # -2 to skip ( and a whitespace
        return name, mrn
    except:
        return None, None

def splitTextDate(text):
    try:
        dateReg = re.search(r"\w{2}\/\w{2}\/\w{4}", text)
        date = dateReg.group()
        dateIndex = dateReg.span()[0]
        otherText = text[0: (dateIndex - 2)]
        return otherText, date
    except:
        return None, None

def splitOneParentheses(text):
    mainText, dateText = text.split('(')
    dateText = dateText[1][:-1]
    return mainText, dateText


def getIndexOfNextButton(elements):
#    print([e.text for e in elements])
    try:
        nextIndex = [e.text for e in elements].index('Next')
        return nextIndex
    except ValueError:
        return

def cleanText(text):
    return re.sub(r'[^A-Za-z0-9]+', ' ', text)

def parseQualification(qualificationsData):
    if len(qualificationsData) > 1:
        q = [cleanText(q).strip() for q in qualificationsData]
        table = list(itertools.product([mrn], q))
    else:
        q = qualificationsData[0]
        q = cleanText(q).strip()
        table = list(itertools.product([mrn], [q]))
    return table

def parseData(data):
    mylist = data.split('\n')
#    print(mylist)
    dataschema = ['Qualifications', 'Type of first registration / date', 'Type of current registration / date', \
              'Practising Certificate Start Date', 'Practising Certificate End Date', 'Specialty / Entry date into the Register of Specialists', \
              'Entry date into Register of Family Physicians', 'Department / Name of Practice Place', \
              'Address of Place of Practice', 'Tel']

    firstRegDateIndex = 0
    addressOfPracticeIndex = 0
    telIndex = 0
    dataOutput = []
    for col in dataschema:
        
        try:
            colIndex = mylist.index(col)+1
            if col == 'Type of first registration / date':
                firstRegDateIndex = colIndex
            elif col == 'Address of Place of Practice':
                addressOfPracticeIndex = colIndex
            elif col == 'Tel':
                telIndex = colIndex
        except ValueError: ## when col is not in list
            if col == 'Specialty / Entry date into the Register of Specialists':
                colIndex = mylist.index('Sub-Specialty / Entry date into the Register of Specialists')+1
            else:
                colIndex = None
        
        if colIndex != None:
            colData = mylist[colIndex]
            if col == 'Type of first registration / date' and firstRegDateIndex > 3: ## means 'Type of first registration / date' has index greater than 3 
                qualifications = parseQualification(mylist[1: (firstRegDateIndex-1)])
                colData = qualifications
                firstRegDate = mylist[firstRegDateIndex]
                dataOutput.pop()
                dataOutput.append(colData)
                dataOutput.append(firstRegDate)
            elif col == 'Type of first registration / date' and firstRegDateIndex <= 3:
                qualifications = parseQualification([mylist[1]])
                colData = qualifications
                firstRegDate = mylist[firstRegDateIndex]
                dataOutput.pop()
                dataOutput.append(colData)
                dataOutput.append(firstRegDate)
            elif col == 'Tel' and addressOfPracticeIndex < (telIndex-1):
                addressOfPractice = mylist[addressOfPracticeIndex: (telIndex-1)]
                addressOfPractice = ' '.join(addressOfPractice)
                addressOfPractice = cleanText(addressOfPractice).strip()
                colData = addressOfPractice
                tel = mylist[telIndex]
                dataOutput.pop()
                dataOutput.append(colData)
                dataOutput.append(tel)
            else:
                dataOutput.append(colData)
        else:
            dataOutput.append(None)
    return dataOutput

def getAllData(xpath):
    try:
        allData = driver.find_element_by_xpath(xpath).text
        return allData
    except:
        driver.implicitly_wait(10)

while (end == False):
    result_listings = driver.find_elements_by_class_name('ui-li-heading') # 10
#    print(len(result_listings))
    for i in range(1, len(result_listings)+1 ):
        docXpath = '//*[@id="result"]/fieldset/li['+str(i)+']/div/h3'
        doc = driver.find_element_by_xpath(docXpath).text
        docName, mrn = splitNameMRN(doc)
        typeOfRegisterXpath = '//*[@id="result"]/fieldset/li['+str(i)+']/div/p/span[2]'
        typeOfRegister = driver.find_element_by_xpath(typeOfRegisterXpath).text
        moreDetailsXpath = '//*[@id="result"]/fieldset/li['+str(i)+']/div/p/a'
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, moreDetailsXpath) )).click()

        allDataXpath = '//*[@id="searchDetails"]/div[3]/div/fieldset/div/div/fieldset/div'
        
        allData = getAllData(allDataXpath)

        qualifications, firstReg, currentReg, pracCertStartDate, pracCertEndDate, \
        regSpecEntryDate, regFamPhyEntryDate, placeOfPractice, addressOfPractice, tel = parseData(allData)
#        print(parseData(allData))
        
        firstRegType, firstRegDate = splitTextDate(firstReg)
        currentRegType, currentRegDate = splitTextDate(currentReg)
        
        df = df.append({'Doctor': docName, 'MRN': mrn, 'Type of Register': typeOfRegister, \
                   'First Registration Type': firstRegType, 'First Registration Date': firstRegDate, \
                   'Current Registration Type': currentRegType, \
                   'Current Registration Date': currentRegDate, \
                   'Practising Certificate Start Date': pracCertStartDate, \
                   'Practising Certificate End Date': pracCertEndDate, \
                   'Register of Specialists Entry Date': regSpecEntryDate, \
                   'Register of Family Physician Entry Date': regFamPhyEntryDate, \
                   'Primary Place of Practice': placeOfPractice, \
                   'Address of Practice': addressOfPractice, 'Telephone': tel}, ignore_index=True)
        
        df_qualifications = df_qualifications.append(qualifications)
                
        if cnt % 100 == 0:
            print(cnt)
        cnt += 1
        driver.back()

    elements = driver.find_elements_by_class_name('pagination')
    indexNext = getIndexOfNextButton(elements)
#    print(indexNext)
    if indexNext == None:
        end = True
    else:
        nextButtonXpath = '//*[@id="result"]/table/tbody/tr/td/a[' + str(indexNext+1) + ']'
#        driver.execute_script("arguments[0].scrollIntoView();", element)
        WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, nextButtonXpath) )).click()


print(df.shape)
driver.quit()
df.to_csv("Practitioners.csv", index = False)
df_qualifications.columns = ['MRN', 'Qualification']
df_qualifications.to_csv("PractitionersQualifications.csv", index = False)