# -*- coding: utf-8 -*-
import scrapy
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from jwc.items import JwcItem
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


class QuotesSpider(scrapy.Spider):
	name = "jwc"
	driver=webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
	curtime=time.strftime("%Y-%m-%d",time.localtime(time.time()))
	timeOut=True #判断当前url是否已经爬取过，因为是按照时间顺序每天一次爬取，所以只要通知的发布日期小于当前日期，说明当前模块剩余的都已经被爬取了，直接跳到下一个模块进行爬取

	"""
	True表示对应的模块从头爬取，False表示日常更新（有ifTimeOut判断)
	依次为：
	parse,parse_jwc_info,parse_nd_news,parse_nd_articles
	"""
	parse_degree=[False,False,True,True]

	def start_requests(self):
		# yield scrapy.Request('http://ndxy.usst.edu.cn/index.php?m=News&a=lists&id=2',callback=self.parse_nd_news)
		yield scrapy.Request('http://www.usst.edu.cn/s/1/t/471/p/14/list.htm',meta={"module":14},callback=self.parse)

	"""判断当前通知的发布时间是否满足函数设置的条件（虽不同的情况可以在此函数中统一设置条件
	若条件满足，将timeOut置为True，解析函数可以继续当前模块的解析（是否继续由timeOut决定
	PS：1,由于很多网页有重要通知置顶的功能，所以通知不是严格按照时间排列，于是设置timeOut条件
		 时要注意对当前页所有通知进行检查
		2,如果想重新爬取某个模块，只需把该函数最初设置timOut为False的语句设置为True即可
		3,对于下载资料等一些没有时间的信息没有timeOut设置"""
	def ifTimeOut(self,pubtime):
		if pubtime==self.curtime:
			self.timeOut=True

	'''抓取学校主页的学术报告、学校公告、教研通知的通知和下载内容'''
	def parse(self,response):
		self.timeOut=True
		module=response.meta['module']
		self.driver.get(response.url)
		next_page=self.driver.find_element_by_name('_l_p_n')
		time.sleep(0.1)
		over_count=0
		while self.timeOut:
			#爬取通知
			self.timeOut=self.parse_degree[0]
			infos=self.driver.find_elements_by_xpath("//table[@class='columnStyle']/tbody/tr/td/a")
			for info in infos:
				try:
					url=info.get_attribute("href")
				except StaleElementReferenceException as e:
					continue
				if url[-3:] in ['pdf','lsx','xls','ocx','doc']:
					item = JwcItem()
					if "http://www.usst.edu.cn" in url:
						next_url=url
					elif "http:" not in url:
						next_url="http://www.usst.edu.cn"+url
					else:
						continue
					item['url'] = next_url
					item['site'] = "学校官网"
					item['title'] = info.find_element_by_xpath('..//a/font').text
					item['body'] = item['title']
					item['download'] = 1
					item['pubtime'] = info.find_element_by_xpath('../..//td[@class="postTime"]').text
					self.ifTimeOut(item['pubtime'])
					yield item
				else:
					if "http://www.usst.edu.cn" in url:
						next_url=url
					elif "http:" not in url:
						next_url="http://www.usst.edu.cn"+url
					else:
						continue
					yield scrapy.Request(next_url, callback=self.parse_usst_item)
			#翻页操作
			try:
				url_pre=next_page
				next_page.click()
				time.sleep(0.13)
				next_page=self.driver.find_element_by_name('_l_p_n')
			except NoSuchElementException as e:
				next_page=WebDriverWait(self.driver,5).until(EC.presence_of_element_located((By.NAME,"_l_p_n")))
			except StaleElementReferenceException as e:
				time.sleep(1)
				next_page = self.driver.find_element_by_name('_l_p_n')
			url_aft=next_page
			if url_aft==url_pre:
				over_count=over_count+1
			if over_count==20:
				break
		if module==14:
			yield scrapy.Request('http://www.usst.edu.cn/s/1/t/517/p/5/list.htm',meta={'module':5}, callback=self.parse)
		elif module==5:
			yield scrapy.Request('http://www.usst.edu.cn/s/1/t/517/p/6/list.htm',meta={'module':6}, callback=self.parse)
		else:
			yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/11/list.htm', callback=self.parse_jwc_info)
	# def parse_1(self,response):
	# 	self.driver.get(response.url)
	# 	next_page = self.driver.find_element_by_name('_l_p_n')
	# 	time.sleep(0.1)
	# 	over_count=0
	# 	while True:
	# 		# 爬取通知
	# 		infos = self.driver.find_elements_by_xpath("//table[@class='columnStyle']/tbody/tr/td/a")
	# 		for info in infos:
	# 			try:
	# 				url = info.get_attribute("href")
	# 			except StaleElementReferenceException as e:
	# 				continue
	# 			if url[-3:] in ['pdf', 'lsx', 'xls', 'ocx', 'doc']:
	# 				item = JwcItem()
	# 				if "http:" in url:
	# 					next_url=url
	# 				else:
	# 					next_url="http://www.usst.edu.cn"+url
	# 				item['url'] = next_url
	# 				item['site'] = "学校官网"
	# 				item['title'] = info.find_element_by_xpath('..//a/font').text
	# 				item['body'] = item['title']
	# 				item['download'] = 1
	# 				item['pubtime'] = info.find_element_by_xpath('../..//td[@class="postTime"]').text
	# 				yield item
	# 			else:
	# 				if "http:" in url:
	# 					next_url=url
	# 				else:
	# 					next_url="http://www.usst.edu.cn"+url
	# 				yield scrapy.Request(next_url, callback=self.parse_usst_item)
	# 		# 翻页操作
	# 		try:
	# 			url_pre = next_page
	# 			next_page.click()
	# 			time.sleep(0.13)
	# 			next_page = self.driver.find_element_by_name('_l_p_n')
	# 		except NoSuchElementException as e:
	# 			next_page = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "_l_p_n")))
	# 		except StaleElementReferenceException as e:
	# 			time.sleep(1)
	# 			next_page = self.driver.find_element_by_name('_l_p_n')
	# 		url_aft = next_page
	# 		if url_aft == url_pre:
	# 			over_count = over_count + 1
	# 		if over_count == 20:
	# 			break
    #
	# 	yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/11/list.htm', callback=self.parse_jwc_info)
    #
	# def parse_2(self,response):
	# 	self.driver.get(response.url)
	# 	next_page = self.driver.find_element_by_name('_l_p_n')
	# 	time.sleep(0.1)
	# 	over_count=0
	# 	while self.timeOut:
	# 		# 爬取通知
	# 		infos = self.driver.find_elements_by_xpath("//table[@class='columnStyle']/tbody/tr/td/a")
	# 		for info in infos:
	# 			try:
	# 				url = info.get_attribute("href")
	# 			except StaleElementReferenceException as e:
	# 				continue
	# 			if url[-3:] in ['pdf', 'lsx', 'xls', 'ocx', 'doc']:
	# 				item = JwcItem()
	# 				if "http:" in url:
	# 					next_url=url
	# 				else:
	# 					next_url="http://www.usst.edu.cn"+url
	# 				item['url'] = next_url
	# 				item['site'] = "学校官网"
	# 				item['title'] = info.find_element_by_xpath('..//a/font').text
	# 				item['body'] = item['title']
	# 				item['download'] = 1
	# 				item['pubtime'] = info.find_element_by_xpath('../..//td[@class="postTime"]').text
	# 				yield item
	# 			else:
	# 				if "http:" in url:
	# 					next_url=url
	# 				else:
	# 					next_url="http://www.usst.edu.cn"+url
	# 				yield scrapy.Request(next_url, callback=self.parse_usst_item)
	# 		# 翻页操作
	# 		try:
	# 			url_pre = next_page
	# 			next_page.click()
	# 			time.sleep(0.13)
	# 			next_page = self.driver.find_element_by_name('_l_p_n')
	# 		except NoSuchElementException as e:
	# 			next_page = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, "_l_p_n")))
	# 		except StaleElementReferenceException as e:
	# 			time.sleep(1)
	# 			next_page = self.driver.find_element_by_name('_l_p_n')
	# 		url_aft = next_page
	# 		if url_aft == url_pre:
	# 			over_count = over_count + 1
	# 		if over_count == 20:
	# 			break
	# 	yield scrapy.Request('http://www.usst.edu.cn/s/1/t/517/p/5/list.htm', callback=self.parse_1)

	'''对校园主页上各分栏中所有通知具体信息的爬取'''
	def parse_usst_item(self, response):
		item = JwcItem()
		item['site'] = '学校官网'
		item['url'] = response.url
		item['title'] = ''
		item['download'] = 0
		titles = response.xpath('//td[@class="mc_title"]/span/text()').extract()
		for t in titles:
			item['title'] = item['title']+t
		item['body']="".join(response.xpath('//td[@class="mc_content"]//text()').extract())
		item['pubtime'] = ''
		pubtime = response.xpath('//td[@class="mc_time"]//td/text()').re(r'\d{4}-\d{2}-\d{2}')
		if (len(pubtime) != 0):
			item['pubtime'] = pubtime[0]
			self.ifTimeOut(item['pubtime'])
		down_links = response.xpath('//a[re:test(@href,"(xlsx|xls|pdf|docx|doc)$")]').extract()
		if len(down_links) > 0:
			item['download'] = 1
		yield item

	"""对教务处通知公告的爬取"""
	def parse_jwc_info(self,response):
		self.TimeOut=self.parse_degree[1]
		infos = response.xpath('//a[re:test(@href,"^(http:\/\/(jwc|jwc2010)\.usst\.edu\.cn)?\/s\/\d{1,2}\/t\/\d{3}\/\w{2}\/\w{2}\/info\d{5}\.htm")]')
		for info in infos:
			urls = info.xpath('..//a/@href').extract()
			if len(urls) != 0:
				url = urls[0]
				if url[0:4] == 'http':
					next_url = url
				else:
					next_url = "http://jwc2010.usst.edu.cn" + url
				yield scrapy.Request(next_url, callback=self.parse_jwc_item)
		next_page=response.xpath(u'//a[@title="进入下一页"]/@href').extract()  #包含中文的xpath一定要加u
		if len(next_page)>=1 and self.timeOut==True:
			next_page[0] = "http://jwc2010.usst.edu.cn" + next_page[0]
			yield scrapy.Request(next_page[0], callback=self.parse_jwc_info)
		else:
			# 当爬取到最后一页通知时转到对下载资料的爬取
			yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/1/c/1920/d/2372/list.htm',callback=self.parse_jwc_down)
			yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/1/c/1920/d/2112/list.htm',callback=self.parse_jwc_down)
			yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/1/c/1920/d/2114/list.htm',callback=self.parse_jwc_down)
			yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/1/c/1920/d/2095/list.htm',callback=self.parse_jwc_down)
			yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/1/c/1920/d/2106/list.htm',callback=self.parse_jwc_down)
			yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/1/c/1920/d/2110/list.htm',callback=self.parse_jwc_down)
			#下面是对教学日历的爬取
			yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/1/c/2084/list.htm',callback=self.parse_jwc_date)

	'''对下载中心学生相关资料的爬取'''
	def parse_jwc_down(self,response):
		infos = response.xpath('//a[re:test(@href,"(doc|docx|xls|xlsx|pdf|\/s\/9\/t\/451\/\w{2}\/\w{2}\/info\d{4,5}\.htm)$")]')
		for info in infos:
			url= info.xpath('..//a/@href').extract()[0]
			if url[-3:] in ['pdf','lsx','xls','ocx','doc']:
				item = JwcItem()
				if url[0:4]=='http':
					next_url=url
				else:
					next_url="http://jwc2010.usst.edu.cn"+url
				item['url'] = next_url
				item['site'] = "教务处"
				item['title'] = info.xpath('..//a/font/text()').extract()[0]
				item['body'] = item['title']
				item['download'] = 1
				item['pubtime'] = '2111-11-11'
				yield item
			else:
				if url[0:4] == 'http':
					next_url = url
				else:
					next_url = "http://jwc2010.usst.edu.cn" + url
				yield scrapy.Request(next_url, callback=self.parse_jwc_down_item)
		next_page = response.xpath(u'//a[@title="进入下一页"]/@href').extract()  # 包含中文的xpath一定要加u
		if next_page == []: #此处必须要返回
			return
		else:
			next_page[0] = "http://jwc2010.usst.edu.cn" + next_page[0]
			yield scrapy.Request(next_page[0], callback=self.parse_jwc_down)

	"""对教务处教学日历的爬取
		由于教学日历展示的都是图片，这里只存储链接"""
	def parse_jwc_date(self,response):
		item=JwcItem()
		dates=response.xpath('//a[re:test(@href,"\/s\/9\/t\/\d{2,4}\/\w{2}\/\w{2}\/info\d{4,5}\.htm")]')
		for date in dates:
			url=date.xpath('..//a/@href').extract()[0]
			date_url="http://jwc2010.usst.edu.cn"+url
			item['url'] = date_url
			item['site'] = "教务处"
			item['title'] = date.xpath('..//a/font/text()').extract()[0]
			item['body'] = item['title']
			item['download'] = 0
			item['pubtime'] = '2111-11-11'
			yield item
		yield scrapy.Request('http://jwc2010.usst.edu.cn/s/9/t/451/p/10/c/1925/list.htm',callback=self.parse_jwc_schedule)

	"""对教务处的培养计划进行爬取,并抛出对能动学院网站的爬取请求"""
	def parse_jwc_schedule(self,response):
		item=JwcItem()
		schedules=response.xpath('//a[re:test(@href,"^\/picture\/article.*\.(pdf|docx)$")]')[1:]#因为网页第一个被爬取得元素被隐藏
		for schedule in schedules:
			url=schedule.xpath('..//a/@href').extract()[0]
			url="http://jwc2010.usst.edu.cn"+url
			item['url']=url
			item['site']='教务处'
			item['title']=schedule.xpath('..//a/span/text()').extract()[0]
			item['body']=item['title']
			item['download']=1
			item['pubtime']='2111-11-11'
			yield item
		# yield scrapy.Request('http://ndxy.usst.edu.cn/index.php?m=News&a=lists&id=1&p=2',meta={'module':1},callback=self.parse_nd_news)
		yield scrapy.Request('http://ndxy.usst.edu.cn/index.php?m=Article&a=lists&id=13&cid=21&p=2',
							 meta={'module': 13}, callback=self.parse_nd_articles)

	'''对教务处中所有通知具体信息的爬去'''
	def parse_jwc_item(self,response):
		item=JwcItem()
		item['site']='教务处'
		item['url']=response.url
		item['title']=''
		item['body']=''
		titles=response.xpath('//td[@class="title_shadow"]/div/font/text()').extract()
		for t in titles:
			item['title']=item['title']+t
		item['body'] = "".join(response.xpath('//td[@class="content"]//text()').extract())
		pubtime = response.xpath('//span[@class="style6"]/text()').re(r'\d{4}-\d{2}-\d{2}')
		if len(pubtime) != 0:
			item['pubtime'] = pubtime[0]
			self.ifTimeOut(item['pubtime'])
		down_links = response.xpath('//a[re:test(@href,"(xlsx|xls|pdf|docx|doc)$")]').extract()
		if len(down_links) > 0:
			item['download'] = 1
		else:
			item['download']=0
		yield item

	"""对教务处中下载项的爬取"""
	def parse_jwc_down_item(self,response):
		item = JwcItem()
		item['site'] = '教务处'
		item['url'] = response.url
		item['title'] = ''
		item['body'] = ''
		titles = response.xpath('//td[@class="title_shadow"]/div/font/text()').extract()
		for t in titles:
			item['title'] = item['title'] + t
		item['body'] = "".join(response.xpath('//td[@class="content"]//text()').extract())
		pubtime = response.xpath('//span[@class="style6"]/text()').re(r'\d{4}-\d{2}-\d{2}')
		if len(pubtime) != 0:
			item['pubtime'] = pubtime[0]
		down_links = response.xpath('//a[re:test(@href,"(xlsx|xls|pdf|docx|doc)$")]').extract()
		if len(down_links) > 0:
			item['download'] = 1
		else:
			item['download'] = 0
		yield item

	"""对能动学院学院动态（id:1)、最新公告(id:2)中属于能动学院的信息爬取"""
	def parse_nd_news(self,response):
		module=response.meta['module']
		if module==1:
			infos = response.xpath(
				'//a[re:test(@href,"^\/index\.php\?m=News&a=details&id=1&NewsId=\d{1,4}")]')
		else:
			infos = response.xpath(
				'//a[re:test(@href,"^\/index\.php\?m=News&a=details&id=2&NewsId=\d{1,4}")]')
		self.timeOut = self.parse_degree[2]
		for info in infos:
			url = info.xpath('..//a/@href').extract()[0]
			pubtime=info.xpath('..//span/text()').extract()[0]
			if url[0:4] == 'http':
				next_url = url
			else:
				next_url = "http://ndxy.usst.edu.cn" + url
			time.sleep(1)
			yield scrapy.Request(next_url, meta={'pubtime':pubtime},callback=self.parse_nd_item)
		time.sleep(3)
		next_page = response.xpath(u'//a[contains(.,"下一页")]/@href').extract()
		if len(next_page) >= 1 and self.timeOut==True:
			next_page[0] = "http://ndxy.usst.edu.cn" + next_page[0]
			yield scrapy.Request(next_page[0],meta={'module':module}, callback=self.parse_nd_news)
		elif module==1:
			yield scrapy.Request('http://ndxy.usst.edu.cn/index.php?m=News&a=lists&id=2&p=4',
								 meta={'module':2},callback=self.parse_nd_news)
		elif module==2:
			yield scrapy.Request('http://ndxy.usst.edu.cn/index.php?m=Article&a=lists&id=13&cid=21&p=2',
								 meta={'module':13},callback=self.parse_nd_articles)

	"""对能动学院科研与学科建设（id:13)、
				本科生培养（id:11)
				学生工作（id:15)中属于能动学院的信息爬取"""
	def parse_nd_articles(self,response):
		module=response.meta['module']
		if module==13:
			infos=response.xpath(
				'//a[re:test(@href,"^\/index\.php\?m=Article&a=details&id=13&cid=21&nid=\d{1,4}")]')
		elif module==11:
			infos = response.xpath(
				'//a[re:test(@href,"^\/index\.php\?m=Article&a=details&id=11&cid=28&nid=\d{1,4}")]')
		elif module==15:
			infos = response.xpath(
				'//a[re:test(@href,"^\/index\.php\?m=Article&a=details&id=15&cid=46&nid=\d{1,4}")]')
		self.timeOut = self.parse_degree[3]
		for info in infos:
			url = info.xpath('..//a/@href').extract()[0]
			pubtime = info.xpath('..//span/text()').extract()[0]
			if url[0:4] == 'http':
				next_url = url
			else:
				next_url = "http://ndxy.usst.edu.cn" + url
			time.sleep(1)
			yield scrapy.Request(next_url, meta={'pubtime': pubtime}, callback=self.parse_nd_item)
		time.sleep(3)
		next_page = response.xpath(u'//a[contains(.,"下一页")]/@href').extract()
		if len(next_page) >= 1 and self.timeOut == True:
			next_page[0] = "http://ndxy.usst.edu.cn" + next_page[0]
			yield scrapy.Request(next_page[0],meta={'module':module},callback=self.parse_nd_articles)
		elif module == 13:
			yield scrapy.Request('http://ndxy.usst.edu.cn/index.php?m=Article&a=lists&id=11&cid=28&p=2',
								 meta={'module':11}, callback=self.parse_nd_articles)
		elif module == 11:
			yield scrapy.Request('http://ndxy.usst.edu.cn/index.php?m=Article&a=lists&id=15&cid=46&p=2',
								 meta={'module':15}, callback=self.parse_nd_articles)
		else:
			exit(0)

	"""对能动学院每个具体通知页的爬取"""
	def parse_nd_item(self,response):
		time.sleep(3)
		item=JwcItem()
		item['pubtime']=response.meta['pubtime']
		self.ifTimeOut(item['pubtime'])
		item['url']=response.url
		item['site']='能动学院'
		try:
			item['title']=response.xpath('//div[@class="xiangqingTit"]/text()').extract()[0]
		except IndexError as e:
			time.sleep(2)
			item['title'] = response.xpath('//div[@class="xiangqingTit"]/text()').extract()[0]
		item['body'] = "".join(response.xpath('//div[@class="xiangqingCon"]//text()').extract())
		down_links = response.xpath('//a[re:test(@href,"(xlsx|xls|pdf|docx|doc)$")]').extract()
		if len(down_links) > 0:
			item['download'] = 1
		else:
			item['download'] = 0
		yield item
