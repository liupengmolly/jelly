# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log

class JwcPersonalPipeline(object):
    def __init__(self):
        self.connect=pymysql.connect(
            host = 'www.jellyofusst.cn',
            db = 'jelly',
            user = 'root',
            password = 'jelly14not@fish',
            charset = 'utf8',
            use_unicode = False)
        self.cursor=self.connect.cursor()

    """实现了去重判断"""
    def process_item(self,item,spider):
        self.cursor.execute('select * from personal_info where st=%s',item['st'])
        ret=self.cursor.fetchone()
        if ret:
            self.cursor.execute('update personal_info set info=%s where st=%s',
                                (item['info'],item['st']))
            self.cursor.execute('update personal_info set crawltime=CURRENT_TIMESTAMP where st=%s',
                                (item['st']))
        else:
            self.cursor.execute('insert into personal_info(st,info) value (%s,%s)',
                                (item['st'],item['info']))
        self.connect.commit()
        return item

