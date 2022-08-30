
from os import link
from typing import List
from loguru import logger
import string
from xmlrpc.client import Boolean
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import sys
from taskUtils.discord_main import discordMain,discordError
from taskUtils.twitter_main import twitterError, twitterMain
from util.commonUtil import Common
from selenium.webdriver.common.by import *
from selenium.common import TimeoutException
from time import sleep
from widgetModel import *
from globalvar import exception_data




# logger.add(".log/premintMain.log", format="{time} | {level} | {name} | {message}", level="DEBUG",
#            rotation="1 KB", encoding="utf-8",enqueue=True, backtrace=True, diagnose=True)



open_url = "http://local.adspower.com:50325/api/v1/browser/start?open_tabs=1&headless=1&user_id="
activt_url = "http://local.adspower.com:50325/api/v1/browser/active?user_id="
close_url = "http://local.adspower.com:50325/api/v1/browser/stop?user_id="



class premintMain:

  @classmethod
  def linkWalletMain(self, ads_id: string, id: string, quit: Boolean):

     resp = requests.get(open_url+ads_id).json()
     if resp["code"] != 0:
         logger.info(resp["msg"])
         logger.info("please check ads_id")
         sys.exit()

     chrome_driver = resp["data"]["webdriver"]
     chrome_options = Options()
     chrome_options.add_experimental_option(
         "debuggerAddress", resp["data"]["ws"]["selenium"])
     driver = webdriver.Chrome(chrome_driver, options=chrome_options)

     #打开并解锁metamask
     self.openMetamask(driver)

     # https://www.premint.xyz/profile/
     #打开premint
     driver.execute_script("window.open('https://www.premint.xyz/login/')")

     #检查是否已登录 已登录则退出
     validLogin = self.loginValid(driver)
     if(validLogin == False):
         logger.info("未登录，开始链接钱包")
         self.linkWallet(driver)
     else:
         logger.info("已登录")

     logger.info(id+"钱包绑定premint完成")
     if(quit):
      Common.closeAds(ads_id)
      

  @classmethod
  def linkWallet(self, driver):
   driver.switch_to.window(driver.window_handles[1])
   #点击 链接钱包 元素
   # //*[@id="wallet-connector"]/button[2]
   Common.AutoClick(
       By.XPATH, "//*[@id=\"wallet-connector\"]/button[2]", driver)

   #点击 小狐狸钱包 元素
   # //*[@id="WEB3_CONNECT_MODAL_ID"]/div/div/div[2]/div[1]/div/div[1]/img
   Common.AutoClick(
       By.XPATH, "//*[@id=\"WEB3_CONNECT_MODAL_ID\"]/div/div/div[2]/div[1]/div/div[1]/img", driver)

   # 切换 至metamask  刷新页面
   driver.switch_to.window(driver.window_handles[0])
   driver.refresh()

   validSign = Common.check_element_exists(
       By.XPATH, "//*[@id=\"app-content\"]/div/div[3]/div/div[3]/button[2]", driver)
   if(validSign):
     #钱包已经链接网站就直接签名
     valid = Common.check_element_exists(
         By.XPATH, "//*[@id=\"app-content\"]/div/div[3]/div/a", driver)
     #点击Sign
     # //*[@id="app-content"]/div/div[3]/div/div[3]/button[2]
     Common.AutoClickWithRefresh(
         By.XPATH, "//*[@id=\"app-content\"]/div/div[3]/div/div[3]/button[2]", driver)
     logger.info("点击签名1完成")

     if(valid):
      Common.AutoClick(
          By.XPATH, "//*[@id=\"app-content\"]/div/div[3]/div/div[3]/button[2]", driver)
      logger.info("点击签名2完成")
     sleep(3)
   else:
     #没链接网站尝试链接钱包 并 签名
     #点击next
     # //*[@id="app-content"]/div/div[2]/div/div[3]/div[2]/button[2]
     Common.AutoClick(
         By.XPATH, "//*[@id=\"app-content\"]/div/div[2]/div/div[3]/div[2]/button[2]", driver)
     #点击Connect
     # //*[@id="app-content"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]
     Common.AutoClick(
         By.XPATH, "//*[@id=\"app-content\"]/div/div[2]/div/div[2]/div[2]/div[2]/footer/button[2]", driver)
     #切换回premint
     driver.switch_to.window(driver.window_handles[1])
     #点击 链接钱包 元素
     # //*[@id="wallet-connector"]/button[2]
     Common.AutoClick(
         By.XPATH, "//*[@id=\"wallet-connector\"]/button[2]", driver)

     #点击 小狐狸钱包 元素
     # //*[@id="WEB3_CONNECT_MODAL_ID"]/div/div/div[2]/div[1]/div/div[1]/img
     Common.AutoClick(
         By.XPATH, "//*[@id=\"WEB3_CONNECT_MODAL_ID\"]/div/div/div[2]/div[1]/div/div[1]/img", driver)
     # 切换 至metamask  刷新页面
     driver.switch_to.window(driver.window_handles[0])
     driver.refresh()

     #点击Sign
     try:
      valid = Common.check_element_exists(
          By.XPATH, "//*[@id=\"app-content\"]/div/div[3]/div/a", driver)
      #点击Sign
      # //*[@id="app-content"]/div/div[3]/div/div[3]/button[2]
      Common.AutoClickWithRefresh(
          By.XPATH, "//*[@id=\"app-content\"]/div/div[3]/div/div[3]/button[2]", driver)
      logger.info("点击签名3完成")

      if(valid):
       Common.AutoClick(
           By.XPATH, "//*[@id=\"app-content\"]/div/div[3]/div/div[3]/button[2]", driver)
       logger.info("点击签名4完成")
     except:
       logger.info("签名异常，可能没签名")

   #测试是否已经注册完成
   #切换回premint
   logger.info("测试是否已经注册完成")

   #检查是否已登录 已登录则退出
   valid = self.loginValid(driver)
   if(valid == False):
       logger.info("未登录，开始链接钱包")
       self.linkWallet(driver)
   else:
       logger.info("已登录")

  @classmethod
  def linkTwitterMain(self, ads_id: string, id: string, quit: Boolean):
     resp = requests.get(open_url+ads_id).json()
     if resp["code"] != 0:
         logger.info(resp["msg"])
         logger.info("please check ads_id")
         sys.exit()

     chrome_driver = resp["data"]["webdriver"]
     chrome_options = Options()
     chrome_options.add_experimental_option(
         "debuggerAddress", resp["data"]["ws"]["selenium"])
     driver = webdriver.Chrome(chrome_driver, options=chrome_options)

     #打开并解锁metamask
     self.openMetamask(driver)

     # https://www.premint.xyz/profile/
     #打开premint
     driver.execute_script("window.open('https://www.premint.xyz/profile/')")
     #检查是否已登录 已登录则退出
     validLogin = self.loginValid(driver)
     if(validLogin == False):
         logger.info("未登录，开始链接钱包"+ads_id)
         return
     else:
         logger.info("已登录")
     self.linkTwitter(driver)
     logger.info(id+":premint绑定推特&Discord完成")
     if(quit):
      Common.closeAds(ads_id)

  @classmethod
  def linkTwitter(self, driver):
      driver.switch_to.window(driver.window_handles[1])

      #验证是否已绑定推特
      valT = Common.check_element_exists(
          By.XPATH, "//a[text()='Connect Twitter']", driver)

      if(valT == True):
          logger.info("未绑定推特开始绑定")

          #点击链接推特
          # //a[text()='Connect Twitter']
          Common.AutoClick(By.XPATH, "//a[text()='Connect Twitter']", driver)
          #等待推特 授权跳转
          sleep(5)
          #点击 授权
          # //*[@id="allow"]
          Common.AutoClick(By.XPATH, "//*[@id=\"allow\"]", driver)
          sleep(5)
          # 验证是否成功绑定
          val = Common.check_element_exists(
              By.XPATH, "//a[text()='Connect Twitter']", driver)
          if(val == False):
              logger.info("绑定premint 推特验证成功")

      else:
          logger.info("推特已绑定")
      valD = Common.check_element_exists(
          By.XPATH, "//a[text()='Connect Discord']", driver)
      if(valD):
          #点击链接dc
          # //a[text()='Connect Discord']
          Common.AutoClick(By.XPATH, "//a[text()='Connect Discord']", driver)
          #等待dc 授权跳转
          sleep(5)
          #点击 授权
          # //*[@id="allow"]
          Common.AutoClickWithRefresh(
              By.XPATH, "//*[@id=\"app-mount\"]/div[2]/div/div[1]/div/div/div/div/div/div[2]/button[2]", driver)
          sleep(5)
          # 验证是否成功绑定
          val = Common.check_element_exists(
              By.XPATH, "//a[text()='Connect Discord']", driver)
          if(val == False):
              logger.info("绑定premint Discord验证成功")
      else:
          logger.info("Discord已绑定")

  @classmethod
  def loginValid(self, driver):
      # https://www.premint.xyz/profile/

      driver.switch_to.window(driver.window_handles[1])
      driver.refresh()
      val = Common.check_element_exists(
          By.XPATH, "//*[@id=\"navbarAccount\"]", driver)
      if(val == False):
       logger.info("登录检查不通过")
      return val

  #打开并解锁metamask
  @classmethod
  def openMetamask(self, driver):
      #    logger.info(driver.title)
     #打开metamask 解锁钱包
     logger.debug("开启&解锁钱包")
     driver.get(
         "chrome-extension://ogibelfbcbolpcdjhakooclfjgndogld/home.html#unlock")
     #输入密码
     # //*[@id="password"]
    #  val=Common.check_element_exists(By.XPATH, "//*[@id=\"password\"]", driver)
    #  print(val)
    #  Common.AutoInput(By.XPATH, "//*[@id=\"password\"]", "w7217459", driver)
     #点击Unlock
     # //*[@id="app-content"]/div/div[3]/div/div/button
    #  Common.AutoClick(
    #      By.XPATH, "//*[@id=\"app-content\"]/div/div[3]/div/div/button", driver)
     
  @classmethod
  def premintLottery(self, ads_id: string, id: string, taskList: List, quit: Boolean):
     logger.info("开始抽奖任务") 
     resp = requests.get(open_url+ads_id).json()
     if resp["code"] != 0:
         logger.info(resp["msg"])
         logger.info("please check ads_id")
         sys.exit()

     chrome_driver = resp["data"]["webdriver"]
     chrome_options = Options()
     print( resp["data"]["ws"]["selenium"])
     chrome_options.add_experimental_option(
         "debuggerAddress", resp["data"]["ws"]["selenium"])
     
     driver = webdriver.Chrome(chrome_driver, options=chrome_options)
     driver.set_page_load_timeout(40)
     driver.set_script_timeout(40)
     #打开并解锁metamask
     self.openMetamask(driver)

     #https://www.premint.xyz/profile/
     #打开premint
     
     for i in range(0,len(taskList)):
      try:
          driver.switch_to.window(driver.window_handles[0])
          self.premintLotteryWarpe(ads_id,id,taskList[i].link,taskList[i].register,quit,driver)
      except twitterError as e:
          logger.error("序号："+id+"推特异常，页面无法打开")
          exception_data.append(exceptionData(id=id,ads_id=ads_id,link=taskList[i].link,address='',type=e.msg))
          if(quit):
               Common.closeAds(ads_id)
          return
      except discordError as e:
          logger.error("序号："+id+"discord异常,页面无法打开")
          exception_data.append(exceptionData(id=id,ads_id=ads_id,link=taskList[i].link,address='',type=e.msg))
          while (len(driver.window_handles)>1):
              print("窗口数")
              print(len(driver.window_handles))
              driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
              driver.close()
          driver.switch_to.window(driver.window_handles[0])
          return
      except Exception as e:
        #   requests.get(close_url+ads_id)
          logger.exception(e)
          exception_data.append(exceptionData(id=id,ads_id=ads_id,link=taskList[i].link,address='',type=""))
          while (len(driver.window_handles)>1):
              print("剩余窗口数："+str(driver.window_handles))
              print("关闭：窗口"+str(len(driver.window_handles)-1))
              driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
              driver.close()
          driver.switch_to.window(driver.window_handles[0])
          
     if(quit):
       Common.closeAds(ads_id)
  
  @classmethod
  def premintLotteryWarpe(self, ads_id: string,id: string, link: string, register: Boolean, quit: Boolean,driver):
      try:
        self.premintLotteryMain(ads_id,id,link,register,quit,driver)
        
      except TimeoutException  as t:
        logger.error("序号："+id+"任务页面开启缓慢异常。任务："+link)
        while (len(driver.window_handles)>1):
              print("剩余窗口数："+str(driver.window_handles))
              print("关闭：窗口"+str(len(driver.window_handles)-1))
              driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
              driver.close()
        exception_data.append(exceptionData(id=id,ads_id=ads_id,link=link,address="",type="任务页面开启缓慢异常。任务："+link))
       #关闭其他页面 并重新执行该方法
    #    while (len(driver.window_handles)>1):
    #        print("窗口数")
    #        print(len(driver.window_handles))
    #        driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
    #        driver.close()
    #    driver.switch_to.window(driver.window_handles[0])
    #    self.premintLotteryMain(ads_id,id,link,register,quit,driver)
  
     
  @classmethod
  def premintLotteryMain(self, ads_id: string,id: string, link: string, register: Boolean, quit: Boolean,driver):
     temp = "window.open('"+link+"')"
     logger.debug("序号："+id+",开启任务界面:"+link)
     try:
      driver.execute_script(temp) 
     except:
      driver.execute_script("window.stop()")  
        
     driver.switch_to.window(driver.window_handles[1])
     #查询是否正确打开页面
     Common.checkAndExceptein(By.XPATH,"//img[@alt='PREMINT']",driver)
     
     valReFinished=Common.check_element_exists(By.XPATH,"//a[text()=' Unregister']",driver,2,1)
     
     if(valReFinished):
       logger.debug("序号："+id+"，已完成注册，跳过")
       driver.close()
       return
       
     driver.refresh() 
     logger.debug("序号："+id+"，未完成注册，开始任务")
     #查找 推特关注任务
     logger.debug("序号："+id+":查找 推特关注任务")
     twLinks = []
     twEles = Common.AutoGetElements(
         By.XPATH, "//*[@id='step-twitter']/div/div/div[3]/div[1]/a", driver)
     
     if(twEles is not None):
      for tl in range(0, len(twEles)):
         twLinks.append(twEles[tl].get_attribute("href"))

     #查找 推特Like&Retweet任务
     logger.debug("序号："+id+":查找 推特Like&Retweet任务")
     twRetList = []
     twRets = Common.AutoGetElements(
         By.XPATH, "//*[@id='step-twitter']/div/div/div[3]/div[2]/a", driver)
     if(twRets is not None):
      for tr in range(0, len(twRets)):
         twRetList.append(twRets[tr].get_attribute("href"))

     #查找 discord进入任务
     logger.debug("序号："+id+":查找 discord进入任务")
     disLinkList = []
     disEles = Common.AutoGetElements(
         By.XPATH, "//*[@id='step-discord']/div/div/div[3]/div/a",
         driver)
     if(disEles is not None):
      for tr in range(0, len(disEles)):
         disLinkList.append(disEles[tr].get_attribute("href"))

     #执行 推特关注任务
     logger.info("序号："+id+":开始推特关注任务,关注"+str(len(twLinks))+"个")
     for i in range(0, len(twLinks)):
         driver.switch_to.window(driver.window_handles[0])
         var = "window.open('"+twLinks[i]+"')"
         driver.execute_script(var) 
         
         driver.switch_to.window(
             driver.window_handles[len(driver.window_handles)-1])
         
         #开始关注
         twitterMain.twitterFollowMain(ads_id, False, driver)
       
             
         driver.close()
         driver.switch_to.window(driver.window_handles[0])

     #执行 推特Like&Retweet
     logger.debug("序号："+id+":开始推特Like&Retweet任务,关注"+str(len(twRetList))+"个")
     for i in range(0, len(twRetList)):
         driver.switch_to.window(driver.window_handles[0])
         var = "window.open('"+twRetList[i]+"')"
         driver.execute_script(var) 

        # driver.execute_script("window.stop()")   
         
         driver.switch_to.window(
             driver.window_handles[len(driver.window_handles)-1])
         #开始like&Retweet
         logger.debug("序号："+id+"开始like&Retweet")
         twitterMain.twitterLikeMain(ads_id, False, driver)
         driver.close()
         driver.switch_to.window(driver.window_handles[0])

     logger.debug("序号："+id+"推特任务完成,开始discord")

     logger.info(id+":开始进入discord任务,"+str(len(disLinkList))+"个")
    #  执行 进入discord任务
     for i in range(0, len(disLinkList)):
         driver.switch_to.window(driver.window_handles[0])
         var = "window.open('"+disLinkList[i]+"')"
         logger.info(var)
         
         try:
          driver.execute_script(var) 
         except:
          driver.execute_script("window.stop()")   
         
         driver.switch_to.window(
             driver.window_handles[len(driver.window_handles)-1])
         #开始关注
         discordMain.discordJoinMain(ads_id, False, driver)
         driver.close()
         
     driver.switch_to.window(
             driver.window_handles[len(driver.window_handles)-1])    
     if(register == "是" ):
         logger.info("序号："+id+":开始点击注册")
         valRe=Common.check_element_exists(By.XPATH,"//*[@id='registration_status']/div/a",driver,2,1)
         print("valRe="+str(valRe))
         if(valRe==False):
          driver.refresh()
          logger.info("序号："+id+":开始点击注册2")
          Common.AutoClickWithRefresh(By.XPATH, "//button[@type='submit']", driver)
          sleep(5)
          driver.refresh()
          valFinish=Common.check_element_exists(By.XPATH,"//a[text()=' Unregister']",driver,10,1)
          print("valFinish="+str(valFinish))
          if(valFinish==False):
              logger.error("序号："+id+":注册失败，重试")
              self.premintLotteryMain(ads_id,id,link,register,quit,driver)
            #   valFinish=True

             
     
     logger.info("序号："+id+":已完成注册")
     if(quit):
        while (len(driver.window_handles)>1):
              print("剩余窗口数："+str(driver.window_handles))
              print("关闭：窗口"+str(len(driver.window_handles)-1))
              driver.switch_to.window(driver.window_handles[len(driver.window_handles)-1])
              driver.close()
      
  @classmethod
  def premintRegisterCheck(self,ads_id: string,id: string, links: List,address:string):
     logger.info("序号：{}，开始检查状态".format(id))
     temp="verify/?wallet={}"
     #检查是否注册完成  已注册未开奖
    # You aren't registered.
    # You are registered.
    # You were selected!
    # You were not selected!
     result=[]
     for i in range(0 ,len(links)):
      header = {
         "cookie": "",
         "Accept": "*/*",
         "Accept-Encoding": "gzip, deflate, br",
         "Accept-Language": "zh-CN,zh;q=0.9",
         "Connection": "keep-alive",
         "Content-Type": "application/json",
         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
               }
      resp = requests.get(url=links[i].link+temp.format(address),headers=header)
      resultType="未知"
      if("You aren't registered." in resp.text):
        resultType="未注册"
        print("未注册")
      if("You are registered." in resp.text):
        resultType="已注册"
        print("已注册")
      if("You were selected!" in resp.text):
        resultType="已中奖"
        print("已中奖")  
      if("You were not selected!" in resp.text):
        resultType="未中奖"
        print("未中奖")
      result.append(premintRegisterCheck(id=id,ads_id=ads_id,link=links[i].link,address=address,type=resultType))
      sleep(1)
     return result 
       
       
     
     
     
     
    #  valReFinished=Common.check_element_exists(By.XPATH,"//a[text()=' Unregister']",driver)
     
    #  if(valReFinished):
    #    logger.debug("序号：{}，{}已注册，".format(id,link))
    #    driver.close()
    #    return premintRegisterCheck(id,ads_id,link,"已注册未开奖")
    #  else:
    #    logger.debug("序号：{}，{}未注册完成，请检查".format(id,link))
   
   
# premintMain.premintRegisterCheck("j3byl5s","158","https://www.premint.xyz/hhwl/","0x8d98cf8962ec37d77ab91aea9d353bd96870cd0a",False)

