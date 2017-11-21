import json
from PIL import Image,ImageEnhance
import scrapy
from pytesseract import *
import time
import re
from jwc_personal.items import JwcPersonalItem
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class Jwc_Personal_Spider(scrapy.Spider):
    name="jwc_personal"
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    st_num='1311410328'
    passwd='zmclppy14.'

    """二值化函数"""
    def initTable(self,threshold=30):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        return table

    """去除图片噪声"""
    def depoint(self,img,threshold=100):  # input: gray image
        pixdata = img.load()
        w, h = img.size
        for y in range(1, h - 1):
            for x in range(1, w - 1):
                count = 0
                if pixdata[x, y - 1] > threshold:
                    count = count + 1
                if pixdata[x, y + 1] > threshold:
                    count = count + 1
                if pixdata[x - 1, y] > threshold:
                    count = count + 1
                if pixdata[x + 1, y] > threshold:
                    count = count + 1
                if count > 2:
                    pixdata[x, y] = 255
        return img

    """验证码处理函数"""
    def cap_process(self):
        self.driver.get_screenshot_as_file('capt.jpg')
        image = Image.open('capt.jpg')
        box = (683, 277, 735, 298)
        region = image.crop(box)
        region.save('cap.jpg')
        # 提高图片质量
        image = Image.open("cap.jpg")
        # 转换为灰度图
        image = image.convert('L')
        # 增强对比度
        sharpImage = ImageEnhance.Contrast(image)
        sharpImage = sharpImage.enhance(2.0)
        # 去除噪声
        cleanImage = self.depoint(sharpImage)
        # 设定阈值，二值化
        binaryImage = cleanImage.point(self.initTable(), '1')
        binaryImage.save("cap_process.jpg")
        try:
            yzm=image_to_string(binaryImage, config='-psm 7')
        except UnicodeDecodeError as e:
            yzm='73498'
        return yzm

    """登录成功后定位至绩点表"""
    def locat_to_gpa(self,userinfo):
        print("正在爬取" + userinfo[0] + "的绩点表")
        time.sleep(1)
        info_query = self.driver.find_element_by_link_text('信息查询')
        info_query.click()
        table_gpa = self.driver.find_element_by_link_text('绩点表(二专课程不计入任选课程)')
        table_gpa.click()
        time.sleep(2)
        self.driver.switch_to_frame('iframeautoheight')

    """定位至绩点表后获取绩点表的信息"""
    def get_info(self):
        info=dict()
        info["平均学分绩点"] = re.search(r'\d{1}\.\d{2}',self.driver.find_element_by_id('Td2').text).group()
        courses = self.driver.find_elements_by_xpath('//table[@id="DBGrid"]/tbody/tr')
        for course in courses:
            course_info=re.findall(r'<td>(.*?)<\/td>',course.get_attribute('innerHTML'))
            if re.match(r'\d{8}',course_info[0]):
                info[course_info[1]]=course_info[3:6]
            else:
                if re.match(r'要求学分',course_info[1]):
                    group_scores=re.findall(r'(\w{2,3}学分)：(\d{1,2}(\.\d{1,2})?)',course_info[1])
                    for group_score in group_scores:
                        info[course_info[0]+group_score[0]]=group_score[1]
                elif re.search(r'要求学分',course_info[1]):
                    group_title,group_scores=re.match(r'(.*?)：(.*)',course_info[1]).groups()
                    group_scores=re.findall(r'(\w{2,3}学分)：(\d{1,2}(\.\d{1,2})?)',group_scores)
                    for group_score in group_scores:
                        info[group_title+group_score[0]]=group_score[1]
        return info

    def start_requests(self):
        url="http://jwc1.usst.edu.cn"
        yield scrapy.Request(url,callback=self.parse)

    def parse(self,response):
        self.driver.get(response.url)
        item=JwcPersonalItem()
        flag=True
        while flag:
            flag=False
            time.sleep(2)
            login = self.driver.find_element_by_id('Button1')
            user=self.driver.find_element_by_name('TextBox1')
            user.clear()
            user.send_keys(self.st_num)
            pwd=self.driver.find_element_by_name('TextBox2')
            pwd.clear()
            pwd.send_keys(self.passwd)
            cap=self.driver.find_element_by_name('TextBox3')
            yzm=self.cap_process()
            cap.send_keys(yzm)
            login.click()
            time.sleep(1)
            self.driver.switch_to_alert().accept()
            try:
                userinfo=self.driver.find_element_by_id('xhxm').text
            except NoSuchElementException as e:
                flag=True
        self.locat_to_gpa(userinfo)
        info=self.get_info()
        item['info']=json.dumps(info)
        item['st']=self.st_num
        yield item
        # post_headers={
        # "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, "
        #           "image / webp, image/apng,* / *;q = 0.8",
        # "Accept-Encoding": "gzip, deflate",
        # "Accept-Language": "zh-CN,zh;q=0.8",
        # "Cache-Control": "max-age=0",
        # "Connection": "keep-alive",
        # "Host":"my.usst.edu.cn",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        # "Referer":"http://my.usst.edu.cn/"
        # }
        # form={'user':'1311410328','pwd':'zmclppy14.'}
        # captcha=response.xpath('//img[re:test(@src,"CheckCode\.aspx$")]/@src').extract()[0]
        # viewstate=response.xpath('//input[@name="__VIEWSTATE"]/@value').extract()[0]
        # if "http" in captcha:
        #     captchaUrl=captcha
        # else:
        #     captchaUrl="http://jwc1.usst.edu.cn/"+captcha
        # urlretrieve(captchaUrl,"cap.jpg")
        # image=Image.open("cap.jpg")
        # image=image.convert('L')
        # binaryImage=image.point(self.initTable(),'1')
        # text=image_to_string(binaryImage,config='-psm 7')
        # print(text)
        # print(viewstate)
        # yield scrapy.FormRequest('http://jwc1.usst.edu.cn/Default2.aspx',
        #     formdata={'__VIEWSTATE':viewstate,'TextBox1':'1311410328',
        #               'TextBox2':'zmclppy14.','TextBox3':text},
        #     callback=self.parse_home)

        # cap = self.driver.find_element_by_xpath('//li[@id="captchaContent"]/img').text
        # print("cap"+str(cap))
        # if len(cap) > 0:
        #     capUrl="http://my.usst.edu.cn/"+cap[0]
        #     print("capUrl"+capUrl)
        #     urlretrieve(capUrl, "cap.jpg")
        #     image=Image.open("cap.jpg")
        #     image=image.convert('L')
        #     binaryImage=image.point(self.initTable(),'1')
        #     text=image_to_string(binaryImage,config='-psm 7')
        #     print("验证码为："+text)
        #     form['captcha']=text
        # print(response.xpath('//div[@class="form-area"]').extract())
        # print("form为:"+str(form))
        # return scrapy.FormRequest.from_response(response,headers=post_headers,
        #     formdata=form,callback=self.parse_home)
