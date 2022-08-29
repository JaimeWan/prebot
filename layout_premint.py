

import string
from xmlrpc.client import Boolean
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys
from util.commonUtil import Common
from selenium.webdriver.common.by import *
from time import sleep
import logging

open_url = "http://local.adspower.com:50325/api/v1/browser/start?open_tabs=1&user_id="
activt_url = "http://local.adspower.com:50325/api/v1/browser/active?user_id="
close_url = "http://local.adspower.com:50325/api/v1/browser/stop?user_id="


class layoutMain:

  @classmethod
  def layout(self,ads_id: string, id: string, quit: Boolean):
  
     resp = requests.get(open_url+ads_id).json()
     if resp["code"] != 0:
         logging.info(resp["msg"])
         logging.info("please check ads_id")
         sys.exit()
  
     chrome_driver = resp["data"]["webdriver"]
     chrome_options = Options()
     chrome_options.add_experimental_option(
         "debuggerAddress", resp["data"]["ws"]["selenium"])
     driver = webdriver.Chrome(chrome_driver, options=chrome_options)

  
     # https://www.premint.xyz/profile/
     #打开premint
    #  driver.execute_script("window.open('https://www.premint.xyz/profile/')")
     driver.get("https://www.premint.xyz/profile/")
     #登出
     Common.AutoClick(By.XPATH,"//*[@id=\"navbar_main\"]/ul[2]/li[2]/div/a[3]",driver)
     #点击登录
     Common.AutoClick(By.XPATH,"//*[@id=\"navbar_main\"]/ul[2]/li[1]/a",driver)
     #点击discord登录
     Common.AutoClick(By.XPATH,"//*[@id=\"st-container\"]/div/div/div/section/div/div/div/a[2]",driver)
     sleep(3)
     #点击授权
     Common.AutoClick(By.XPATH,"//*[@id=\"app-mount\"]/div[2]/div/div[1]/div/div/div/div/div/div[2]/button[2]",driver)
     sleep(3)
     #点击profile
     Common.AutoClick(By.XPATH,"//*[@id=\"navbar_main\"]/ul[2]/li[2]/div/a[1]",driver)
     #点击disconnect
     Common.AutoClick(By.XPATH,"//*[@id=\"st-container\"]/div/div/div/section/div/div/div/div/div/div[2]/div[1]/div[9]/div/a",driver)
     #点击选择discord
     Common.AutoClick(By.XPATH,"//span[text()='Discord']",driver)
     #点击remove
     Common.AutoClick(By.XPATH,"//*[@id=\"st-container\"]/div/div/div/section/div/div/div/div[2]/div/form/fieldset/div[3]/button",driver)
     #登出
     Common.AutoClick(By.XPATH,"//*[@id=\"navbar_main\"]/ul[2]/li[2]/div/a[3]",driver)
     
     logging.info(id+"discored解绑premint完成")
     if(quit):
      requests.get(close_url+ads_id)


  @classmethod
  def loginValid(self,driver):
      # https://www.premint.xyz/profile/
  
      driver.switch_to.window(driver.window_handles[1])
      driver.refresh()
      val = Common.check_element_exists(
          By.XPATH, "//*[@id=\"navbarAccount\"]", driver)
      if(val == False):
       logging.info("登录检查不通过")
      return val

  @classmethod
  def popUpAllow(self,ads_id: string, id: string, quit: Boolean):
 
     resp = requests.get(open_url+ads_id).json()
     if resp["code"] != 0:
         logging.info(resp["msg"])
         logging.info("please check ads_id")
         sys.exit()
  
     chrome_driver = resp["data"]["webdriver"]
     chrome_options = Options()
     chrome_options.add_experimental_option(
         "debuggerAddress", resp["data"]["ws"]["selenium"])
     driver = webdriver.Chrome(chrome_driver, options=chrome_options)

  
     # https://www.premint.xyz/profile/
     #打开premint
    #  driver.execute_script("window.open('https://www.premint.xyz/profile/')")
     driver.get("chrome://settings/content/popups")  
     print(Common.check_element_exists(By.XPATH,"//*[@id='button']",driver))
     
     
     
  @classmethod
  def test(self,ads_id: string, id: string, quit: Boolean):
 
     resp = requests.get(open_url+ads_id).json()
     if resp["code"] != 0:
         logging.info(resp["msg"])
         logging.info("please check ads_id")
         sys.exit()
  
     chrome_driver = resp["data"]["webdriver"]
     chrome_options = Options()
     chrome_options.add_experimental_option(
         "debuggerAddress", resp["data"]["ws"]["selenium"])
     driver = webdriver.Chrome(chrome_driver, options=chrome_options)
     driver.set_page_load_timeout(10)
     driver.set_script_timeout(1)
  
     # https://www.premint.xyz/profile/
     #打开premint
    #  driver.execute_script("window.open('https://www.premint.xyz/profile/')")
     driver.get("chrome://settings/content/popups")  
     temp = "window.open('https://www.premint.xyz/beowulfnft/')"
     try:
      driver.execute_script(temp) 
     except:
      driver.execute_script("window.stop()")   
     print("测试完成")  

layoutMain.test("j3byfbe","125",False)  
# layoutMain.layout("j3byfaj","95",False)
# layoutMain.layout("j3byfak","96",False)
# layoutMain.layout("j3byfal","97",False)
# layoutMain.layout("j3byfam","98",False)
# layoutMain.layout("j3byfan","99",False)
# layoutMain.layout("j3byfao","100",False)
# layoutMain.layout("j3byfaq","102",False)
# layoutMain.layout("j3byfar","103",False)
# layoutMain.layout("j3byfas","104",False)
# layoutMain.layout("j3byfau","106",False)
# layoutMain.layout("j3byfav","107",False)
# layoutMain.layout("j3byfaw","108",False)
# layoutMain.layout("j3byfax","109",False)
# layoutMain.layout("j3byfay","110",False)
# layoutMain.layout("j3byfb0","111",False)
# layoutMain.layout("j3byfb1","112",False)