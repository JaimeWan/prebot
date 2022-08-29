
import string
import requests,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sys
from util.commonUtil import Common
from selenium.webdriver.common.by import *
from time import sleep
import logging



open_url = "http://local.adspower.com:50325/api/v1/browser/start?open_tabs=1&user_id="
activt_url="http://local.adspower.com:50325/api/v1/browser/active?user_id="
close_url = "http://local.adspower.com:50325/api/v1/browser/stop?user_id="




class  metamaskMain:
  
  @staticmethod
  def accountImport(ads_id:string,word:string):
      
   resp = requests.get(open_url+ads_id).json()
   if resp["code"] != 0:
       logging.info(resp["msg"])
       logging.info("please check ads_id")
       sys.exit()

   chrome_driver = resp["data"]["webdriver"]
   chrome_options = Options()
   chrome_options.add_experimental_option("debuggerAddress", resp["data"]["ws"]["selenium"])
   driver = webdriver.Chrome(chrome_driver, options=chrome_options)
   logging.info(driver.title)
   
   driver.get("chrome-extension://ogibelfbcbolpcdjhakooclfjgndogld/home.html#initialize/welcome") # 打开新标签open_tabs
#    driver.execute_script("window.open('chrome-extension://mgggfedbbijejgpkdojogaclbehnoepl/home.html#initialize/create-password/import-with-seed-phrase')") # 打开新标签open_tabs
   
#    //*[@id="app-content"]/div/div[2]/div/div/div/button
   Common.AutoClick(By.XPATH,"//*[@id=\"app-content\"]/div/div[2]/div/div/div/button",driver)
#    //*[@id="app-content"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]
   Common.AutoClick(By.XPATH,"//*[@id=\"app-content\"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button",driver)
#    //*[@id="app-content"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/button
   Common.AutoClick(By.XPATH,"//*[@id=\"app-content\"]/div/div[2]/div/div/div/div[5]/div[1]/footer/button[2]",driver)
   
   Common.setText(word)
   # //*[@id="import-srp__srp-word-0"]
   cr = Common.AutoGetElement(By.XPATH,"//*[@id=\"import-srp__srp-word-0\"]",driver)
   # cr = Common.AutoGetElement(By.XPATH,"//*[@id=\"app-content\"]/div/div[2]/div/div/div[2]/form/div[1]/div[3]/div[1]/div[1]",driver)
   logging.info(type(cr))
   cr.click()
   cr.send_keys(Keys.CONTROL,'v')
   
   # //*[@id="password"]
   Common.AutoInput(By.XPATH,"//*[@id=\"password\"]","w7217459",driver)
   # //*[@id="confirm-password"]
   Common.AutoInput(By.XPATH,"//*[@id=\"confirm-password\"]","w7217459",driver)
   
   # //*[@id="create-new-vault__terms-checkbox"]
   
   Common.AutoClick(By.XPATH,"//*[@id=\"create-new-vault__terms-checkbox\"]",driver)
   # //*[@id="app-content"]/div/div[2]/div/div/div[2]/form/button
   Common.AutoClick(By.XPATH,"//*[@id=\"app-content\"]/div/div[2]/div/div/div[2]/form/button",driver)
#    //*[@id="app-content"]/div/div[2]/div/div/button
   Common.AutoClick(By.XPATH,"//*[@id=\"app-content\"]/div/div[2]/div/div/button",driver)
   sleep(5)
   requests.get(close_url+ads_id)
