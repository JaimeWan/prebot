

from operator import truediv
from time import sleep
from typing import List
from xmlrpc.client import Boolean
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Ui_mainUi import Ui_MainWindow
from PyQt5 import QtWidgets
import xlrd
from taskUtils.metamask_main import metamaskMain    
from taskUtils.twitter_main import twitterMain
from taskUtils.premint_main import premintMain
from widgetModel import *
import threading
from loguru import logger
import json
import xlwt 
import datetime
import time

from globalvar import *

threadNum = 2


# logger.add(".log/subUi.log", format="{time} | {level} | {name} | {message}", level="DEBUG",
#            rotation="1 KB", retention="10 seconds", encoding="utf-8", backtrace=True, diagnose=True)




 
class subUi(Ui_MainWindow, QMainWindow):

    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi(self)
            
        
    #获取表格数据
    def getWidgetData(self):
       row_num = self.tableWidget.rowCount()
       cols_num = self.tableWidget.columnCount()
       table_d = []
       for i in range(0, row_num):
          address = self.tableWidget.item(i, 0).text()
          id = self.tableWidget.item(i, 1).text()
          ads_id = self.tableWidget.item(i, 2).text()
          word = self.tableWidget.item(i, 3).text()
          data = widget(address, id, ads_id, word)
          table_d.append(data)
       return table_d
   
    def showFileDialog(self):
        # 文件打开窗口，路径"D:\\"是窗口打开默认显示的路径，最后一个参数文件的过滤，不满足条件的不会显示
        filename, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "", "Image Files (*.xls *.xlsx)")
        if filename:
            logger.info(f"file: {filename}")
            excel = xlrd.open_workbook(filename)
            sheet = excel.sheet_by_index(0)
            #导入数据
            for i in range(1, sheet.nrows):
             row_list = sheet.row_values(i)
             
             if(row_list[0].startswith("0x") | row_list[0].startswith("0X")):
              self.tableWidget.setRowCount(self.tableWidget.rowCount()+1)
              address_item = QtWidgets.QTableWidgetItem(row_list[0])
              self.tableWidget.setItem(i-1, 0, address_item)
              id_item = QtWidgets.QTableWidgetItem(row_list[1])
              self.tableWidget.setItem(i-1, 1, id_item)
              acc_id_item = QtWidgets.QTableWidgetItem(row_list[2])
              self.tableWidget.setItem(i-1, 2, acc_id_item)
              word_item = QtWidgets.QTableWidgetItem(row_list[3])
              self.tableWidget.setItem(i-1, 3, word_item)
             else:
              msg_box = QMessageBox(QMessageBox.Warning,
                                    "错误提示", str("第"+str(i)+"行地址错误"))
              msg_box.exec_()
              break
          
    def clearWidget(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.clearContents()

    #导入钱包助记词
    def importAddress(self):
       table_d = self.getWidgetData()

       logger.info(len(table_d))
       for i in range(0, len(table_d)):
           logger.info(i)
           logger.info(table_d[i].ads_id)
           logger.info(table_d[i].word)
           metamaskMain.accountImport(table_d[i].ads_id, table_d[i].word)
    
    #premint钱包绑定
    def premintImport(self):
        
       table_d = self.getWidgetData()
       
       logger.info(len(table_d))
       for i in range(0, len(table_d)):
           logger.info("id:"+table_d[i].id+"开始绑定")
           try:
            premintMain.linkWalletMain(table_d[i].ads_id, table_d[i].id, True)
           except Exception as e:
              logger.info("id:"+table_d[i].id+"绑定异常")
              logger.info(e)

    #premint绑定dc和推特
    def premintDcAndTwitter(self):
        
       table_d = self.getWidgetData()
       
       logger.info(len(table_d))
       for i in range(0, len(table_d)):
           logger.info("id:"+table_d[i].id+"开始绑定")
           try:
            premintMain.linkTwitterMain(table_d[i].ads_id, table_d[i].id, True)
           except Exception as e:
              logger.info("id:"+table_d[i].id+"绑定异常")
              logger.info(e)

    #导入推特任务数据
    def twitterTaskImport(self):
         # 文件打开窗口，路径"D:\\"是窗口打开默认显示的路径，最后一个参数文件的过滤，不满足条件的不会显示
        filename, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "", "Image Files (*.xls *.xlsx)")
        if filename:
            logger.info(f"file: {filename}")
            excel = xlrd.open_workbook(filename)
            sheet = excel.sheet_by_index(0)
            
            twitter_task_data = []
            #导入数据
            for i in range(1, sheet.nrows):
             row_list = sheet.row_values(i)
             
             if(row_list[0].startswith("https") | row_list[0].startswith("http")):
              
              link = row_list[0]
              
              type = row_list[1]
              
              content = row_list[2]
              
              twitter_task_data.append(twitterTask(link, type, content))
              logger.info(row_list[0])
              logger.info(row_list[1])
             else:
              msg_box = QMessageBox(QMessageBox.Warning,
                                    "错误提示", str("第"+str(i)+"行链接错误"))
              msg_box.exec_()
              break
     
    #推特日常检查
    def twitterDailyCheck(self):
        logger.info("推特日常检查开始")
        table_d = self.getWidgetData()
       
        for t in range(0, len(table_d)):
         twitterMain.dailyLogin(table_d[t].ads_id, True)
    
    #推特任务执行
    def twitterTask(self):
        
       logger.info(len(twitter_task_data))
       
       table_d = self.getWidgetData()
       
       for t in range(0, len(table_d)):
           
         for i in range(0, len(twitter_task_data)):
             try:
              logger.info(table_d[t].ads_id+":开始任务")
              logger.info(type(twitter_task_data[i].type))
              twitterMain.twitterTaskMain(table_d[t].ads_id, twitter_task_data[i].link,
                                          twitter_task_data[i].type, twitter_task_data[i].content, True)
             except Exception as e:
                logger.info("id:"+table_d[i].id+"任务异常")
                logger.info(e)
    
    #premint任务数据导入
    def premintTaskImport(self):
        # 文件打开窗口，路径"D:\\"是窗口打开默认显示的路径，最后一个参数文件的过滤，不满足条件的不会显示
        filename, _ = QFileDialog.getOpenFileName(
            self, "打开文件", "", "Image Files (*.xls *.xlsx)")
        if filename:
            logger.info(f"file: {filename}")
            excel = xlrd.open_workbook(filename)
            sheet = excel.sheet_by_index(0)
            premint_task_data.clear()
            #导入数据
            for i in range(1, sheet.nrows):
             row_list = sheet.row_values(i)
             
             if(row_list[0].startswith("https") | row_list[0].startswith("http")):
              
              link = row_list[0]
              register = row_list[1]
              logger.info(link)
              premint_task_data.append(premintTask(link, register))
              
             else:
              msg_box = QMessageBox(QMessageBox.Warning,
                                    "错误提示", str("第"+str(i)+"行链接错误"))
              msg_box.exec_()
              break
             logger.info(len(premint_task_data))

    def premintLottery(self, ads_id: string, id: string,  taskList: List,quit:Boolean):
        logger.debug("序号："+id+",开始任务")
        
        premintMain.premintLottery(ads_id, id, taskList, quit)
        # try:
        #       premintMain.premintLottery(ads_id, id, taskList, quit)
        # except Exception as e:
        #        logger.error("序号："+id+",任务异常")
        #        logger.exception(e)
        #        exception_data.append({"id": id, "ads_id":ads_id})
               
          
    #premint任务执行
    def premintTask(self):
       logger.debug("premint任务执行开始")
       exception_data.clear()
       table_d = self.getWidgetData()
       
       x = len(table_d)//threadNum
       y = len(table_d) %threadNum

       for t in range(0, x):

         threads = []
         for j in range(0, threadNum):
           thread = threading.Thread(target=self.premintLottery, args=(table_d[t*threadNum+j].ads_id, table_d[t*threadNum+j].id,premint_task_data,True))

           threads.append(thread)

         for m in range(0, threadNum):
            threads[m].start()
            sleep(1.5)

         for n in range(0, threadNum):
            threads[n].join()

       for t in range(0, y):
         try:
          logger.debug("序号："+table_d[x*threadNum+t].id+":开始任务")

          premintMain.premintLottery(table_d[x*threadNum+t].ads_id, table_d[x*threadNum+t].id, premint_task_data,True)
         except Exception as e:
            logger.error("序号："+table_d[x*threadNum+t].id+":任务异常")
            logger.error(e)
            logger.exception(e)
       logger.info("任务完成")
       xl = xlwt.Workbook(encoding='utf-8')
       ws = xl.add_sheet("任务异常记录", cell_overwrite_ok=True)
       
       ws.write(0,0,"id")
       ws.write(0,1,"ads_id") 
       ws.write(0,2,"地址") 
       ws.write(0,3,"链接")
       ws.write(0,4,"错误类型")
       for i in range(0,len(exception_data)):
        
          ws.write(i+1,0,exception_data[i].id)
          ws.write(i+1,1,exception_data[i].ads_id) 
          ws.write(i+1,2,exception_data[i].address) 
          ws.write(i+1,3,exception_data[i].link)
          ws.write(i+1,4,exception_data[i].type)
          
       
       timestamp=datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H%M%S')
       xl.save('任务异常记录{}.xls'.format(timestamp))
    
       
    #任务情况检查
    def premintCheck(self):
       table_d = self.getWidgetData()
       result=[]
       for i in range(0,len(table_d)):
        temp=premintMain.premintRegisterCheck(ads_id=table_d[i].ads_id,id=table_d[i].id,links=premint_task_data,address=table_d[i].address)
        result.extend(temp)                    
       
       xl = xlwt.Workbook(encoding='utf-8')
       ws = xl.add_sheet("测试", cell_overwrite_ok=True)
       
       ws.write(0,0,"id")
       ws.write(0,1,"ads_id") 
       ws.write(0,2,"地址") 
       ws.write(0,3,"链接")
       ws.write(0,4,"状态")
       for i in range(0,len(result)):
          ws.write(i+1,0,result[i].id)
          ws.write(i+1,1,result[i].ads_id) 
          ws.write(i+1,2,result[i].address) 
          ws.write(i+1,3,result[i].link)
          ws.write(i+1,4,result[i].type)
       
       timestamp=datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d %H%M%S')
       xl.save('测试{}.xls'.format(timestamp))
       logger.info("任务检查完成")
# premintMain.premintRegisterCheck("j3byl5s","158","https://www.premint.xyz/hhwl/","0x8d98cf8962ec37d77ab91aea9d353bd96870cd0a")                 