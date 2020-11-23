# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from datetime import datetime


def toggleData(mode):
    # Click to show option menu
    # filterXpath = '//*[@id="ctl00_ctl36_g_27083341_cf6a_44dd_93e0_4bd660aae4a1"]/div[3]/dl/dt/a'
    filterXpath = '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_divFilterApplied"]'
    driver.find_element_by_xpath(filterXpath).click()
    
    if mode == 'medical':
        # Select filter to Medical clinics
        medClinicsXpath = '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_div_Main_MCO"]'
        # driver.find_element_by_xpath(medClinicsXpath).click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, medClinicsXpath) )).click()
    
    elif mode == 'dental':
        # Select filter to Dental clinics
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_rdo_DC"]') )).click()
    
    elif mode == 'medical-west':
        # Select filter to West Region clinics
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_rdo_REG"]') )).click()
        westCheckBoxXpath = '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_div_REG_West"]/label'
        # driver.find_element_by_xpath(westCheckBoxXpath).click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, westCheckBoxXpath))).click()
    
    elif mode == '24H':
        # Select 24H clinics
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_rdo_MCO"]') )).click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_div_OH"]') )).click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_div_OH_Y"]/label') )).click()
    
    # elif mode == 'FMC':
    #     # Select Family Medicine Clinic
    #     WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_rdo_MCO"]') )).click()
        
    # elif mode == 'CHC':
    #     # Select Community Health Centre
    #     WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_rdo_MCO"]') )).click()
        
    elif mode == 'all':
        # Scrape all clinics
        pass
    
    # Click to apply filter
    applyFilterXpath = '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_DirectoryFilter_btn_Filter"]'
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, applyFilterXpath))).click()
    


if __name__=='__main__':
    driver = webdriver.Chrome('C:/Users/david/Documents/chromedriver/chromedriver.exe')
    
    mode = 'medical' # options: all, medical, dental, medical-west, 24H
    
    http = "https://www.healthhub.sg/directory/clinics-and-polyclinics"
    driver.get(http)
    
    names = []
    addresses = []
    end = False
    
    toggleData(mode)
    
    while(end == False):
        datalistings = driver.find_elements_by_class_name("app_ment")
        for i in range(1, len(datalistings)+1 ):
            xpath = '//*[@id="accordion_browse_map"]/div['+str(i)+']/div[1]/h4/a/span'
            gp = driver.find_element_by_xpath(xpath).text
            name, address = gp.split('\n')
            names.append(name)
            addresses.append(address)
            
        nextArrowXpath = '//*[@id="ctl00_ctl36_g_b711ea8b_c796_44ac_80bf_19dbd5b06247_ctl00_PaginationMain_lnkNextResponsive"]'
        nextExist = driver.find_element_by_xpath(nextArrowXpath).get_attribute("href") ## returns None if there is no href attribute
        if nextExist:
            driver.find_element_by_xpath(nextArrowXpath).click()
        else:
            end = True
    
    df = pd.DataFrame()
    df['Clinic'] = names
    df['Address'] = addresses
    df['Postal Code'] = [add.split()[-1] for add in addresses]
    print(df.shape)
    
    if not os.path.exists("./output"):
        os.mkdir("output")
    df.to_csv(f"./output/GPClinics_{mode}_{datetime.now().date()}.csv", index = False)

    # driver.quit()