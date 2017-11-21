# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



import pymysql

class JwcPipeline(object):
    def __init__(self):
        self.connect=pymysql.connect(
            host = 'www.jellyofusst.cn',
            db = 'jelly',
            user = 'root',
            password = 'jelly14not@fish',
            charset = 'utf8',
            use_unicode = False)
        self.cursor=self.connect.cursor()


    def process_item(self,item,spider):
        self.cursor.execute("insert into jwcinfo (title,body,url,pubtime,site,download) values (%s,%s,%s,%s,%s,%s)",
                            (item["title"],item["body"], item["url"],item["pubtime"],item['site'],item['download']))
        self.connect.commit()
        return item



