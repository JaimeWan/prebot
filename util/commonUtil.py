import re
import string
from time import sleep
from xmlrpc.client import Boolean
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common import by
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import win32clipboard as w
import win32con
from loguru import logger

second = 5

# logger.add(".log/commonUtil.log", format="{time} | {level} | {name} | {message}", level="DEBUG",
#            rotation="1 KB", retention="10 seconds", encoding="utf-8", backtrace=True, diagnose=True)


class Common:

  @classmethod
  def closeAds(self, ads_id: string):
    close_url = "http://local.adspower.com:50325/api/v1/browser/stop?user_id="
    resp = requests.get(close_url+ads_id).json()
    if resp["code"] != 0:
        logger.error(resp["msg"])
        logger.error("ads关闭失败.重试")
        sleep(1)
        if(resp["msg"]!="User_id is not open"):
         self.closeAds(ads_id)
    else:
        logger.info("ads关闭成功")
        return

  @staticmethod
  def setText(aString):
      # 打开剪贴板
      w.OpenClipboard()
      # 清空剪贴板
      w.EmptyClipboard()
      # 将数据astring写入剪贴板中
      w.SetClipboardData(win32con.CF_UNICODETEXT, aString)
      # 关闭剪贴板
      w.CloseClipboard()

  @staticmethod
  def gettext():
      w.OpenClipboard()
      t = w.GetClipboardData(win32con.CF_TEXT)
      w.CloseClipboard()
      return t.decode('UTF-8')

  @classmethod
  def AutoClick(self, method: By, param: string, driver):  # 自动点击
    button = self.tryGetElemetTwice(method, param, driver)
    # button = WebDriverWait(driver, second, 1).until(EC.presence_of_element_located((method, param)))
    driver.execute_script("arguments[0].click();", button)

  @classmethod
  def AutoClickWithRefresh(self, method: By, param: string, driver):  # 自动点击
    button = self.tryGetElemetTwiceWithRefresh(method, param, driver)
    if(button is None):
      logger.debug("获取元素失败："+param)
    driver.execute_script("arguments[0].click();", button)

  @classmethod
  def validElementContains(self, method: By, param: string, driver):

    temp = True
    a = 0
    while (a < 2) & temp:
       try:
         #todo 未捕获到就刷新，后面可以改
         WebDriverWait(driver, second, 0.5).until(
             EC.presence_of_element_located((method, param))
         )
         temp = False
         a = a+2
       except Exception:
         a = a+1

  @classmethod
  def AutoGetElement(self, method: By, param: string, driver):
    element = self.tryGetElemetTwice(method, param, driver)

    return element

  @classmethod
  def AutoGetElementWithRefresh(self, method: By, param: string, driver):
    element = self.tryGetElemetTwiceWithRefresh(method, param, driver)

    return element

  @classmethod
  def AutoGetElements(self, method: By, param: string, driver):
    elements = self.tryGetElemetsTwice(method, param, driver)
    return elements

  @classmethod
  def AutoInput(self, method: By, param: string, content, driver):
     element = self.tryGetElemetTwice(method, param, driver)
     element.clear()
     element.send_keys(content)

  @classmethod
  def tryGetElemetTwice(self, method: By, className: string, driver ,num=5,waitTimes=1):
    temp = True
    a = 0
    element = None
    while (a < num) & temp:
       try:
         #todo 未捕获到就刷新，后面可以改
         element = WebDriverWait(driver, second, waitTimes).until(
             EC.presence_of_element_located((method, className))
         )
         temp = False
         a = a+num
       except Exception:
         a = a+num
    return element

  @classmethod
  def tryGetElemetTwiceWithRefresh(self, method: By, className: string, driver,num=5,waitTimes=1):
    temp = False
    a = 0
    element = None
    while (a < num):
       if(temp == True):
         a = a+num
       try:
         element = WebDriverWait(driver, second, waitTimes).until(
             EC.presence_of_element_located((method, className))
         )
         if(element is not None):
          temp = True
          a = a+num
       except Exception:
         logger.debug("未找到元素:{}，执行刷新后重试".format(className))
         driver.refresh()
         a = a+1
    return element

  @classmethod
  def tryGetElemetsTwice(self, method: By, className: string, driver):
    temp = True
    a = 0
    elements = None
    while (a < 2) & temp:

       try:
         #todo 未捕获到就刷新，后面可以改
         logger.debug("check:"+className)
         elements = WebDriverWait(driver, second,1).until(
             EC.presence_of_all_elements_located((method, className))
         )
         temp = False
         a = a+2
       except Exception:
         a = a+1
    return elements

  @classmethod
  def check_element_exists(self, method: By, param: string, driver,num=5,waitTimes=1):
    var = self.tryGetElemetTwiceWithRefresh(method, param, driver,num,waitTimes)
    if(var is None):
      return False
    else:
      return True

  @classmethod
  def check_element_existsNoRefresh(self, method: By, param: string, driver,num=5,waitTimes=1):
    var = self.tryGetElemetTwice(method, param, driver,num,waitTimes)
    if(var is None):
      return False
    else:
      return True

   #检查页面正常打开 未找到元素则抛错
  @classmethod
  def checkAndExceptein(self, method: By, param: string,  driver):
    var = self.tryGetElemetTwiceWithRefresh(method, param, driver)
    logger.debug("check:"+param)
    if(var is None):
       logger.debug("check False:"+param)
       raise Exception('未找到元素：{}'.format(param))
     
     
   #检查页面正常打开
  @classmethod
  def checkAndRefresh(self, method: By, param: string, flag: Boolean, driver):
     var = self.tryGetElemetTwiceWithRefresh(method, param, driver)
     logger.debug("check:"+param)
     if(var is None):
       logger.debug("check False:"+param)
       return False
     else:
       logger.debug("check True:"+param)
       return True



