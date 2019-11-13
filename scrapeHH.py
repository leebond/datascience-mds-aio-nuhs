# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
driver = webdriver.Chrome('C:/Users/david/Documents/chromedriver/chromedriver.exe')

http = "https://www.healthhub.sg/directory/clinics-and-polyclinics"
driver.get(http)

names = []
addresses = []
end = False

# Click to show option menu
filterXpath = '//*[@id="ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1"]/div[3]/dl/dt/a'
driver.find_element_by_xpath(filterXpath).click()

# Select filter to Medical clinics
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1_ctl00_DirectoryFilter_rdo_MCO") )).click()
    
# Select filter to Dental clinics
#WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1_ctl00_DirectoryFilter_rdo_DC") )).click()

# Select filter to West Region clinics
#WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1_ctl00_DirectoryFilter_rdo_REG") )).click()
#westCheckBoxXpath = '//*[@id="ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1_ctl00_DirectoryFilter_div_REG_West"]/label'
#driver.find_element_by_xpath(westCheckBoxXpath).click()

# Select 24H clinics
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1_ctl00_DirectoryFilter_div_OH") )).click()
WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.ID, "ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1_ctl00_DirectoryFilter_div_OH_Y") )).click()

# Click to apply filter
applyFilterXpath = '//*[@id="ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1_ctl00_DirectoryFilter_btn_Filter"]'
driver.find_element_by_xpath(applyFilterXpath).click()

while(end == False):
    datalistings = driver.find_elements_by_class_name("app_ment")
    for i in range(1, len(datalistings)+1 ):
        xpath = '//*[@id="accordion_browse_map"]/div['+str(i)+']/div[1]/h4/a/span'
        gp = driver.find_element_by_xpath(xpath).text
        name, address = gp.split('\n')
        names.append(name)
        addresses.append(address)
        
    nextArrow = '//*[@id="ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1_ctl00_PaginationMain_lnkNextResponsive"]'
    nextExist = driver.find_element_by_xpath(nextArrow).get_attribute("href") ## returns None if there is no href attribute
    if nextExist != None:
        driver.find_element_by_xpath(nextArrow).click()
    else:
        end = True

df = pd.DataFrame()
df['Clinic'] = names
df['Address'] = addresses
print(df.shape)
driver.quit()
df.to_csv("GPClinics24H.csv", index = False)