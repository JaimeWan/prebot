from loguru import logger
import string
from xmlrpc.client import Boolean
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sys
from util.commonUtil import Common
from selenium.webdriver.common.by import *
from time import sleep


open_url = "http://local.adspower.com:50325/api/v1/browser/start?open_tabs=1&user_id="
activt_url = "http://local.adspower.com:50325/api/v1/browser/active?user_id="
close_url = "http://local.adspower.com:50325/api/v1/browser/stop?user_id="


class twitterError(Exception):
    def __init__(self, msg):
        '''
        :param msg: 异常信息
        '''
        self.msg = msg

class twitterMain:

  #推特关注
  @classmethod
#   @logger.catch
  def twitterFollowMain(self, ads_id: string, quit: Boolean, driver):
      
      valOpen2 = Common.check_element_exists(
            By.XPATH, "//div[contains(text(),'推文') or contains(text(),'Tweets')]", driver,2,0.5)
      if(valOpen2==False):
          raise twitterError("代理异常，推特无法打开")
      #检查是否已完成 已完成则退出
      valFollow = Common.check_element_exists(
          By.XPATH, "//span[text()='Follow']", driver)
      if(valFollow==False):
          logger.debug("序号：{}，Following={}，跳过".format(ads_id,valFollow))
          return
      sleep(2)
      try:
        Common.AutoClickWithRefresh(
           By.XPATH, "//span[text()='Follow']", driver)
        logger.debug("twitter关注完成")
        if(quit):
         requests.get(close_url+ads_id)
      except Exception as e:
        logger.debug("序号：{},twitter关注出错,重试".format(ads_id))  
        logger.error(e)  
        self.twitterFollowMain(ads_id=ads_id, quit=quit, driver=driver)
        



    #  //div[@aria-label='喜欢' or @aria-label='Like']
    # //div[@aria-label='已喜欢' or @aria-label='Liked']
    # //div[@aria-label='转推' or @aria-label='Retweet']
    # //div[@aria-label='已转推' or @aria-label='Retweeted']

  #推特Like

  @classmethod
  @logger.catch
  def twitterLikeMain(self, ads_id: string, quit: Boolean, driver):
      #检查是否正常打开页面
    #   valOpen = Common.check_element_exists(
    #         By.XPATH, "//*[@id='react-root']/div/div/div[2]/header", driver,2,0.5)
    #   if(valOpen==False):
    #       raise twitterError("代理异常，推特无法打开")
      valOpen2 = Common.check_element_exists(
            By.XPATH, "//article", driver,2,0.5)
      if(valOpen2==False):
          raise twitterError("代理异常，推特无法打开")
       #检查是否已完成 已完成则退出
      valLike = Common.check_element_existsNoRefresh(
          By.XPATH, "//div[@aria-label='已喜欢' or @aria-label='Liked']", driver)
        
      if(valLike==False):
          logger.debug("序号：{},Liked={},开始retweet".format(ads_id,valLike))
          sleep(2)
          try:
            logger.debug("twitter")  
            Common.AutoClickWithRefresh(
                By.XPATH, "//div[@aria-label='喜欢' or @aria-label='Like']", driver)
            logger.debug("twitter喜欢完成")
            if(quit):
             requests.get(close_url+ads_id)
          except Exception as e:
            logger.debug("序号：{},twitter点赞出错,重试".format(ads_id))    
            logger.error(e)
            self.twitterLikeMain(ads_id=ads_id, quit=quit, driver=driver)
                #检查是否已完成 已完成则退出
      valRetweet = Common.check_element_existsNoRefresh(
              By.XPATH, "//div[@aria-label='已转推' or @aria-label='Retweeted']", driver)
        
      sleep(2)
      if(valRetweet==False):
        logger.debug("序号：{},Retweeted={},开始retweet".format(ads_id,valRetweet))
        try:
           Common.AutoClickWithRefresh(
               By.XPATH, "//div[@aria-label='转推' or @aria-label='Retweet']", driver)
           sleep(1)
           Common.AutoClickWithRefresh(
               By.XPATH, "//div[@data-testid='retweetConfirm']", driver)
           logger.debug("twitter转发完成")
           if(quit):
            requests.get(close_url+ads_id)
        except Exception as e:
            logger.debug("序号：{},twitter转发出错,重试".format(ads_id))
            self.twitterLikeMain(ads_id=ads_id, quit=quit, driver=driver) 

  


  #推特Retweet

  @classmethod
  @logger.catch
  def twitterRetweetMain(self, ads_id: string, quit: Boolean, driver):
      #检查是否正常打开页面
      valOpen = Common.check_element_exists(
            By.XPATH, "//*[@id='react-root']/div/div/div[2]/header", driver,2,0.5)
      if(valOpen==False):
          raise twitterError("代理异常，推特无法打开")
      
      #检查是否已完成 已完成则退出
      valRetweet = Common.check_element_exists(
          By.XPATH, "//div[@aria-label='已转推' or @aria-label='Retweeted']", driver)
  
      if(valRetweet):
          logger.debug("序号：{},Retweeted={}，跳过".format(ads_id,valRetweet))
          return
      sleep(2)
      try:
         Common.AutoClickWithRefresh(
             By.XPATH, "//div[@aria-label='转推' or @aria-label='Retweet']", driver)
         sleep(1)
         Common.AutoClickWithRefresh(
             By.XPATH, "//div[@data-testid='retweetConfirm']", driver)
         logger.debug("twitter转发完成")
         if(quit):
          requests.get(close_url+ads_id)
      except Exception as e:
          logger.debug("序号：{},twitter转发出错,重试".format(ads_id))
          self.twitterRetweetMain(ads_id=ads_id, quit=quit, driver=driver)


  @classmethod
  @logger.catch
  def twitterTaskMain(self, ads_id: string, link: string, type: string, content: string, quit: Boolean):
     #打开网页
     resp = requests.get(open_url+ads_id).json()
     if resp["code"] != 0:
         print(resp["msg"])
         print("please check ads_id")
         sys.exit()

     chrome_driver = resp["data"]["webdriver"]
     chrome_options = Options()
     chrome_options.add_experimental_option(
         "debuggerAddress", resp["data"]["ws"]["selenium"])
     driver = webdriver.Chrome(chrome_driver, options=chrome_options)

     #https://www.premint.xyz/profile/
     #打开premint
     #driver.execute_script("window.open('https://twitter.com/PUMA')")
     driver.get(link)
     if(type == 'follow'):
         logger.debug(ads_id+":开始follow")
         self.twitterFollowMain(ads_id, link, quit, driver)

     if(type == 'loginCheck'):
         logger.debug(ads_id+":检查登录")
         self.dailyLogin(ads_id=ads_id, quit=quit, driver=driver)

  @classmethod
  #   todo
  def dailyLogin(self, ads_id: string, quit: Boolean):

     #打开网页
     resp = requests.get(open_url+ads_id).json()
     if resp["code"] != 0:
         print(resp["msg"])
         print("please check ads_id")
         sys.exit()

     chrome_driver = resp["data"]["webdriver"]
     chrome_options = Options()
     chrome_options.add_experimental_option(
         "debuggerAddress", resp["data"]["ws"]["selenium"])
     driver = webdriver.Chrome(chrome_driver, options=chrome_options)
     driver.get("https://twitter.com/home")
     sleep(3)
     #检查是否已登录 已登录则退出
     valFollow = Common.check_element_exists(
         By.XPATH, "//*[@id='react-root']/div/div/div[2]/header", driver)
     if(valFollow):
         driver.refresh()
         logger.debug(ads_id+":twitter正常")
     else:
         logger.error(ads_id+":twitter异常")
     if(quit & valFollow):
      requests.get(close_url+ads_id)


# twitterMain.twitterFollowtMain("j3byl5s","158",False)
# twitterMain.twitterFollowtMain("j3byl5t","159",False)
# twitterMain.twitterFollowtMain("j3byl5u","160",False)
# twitterMain.twitterFollowtMain("j3byl5v","161",False)
# twitterMain.twitterFollowtMain("j3byl5w","162",False)
# twitterMain.twitterFollowtMain("j3byl5x","163",False)
# twitterMain.twitterFollowtMain("j3byl5y","164",False)
# twitterMain.twitterFollowtMain("j3byl60","165",False)
# twitterMain.twitterFollowtMain("j3byl61","166",False)
# twitterMain.twitterFollowtMain("j3byl62","167",False)
