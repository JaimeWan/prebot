from typing import List
import xlrd
import string
import xlwt 


class excelUtil:
    
    #导出excel
    def exoprtExcel(self,path:string,data:List):
        wb = xlwt.Workbook()
        ws = wb.add_sheet(path)
        # for i in range(0,len(data)):
        #     for key,val in data[i].item():
        #         ws.write