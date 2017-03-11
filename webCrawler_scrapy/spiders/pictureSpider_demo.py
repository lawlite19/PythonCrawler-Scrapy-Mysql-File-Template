#coding=utf-8
import scrapy
import re
import os
import urllib
import MySQLdb
import sys
from scrapy.selector import Selector
from scrapy.http import HtmlResponse,Request

from webCrawler_scrapy.items import WebcrawlerScrapyItem #导入item对应的类，crawlPictures是项目名，items是items.py文件，import的是items.py中的class，也可以import *

class Spdier_pictures(scrapy.spiders.Spider):
    name="webCrawler_scrapy"    #定义爬虫名，要和settings中的BOT_NAME属性对应的值一致
    
    allowed_domains=["desk.zol.com.cn"] #搜索的域名范围，也就是爬虫的约束区域，规定爬虫只爬取这个域名下的网页
    
    start_urls=["http://desk.zol.com.cn/fengjing/1920x1080/1.html"]   #开始爬取的地址
    
    #该函数名不能改变，因为Scrapy源码中默认callback函数的函数名就是parse
    def parse(self, response):
        se=Selector(response) #创建查询对象，HtmlXPathSelector已过时
        if(re.match("http://desk.zol.com.cn/fengjing/\d+x\d+/\d+.html", response.url)):#如果url能够匹配到需要爬取的url，就爬取
            src=se.xpath("//ul[@class='pic-list2  clearfix']/li")#匹配到ul下的所有小li
            
            for i in range(len(src)):#遍历li个数
                imgURLs=se.xpath("//ul[@class='pic-list2  clearfix']/li[%d]/a/img/@src"%i).extract() #依次抽取所需要的信息
                titles=se.xpath("//ul[@class='pic-list2  clearfix']/li[%d]/a/img/@title"%i).extract()
                
                if imgURLs:
                    realUrl=imgURLs[0].replace("t_s208x130c5","t_s2560x1600c5") #这里替换一下，可以找到更大的图片
                    file_name=u"%s.jpg"%titles[0] #要保存文件的命名
                    
                    path=os.path.join("D:\pics",file_name)#拼接这个图片的路径，我是放在F盘的pics文件夹下
                    
                    type = sys.getfilesystemencoding()
                    print file_name.encode(type)  
                    
                    item=WebcrawlerScrapyItem()  #实例item（具体定义的item类）,将要保存的值放到事先声明的item属性中
                    item['name']=file_name 
                    item['url']=realUrl
                    print item["name"],item["url"]    
                    
                    yield item  #返回item,这时会自定解析item
                    
                    urllib.urlretrieve(realUrl,path)  #接收文件路径和需要保存的路径，会自动去文件路径下载并保存到我们指定的本地路径
            
            all_urls=se.xpath("//a/@href").extract()#提取界面所有的url
            for url in all_urls:
                if url.startswith("/fengjing/1920x1080/"):#若是满足定义的条件，继续爬取
                    yield Request("http://desk.zol.com.cn"+url,callback=self.parse)