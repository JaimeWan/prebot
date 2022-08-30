from lib2to3.pgen2 import driver
import string
from xmlrpc.client import Boolean
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from util.commonUtil import Common
from selenium.webdriver.common.by import *
from time import sleep
import logging

open_url = "http://local.adspower.com:50325/api/v1/browser/start?open_tabs=1&user_id="
activt_url = "http://local.adspower.com:50325/api/v1/browser/active?user_id="
close_url = "http://local.adspower.com:50325/api/v1/browser/stop?user_id="

class discordError(Exception):
    def __init__(self, msg):
        '''
        :param msg: 异常信息
        '''
        self.msg = msg

class discordMain:
  
  #加入discord
  @classmethod
  def discordJoinMain(self, ads_id: string, quit: Boolean,driver):
     var=Common.check_element_exists(By.XPATH,"//button/div",driver)
     a=0
     while var==False:
         if(a>1):
             raise discordError("代理异常，discord无法打开")
         a=a+1
         driver.refresh()
         sleep(2)
         var=Common.check_element_exists(By.XPATH,"//button/div",driver)
         
      
     #检查是否已已进入
     valEle = Common.AutoGetElementWithRefresh(
         By.XPATH, "//button/div", driver)
     print("开始进入discord")
     print(valEle.text)
     if(valEle.text=="接受邀请"):
         Common.AutoClickWithRefresh(
             By.XPATH, "//button/div", driver)
         sleep(5)
     else:
         print("下一个")


  

  #推特Like&Retweet
  @classmethod
  def twitterLikeMain(self, ads_id: string, quit: Boolean,driver):

     #检查是否已完成 已完成则退出
     valFollow = Common.check_element_exists(
         By.XPATH, "//div[@aria-label='已喜欢' or @aria-label='Liked']", driver)
    #  //div[@aria-label='喜欢' or @aria-label='Like']
    # //div[@aria-label='已喜欢' or @aria-label='Liked']
    # //div[@aria-label='转推' or @aria-label='Retweet']
    # //div[@aria-label='已转推' or @aria-label='Retweeted']
     print(valFollow)
     if(valFollow==False):
         Common.AutoClickWithRefresh(
             By.XPATH, "//div[@aria-label='喜欢' or @aria-label='Like']", driver)
         print("twitter喜欢完成")
     else:
         print("twitter已喜欢,下一个")
         
     if(quit):
      requests.get(close_url+ads_id)
