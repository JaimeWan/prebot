
import string

#表格对象
class widget:
    
  def __init__(self,address:string,id:string,ads_id:string,word:string):

        self.address=address   

        self.id=id

        self.ads_id=ads_id
        
        self.word=word
        
class twitterTask:
  def __init__(self,link:string,type:string,content:string):

        self.link=link   

        self.type=type

        self.content=content
        
class premintTask:
  def __init__(self,link:string,register:string):

        self.link=link
        self.register=register


class premintRegisterCheck:
  def __init__(self,id:string,ads_id:string,link:string,address:string,type:string):
        
        self.id=id

        self.ads_id=ads_id    
        
        self.link=link   
        
        self.address=address
        
        self.type=type
        
class exceptionData:
  def __init__(self,id:string,ads_id:string,link:string,address:string,type:string):
        
        self.id=id

        self.ads_id=ads_id    
        
        self.link=link   
        
        self.address=address
        
        self.type=type        