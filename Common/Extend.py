
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from unittest.case import TestCase
import time
from Common import LogUtility

class Extend(object):
    # 安装webdriver
    def __init__(self, browser='chrome'):
        '''
        初始化selenium webdriver, 将chrome作为默认webdriver
        '''
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        if browser == "firefox" or browser == "ff":
            driver = webdriver.Firefox(options=options)
        elif browser == "chrome":
            driver = webdriver.Chrome(options=options)
        elif browser == "internet explorer" or browser == "ie":
            driver = webdriver.Ie(options=options)
        elif browser == "opera":
            driver = webdriver.Opera(options=options)
        elif browser == "phantomjs":
            driver = webdriver.PhantomJS(options=options)
        try:
            self.driver = driver
        except Exception:
            raise NameError("Not found %s browser,You can enter 'ie', 'ff' or 'chrome'." % browser)
            #LogUtility.log("Not found %s browser,You can enter 'ie', 'ff' or 'chrome'." % browser)
            
            
    def findElement(self,type,value):
        '''
        描述：查找元素, 例如：('id','username')

        用法：self.findElement(type,value)
        '''
        try:
            if type == "id" or type == "ID" or type=="Id":
                element = self.driver.find_element_by_id(value)
                #LogUtility.log("Find element id:%s" % value)

            elif type == "name" or type == "NAME" or type=="Name":
                element = self.driver.find_element_by_name(value)
                #LogUtility.log("Find element name:%s" % value)

            elif type == "class" or type == "CLASS" or type=="Class":
                element = self.driver.find_element_by_class_name(value)
                #LogUtility.log("Find element class:%s" % value)

            elif type == "link_text" or type == "LINK_TEXT" or type=="Link_text":
                element = self.driver.find_element_by_link_text(value)
                #LogUtility.log("Find element link text:%s" % value)
                
            elif type == "tag_name" or type == "TAG_NAME" or type=="Tag_name":
                element = self.driver.find_element_by_tag_name(value)
                #LogUtility.log("Find element tag_name:%s" % value)

            elif type == "xpath" or type == "XPATH" or type=="Xpath":
                element = self.driver.find_element_by_xpath(value)
                #LogUtility.log("Find element xpath:%s" % value)

            elif type == "css" or type == "CSS" or type=="Css":
                element = self.driver.find_element_by_css_selector(value)
                #LogUtility.log("Find element css:%s" % value)
            else:
                raise NameError("tpye:%s不正确，请输入正确的type"%(str(type)))
                #LogUtility.log("Please correct the type in function parameter")
        except NameError:
            raise
        except Exception:
            raise ValueError("element对象没有找到，%s:%s" % (str(type),str(value)))
            #LogUtility.log("No such element found %s:%s" % (str(type),str(value)))
        return element

    def findElements(self,type,value):
        '''
        描述：查找元素, 例如：('id','username')

        用法：self.findElements(type,value)
        '''
        try:
            if type == "id" or type == "ID" or type=="Id":
                elements = self.driver.find_elements_by_id(value)
                #LogUtility.log("Find elements id:%s" % value)

            elif type == "name" or type == "NAME" or type=="Name":
                elements = self.driver.find_elements_by_name(value)
                #LogUtility.log("Find element name:%s" % value)

            elif type == "class" or type == "CLASS" or type=="Class":
                elements = self.driver.find_elements_by_class_name(value)
                #LogUtility.log("Find element class:%s" % value)

            elif type == "link_text" or type == "LINK_TEXT" or type=="Link_text":
                elements = self.driver.find_elements_by_link_text(value)
                #LogUtility.log("Find element link text:%s" % value)
                
            elif type == "tag_name" or type == "TAG_NAME" or type=="Tag_name":
                elements = self.driver.find_elements_by_tag_name(value)
                #LogUtility.log("Find element tag_name:%s" % value)

            elif type == "xpath" or type == "XPATH" or type=="Xpath":
                elements = self.driver.find_elements_by_xpath(value)
                #LogUtility.log("Find element xpath:%s" % value)

            elif type == "css" or type == "CSS" or type=="Css":
                elements = self.driver.find_elements_by_css_selector(value)
                #LogUtility.log("Find element css:%s" % value)
            else:
                raise NameError("tpye:%s不正确，请输入正确的type"%(str(type)))
                #LogUtility.log("Please correct the type in function parameter")
            if len(elements) == 0:
                raise ValueError('elements没有取到元素对象，%s:%s' % (str(type),str(value)))
        except NameError:
            raise
        except ValueError:
            raise 
        except Exception as e:
            print(e)
            #LogUtility.log("No such element found %s:%s" % (str(type),str(value)))
        return elements

    def implicitlyWwait(self, time):
        '''
        描述：隐式等待
        用法：self.implicitlyWwait(time)
        '''
        self.driver.implicitly_wait(time)

    def wait(self,clock):
        '''
        描述：等待
        用法：self.wait(clock)
        '''
        time.sleep(clock)

    def findSelect(self,type,value,text):
        '''
        描述：操作select元素

        用法：self.findSelect(type,value,text)
        '''
        element = Select(self.findElement(type,value)).select_by_visible_text(text)
        return element

    def assertSelectedOptions(self,type,value,texts):
        '''
        描述：校验下拉框已选择文本

        用法：assertSelectedOptions(self,type,value,texts)
        '''
        element = Select(self.findElement(type,value))
        optionsset=set()
        textslist = texts.split(',')
        for i in element.all_selected_options:
            optionsset.add(i.text.strip())
        LogUtility.logger.debug('texts:%s\n页面文本集：%s'%(set(textslist),optionsset))
        TestCase().assertSetEqual(optionsset, set(textslist))

    def assertSelectOptions(self,type,value,texts):
        '''
        描述：校验下拉框文本

        用法：assertSelectOptions(self,type,value,texts)
        '''
        element = Select(self.findElement(type,value))
        optionsset=set()
        textslist = texts.split(',')
        for i in element.options:
            optionsset.add(i.text.strip())
        LogUtility.logger.debug('texts:%s\n页面文本集：%s'%(set(textslist),optionsset))
        TestCase().assertSetEqual(optionsset, set(textslist))

    def open(self,url):
        '''
        描述：打开url

        用法：self.open(url)
        '''
        if url != "":
            self.driver.get(url)
        else:
            raise ValueError("please provide a base url")


    def type(self,type,value,text):
        '''
        描述：操作input元素

        用法：self.type(type,value,text)
        '''
        element =self.findElement(type,value)
        element.send_keys(text)
    
    def clearType(self,type,value,text):
        '''
        描述：清空并填写文本
        
        用法：self.clearType(type,value,text)
        '''
        element = self.findElement(type, value)
        element.clear()
        time.sleep(1)
        element.send_keys(text)   

    def clearTypetime(self,value,clock):
       
        js = "document.getElementById('"+value+"').removeAttribute('readonly')"
        LogUtility.logger.debug('js语句：%s'%(js))
        time.sleep(1.5)
        self.driver.execute_script(js)
        element = self.driver.find_element_by_id(value)
        element.clear()
        element.send_keys(clock)    

    def enter(self,type,value):
        '''
        描述：回车

        用法：self.enter(type,value)
        '''
        element =self.findElement(type,value)
        element.send_keys(Keys.ENTER)
		
    def backSpace(self,type,value):
        '''
        描述：删除键

        用法：self.backSpace(type,value)
        '''
        element =self.findElement(type,value)
        element.clear()
        element.send_keys(Keys.BACK_SPACE)
        
    def table(self,type,value):
        '''
        描述：Table

        用法：self.table(type,value)
        '''
        element =self.findElement(type,value)
        element.send_keys(Keys.TAB)

    def submit(self,type,value):
        '''
        描述：提交表单
        用法：self.submit(element)
        '''
        element = self.findElement(type, value)
        element.submit()

    def click(self,type,value):
        '''
        描述：点击页面元素，如：button, image, link等
        用法：self.click(element)
        '''
        element = self.findElement(type,value)
        element.click()

    def clear(self,type, value):
        '''
        描述：清理元素值
        用法：self.clear(element)
        '''
        element = self.findElement(type, value)
        element.clear()

    def quit(self):
        '''
        描述：退出webdriver
        用法：self.quit()
        '''
        self.driver.quit()

    def getAttribute(self, element, attribute):
        '''
        描述：获取元素属性
        用法：self.getAttribute(element, attribute)
        '''
        return element.get_attribute(attribute)

    def getText(self, type, value):
        '''
        描述：获取元素的值
        用法：self.getText(element)
        '''
        element = self.findElement(type, value)
        return element.text

    def getSize(self, element):
        '''
        描述：获取元素的大小
        用法：self.getSize(element)
        '''
        return element.size

    def isDisplayed(self, element):
        '''
        描述：元素上否隐藏
        用法：self.isDisplayed(element)
        '''
        element.is_displayed()

    def getTitle(self):
        '''
        描述：获取Title
        用法：self.getTitle()
        '''
        return self.driver.title
    
    def getCurrentUrl(self):
        '''
        描述：获取当前链接
        用法：self.getCurrentUrl()
        '''
        return self.driver.current_url

    def getScreenshot(self,targetpath):
        '''
        描述：截图并保存到指定路径
        用法：self.getScreenshot(targetpath)
        '''
        self.driver.get_screenshot_as_file(targetpath)

    def maximizeWindow(self):
        '''
        描述：最大化当前浏览器窗口
        用法：self.maximizeWindow()
        '''
        self.driver.maximize_window()

    def back(self):
        '''
        描述：后退
        用法：self.back()
        '''
        self.driver.back()

    def forward(self):
        """
        描述：前进
        用法：self.forward()
        """
        self.driver.forward()

    def getWindowSize(self):
        """
        描述：获取窗口大小
        用法：self.getWindowSize()
        """
        return self.driver.get_window_size()

    def refresh(self):
        '''
        描述：刷新
        用法：self.refresh()
        '''
        self.driver.refresh()

    def switchToFrame(self, type, value):
        '''
        描述：切换到frame
        用法：self.switchToFrame()
        '''
        element = self.findElement(type, value)
        self.driver.switch_to.frame(element)

    def switchToParentFrame(self):
        '''描述：返回上层frame
        用法：self.switchToParentFrame()
        '''
        self.driver.switch_to.parent_frame()

    def switchToOuterFrame(self):
        '''描述：返回最外层frame
        用法：self.switchToOuterFrame()
        '''
        self.driver.switch_to.default_content()

    def switchToWindow(self,windowindex):
        '''
        描述：切换到窗口
        用法：self.switchToWindow(windowindex)
        '''
        currenthandle = self.driver.current_window_handle
        handleslist = self.driver.window_handles
        self.driver.switch_to_window(handleslist[int(windowindex)-1])

    def currentWindowHandle(self):
        '''
        描述：当前窗口句柄
        用法：self.currentWindowHandle()
        '''
        self.driver.current_window_handle

    def WindowHandle(self):
        '''
        描述：所有窗口句柄
        用法：self.WindowHandle()
        '''
        self.driver.window_handle
 
    def assertTitle(self,text):
        """
        描述：验证当前页中title是否在给定得字符串中
        用法：self.assert_title()
        """

        title = str(self.driver.title)
        LogUtility.logger.debug('text:%s\ntitle:%s'%(text,title))
        TestCase().assertEqual(text, title)
		
    def assertTextExist(self,type,value,exist = 'True'):
        element = self.findElement(type, value)
        if exist == 'True':
            if element.text == "":
                LogUtility.logger.debug('元素对象的文本为空')
            else:
                raise NameError('元素对象的文本:%s,不为空'%(element.text))
        elif exist == 'False':
            if element.text != "":
                LogUtility.logger.debug('元素对象的文本:%s,不为空'%(element.text))
            else:
                raise NameError('元素对象的文本为空')
        else:
            raise TypeError('输入的参数exist:%s格式不正确'%(exist))
   
    def assertText(self,type,value,text):
        '''
        描述：验证当前页中既定得元素是否在给定得字符串中
        用法：self.assert_text()
        '''
        element = self.findElement(type, value)
        LogUtility.logger.debug('text:%s\n页面文本:%s'%(text,element.text.strip()))
        TestCase().assertEqual(text, element.text.strip())
        
    def assertTexts(self,type,value,texts,order='False'): 
        '''
        描述：验证当前页中既定得元素是否在给定得字符串中
        用法：self.assertTexts(type,value,texts,order='False')
        '''
        if order == 'True':
            s = []
            textslist = texts.split(',')
            elements = self.findElements(type, value)
            for element in elements:
                s.append(element.text.strip())
            LogUtility.logger.debug('texts:%s\n页面文本集：%s'%(textslist,s))
            TestCase().assertListEqual(textslist, s)
        elif order == 'False':
            s= set()
            textslist = texts.split(',')
            elements = self.findElements(type, value)
            for element in elements:
                s.add(element.text.strip())
            LogUtility.logger.debug('texts:%s\n页面文本集：%s'%(set(textslist),s))
            TestCase().assertSetEqual(set(textslist), s)

    def assertAttribute(self,type,value,attribute,texts):
        s =set()
        textslist = texts.split(',')
        elements = self.findElements(type, value)
        for element in elements:
            if not element.get_attribute(attribute):
                raise AttributeError('element对象没有'+attribute+'属性')
            s =set.union(s,set(element.get_attribute(attribute).strip().split(',')))
        
        LogUtility.logger.debug('texts:%s\n页面文本集：%s'%(set(textslist),s))
        TestCase().assertSetEqual(set(textslist), s)
        
    def switchToAlert(self):
        '''
        切换到弹窗
        '''
        WebDriverWait(self.driver,30).until(EC.alert_is_present())
        time.sleep(1)
        self.driver.switch_to.alert
        
    def acceptAlert(self):
        '''
        弹窗确认
        '''
        WebDriverWait(self.driver,30).until(EC.alert_is_present())
        time.sleep(1)
        self.driver.switch_to.alert.accept()
        
    def dismissAlert(self):
        '''
        弹窗取消
        '''
        WebDriverWait(self.driver,30).until(EC.alert_is_present())
        time.sleep(1)
        self.driver.switch_to.alert.dismiss()
        
    def textAlert(self):
        '''
        弹窗信息
        '''
        self.driver.switch_to.alert.text
        
    def assertTextAlert(self,text):
        '''
        验证弹窗信息
        '''
        WebDriverWait(self.driver,30).until(EC.alert_is_present())
        time.sleep(1)
        realtext = self.driver.switch_to.alert.text
        LogUtility.logger.debug('text:%s\n页面文本集：%s'%(text,realtext))
        TestCase().assertIn(text,realtext)
        
    def tpyeAlert(self,text):
        '''
        弹窗填写
        '''
        WebDriverWait(self.driver,30).until(EC.alert_is_present())
        time.sleep(1)
        self.driver.switch_to.alert.send_keys(text)
        
    def setWindowSize(self,width,height,windowHandle='current'):
        '''
        描述：设置浏览器窗口大小
        用法：setWindowSize(width,height,windowHandle='current'):
        参数：
        width:浏览器宽
        height:浏览器搞高
        '''
        
        return self.driver.set_window_size(width, height, windowHandle)
        
    def scrollBar(self, leftmargin,topmargin):
        '''
        描述：设置滚动条
        用法：self.driver.execute_script(js)
        参数：
        lefttmargin:左边距
        topmargin:上边距
        '''
        js="window.scrollTo(" + leftmargin + ',' + topmargin +");"
        print(js)
        self.driver.execute_script(js)
        
    def focus(self,type,value):
        target = self.findElement(type, value)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        
    def uploadFile(self,type,value,path):
        '''
        描述：上传文件
        '''
        self.findElement(type,value).send_keys(path)
        
    def checkOne(self,type,value):
        element = self.findElement(type, value)
        if not element.is_selected():
            element.click()
            
    def decheckOne(self,type,value):
        element = self.findElement(type, value)
        if element.is_selected():
            element.click()

    def checkAll(self,type,value):
        elements = self.findElements(type, value)
        for element in elements:
            if not element.is_selected():
                element.click()
    
    def decheckAll(self,type,value):
        elements = self.findElements(type, value)
        for element in elements:
            if element.is_selected():
                element.click()  

    def assertChecked(self,type,value,result = 'True'):
        '''
        描述：验证元素勾选
        用法：self.assertchecked(type,value)
        参数：result默认为True,验证元素被勾选，
        result=False,验证元素为被勾选
        '''
        element = self.findElement(type, value)
        print(str(element.is_selected()))
        TestCase().assertEqual(str(element.is_selected()), result)

    def tableClick(self,type,value,column,columntext,attributevalue):
        table = self.findElement(type, value )
        trlist = table.find_elements_by_tag_name('tr')
        textlist = []
        titlelist = []        
        for row in trlist:
            tdlist = row.find_elements_by_tag_name('td')
            
            if tdlist[int(column)-1].text.strip() == columntext:  
                textlist.append(tdlist[int(column)-1].text)            
                print('tdlistcell:',tdlist[int(column)-1].text)
                element = tdlist[-1]   
                elements = element.find_elements_by_xpath('./a')
                for i in elements:
                    if i.get_attribute('title') == attributevalue:
                        titlelist.append(i.get_attribute('title'))
                        i.click()
                        break
                break            
        if textlist == []:   
            raise NameError('没有匹配到文本：%s'%(columntext))
        elif titlelist == []:
            raise NameError('没有找到"%s"'%(attributevalue)) 

    def tableCheck(self,type,value,matchparas,descolumn,result = 'True'):
        table = self.findElement(type, value)
        trlist = table.find_elements_by_tag_name('tr')
        matchparaslist = matchparas.split(',')
        columns = []
        columntexts = []
        matchlist = []
        
        for i in range(len(matchparaslist)):
            if i%2 == 0: 
                columns.append(matchparaslist[i])
            else:
                columntexts.append(matchparaslist[i])
                
        for row in trlist:
            tdlist = row.find_elements_by_tag_name('td')
            if len(columns) == 1:
                if tdlist[int(columns[0])-1].text.strip() == columntexts[0]:
                    matchlist.append(tdlist[int(columns[0])-1].text.strip())
                    LogUtility.logger.debug('texts:%s\n页面文本：%s'%(columntexts[0],tdlist[int(columns[0])-1].text.strip()))
                    checkelement = tdlist[int(descolumn)-1].find_element_by_xpath('./input')
                    if result == 'True':
                        if checkelement.is_selected():                                         
                            break
                        if not checkelement.is_selected():
                            checkelement.click()                                              
                            break
                    elif result == 'False':
                        if checkelement.is_selected():
                            checkelement.click()                                              
                            break
                        if not checkelement.is_selected():                                            
                            break
                    else:
                        raise TypeError('descolumn=1时，result只能输入True或False')
            else:               
                if tdlist[int(columns[0])-1].text.strip() == columntexts[0] and tdlist[int(columns[1])-1].text.strip() == columntexts[1]:
                    matchlist.append(tdlist[int(columns[1])-1].text.strip())
                    LogUtility.logger.debug('texts:%s,%s\n页面文本：%s,%s'%(columntexts[0],columntexts[1],tdlist[int(columns[0])-1].text.strip(),tdlist[int(columns[1])-1].text.strip()))
                    checkelement = tdlist[int(descolumn)-1].find_element_by_xpath('./input')
                    if result == 'True':
                        if checkelement.is_selected():                                         
                            break
                        if not checkelement.is_selected():
                            checkelement.click()                                              
                            break
                    elif result == 'False':
                        if checkelement.is_selected():
                            checkelement.click()                                              
                            break
                        if not checkelement.is_selected():                                            
                            break
                    else:
                        raise TypeError('descolumn=1时，result只能输入True或False')

    def tableOperate(self,type,value,matchparas,descolumn,text=None):
        table = self.findElement(type, value)
        trlist = table.find_elements_by_tag_name('tr')
        matchparaslist = matchparas.split(',')
        columns = []
        columntexts = []
        matchlist = []
        textlist = []
        titlelist = []
        
        for i in range(len(matchparaslist)):
            if i%2 == 0: 
                columns.append(matchparaslist[i])
            else:
                columntexts.append(matchparaslist[i])
        
        for row in trlist:
            tdlist = row.find_elements_by_tag_name('td')
            if len(columns) == 1:
                if tdlist[int(columns[0])-1].text.strip() == columntexts[0]:
                    matchlist.append(tdlist[int(columns[0])-1].text.strip())
                    LogUtility.logger.debug('texts:%s\n页面文本：%s'%(columntexts[0],tdlist[int(columns[0])-1].text.strip()))
                    if int(descolumn) == 1:
                        checkelement = tdlist[int(descolumn)-1].find_element_by_xpath('./input')
                        checkelement.click()                                              
                        break

                    
                    elif int(descolumn) == len(tdlist):
                        element = tdlist[-1]
                        elements = element.find_elements_by_xpath('./a')
                        for i in elements: 
                            if i.get_attribute('title').strip() == str(text):
                                titlelist.append(i.get_attribute('title'))
                                LogUtility.logger.debug('texts:%s\n页面文本：%s'%(i.get_attribute('title'),str(text)))
                                i.click()
                                break
                            if i.text.strip() == str(text):
                                textlist.append(i.text.strip())
                                LogUtility.logger.debug('texts:%s\n页面文本：%s'%(i.text.strip(),str(text)))   
                                i.click()
                                break
                    else:
                        element = tdlist[int(descolumn)-1]
                        elements = element.find_elements_by_xpath('./a')
                        for i in elements:
                            if i.text.strip() == str(text):
                                textlist.append(i.text.strip())
                                LogUtility.logger.debug('texts:%s\n页面文本：%s'%(i.text.strip(),str(text)))
                                print(i.text.strip())
                                i.click()
                                break
                    break
            else:               
                if tdlist[int(columns[0])-1].text.strip() == columntexts[0] and tdlist[int(columns[1])-1].text.strip() == columntexts[1]:
                    matchlist.append(tdlist[int(columns[1])-1].text.strip())
                    LogUtility.logger.debug('texts:%s,%s\n页面文本：%s,%s'%(columntexts[0],columntexts[1],tdlist[int(columns[0])-1].text.strip(),tdlist[int(columns[1])-1].text.strip()))
                    if int(descolumn) == 1:
                        checkelement = tdlist[int(descolumn)-1].find_element_by_xpath('./input')
                        checkelement.click()                                              
                        break
                    
                    elif int(descolumn) == len(tdlist):
                        element = tdlist[-1]
                        elements = element.find_elements_by_xpath('./a')
                        for i in elements: 
                            if i.get_attribute('title').strip() == str(text):
                                titlelist.append(i.get_attribute('title'))
                                LogUtility.logger.debug('texts:%s\n页面文本：%s'%(i.get_attribute('title'),str(text)))   
                                i.click()
                                break
                            if i.text.strip() == str(text): 
                                textlist.append(i.text.strip())
                                LogUtility.logger.debug('texts:%s\n页面文本：%s'%(i.text.strip(),str(text)))   
                                i.click()
                                break
                    else:
                        element = tdlist[int(descolumn)-1]
                        print('element',element)
                        elements = element.find_elements_by_xpath('./a')
                        for i in elements:
                            if i.text.strip() == str(text):
                                textlist.append(i.text.strip())
                                LogUtility.logger.debug('texts:%s\n页面文本：%s'%(i.text.strip(),str(text)))
                                i.click()
                                break
                    break
        if int(descolumn) == 1: 
            if not checkelement:
                raise NameError('没有找到勾选项')
        elif int(descolumn) != len(tdlist):
            if matchlist == []:   
                raise NameError('没有匹配到文本：%s'%(matchparas))
            if textlist == []:   
                raise NameError('没有找到文本%s'%(text))
        else:    
            if textlist == [] and titlelist == []:
                raise NameError('操作列没有找到文本或属性%s'%(text))
	
    def assertTableOp(self,type,value,column,columntext,texts):
        table = self.findElement(type, value )
        trlist = table.find_elements_by_tag_name('tr')
        if len(trlist)==0:
            raise NameError('表格行数为0，%s:%s,没有定位到正确的表格'%(type,value))
        s = set()
        textslist = texts.split(',')
        matchlist = []
        for row in trlist:
            tdlist = row.find_elements_by_tag_name('td')
            if tdlist[int(column)-1].text.strip() == columntext:
                matchlist.append(tdlist[int(column)-1])
                element = tdlist[-1]
                elements = element.find_elements_by_xpath('./a')
                for i in elements:
                    s.add(i.get_attribute('title'))
        LogUtility.logger.debug('texts:%s\n页面文本集：%s'%(set(textslist),s))
        if matchlist == []:
            raise NameError('没有找到匹配项,输入文本%s'%(tdlist[int(column)-1].text,columntext))
        TestCase().assertSetEqual(s, set(textslist))
        
    def assertTableAttribute(self,type,value,matchparas,descolumn,values):
        table = self.findElement(type, value)
        trlist = table.find_elements_by_tag_name('tr')
        if len(trlist)==0:
            raise NameError('表格行数为0，%s:%s,没有定位到正确的表格'%(type,value))
        matchparaslist = matchparas.split(',')
        columns = []
        columntexts = []
        matchlist = []
        j=50    
        #控制row循环次数
        for i in range(len(matchparaslist)):
            if i%2 == 0: 
                columns.append(matchparaslist[i])
            else:
                columntexts.append(matchparaslist[i])
                
        for row in trlist:
            tdlist = row.find_elements_by_tag_name('td')
            j -=1
            if j > 0:
                if len(columns) == 1:
                    LogUtility.logger.debug('页面文本:%s'%(tdlist[int(columns[0])-1].text.strip()))
                    if tdlist[int(columns[0])-1].text.strip() == columntexts[0]:
                        matchlist.append(tdlist[int(columns[0])-1].text.strip())
                        LogUtility.logger.debug('texts:%s\n页面文本:%s'%(columntexts[0],tdlist[int(columns[0])-1].text.strip()))
                        element = tdlist[int(descolumn)-1]
                        break
                else:
                    LogUtility.logger.debug('页面文本：%s,%s'%(tdlist[int(columns[0])-1].text.strip(),tdlist[int(columns[1])-1].text.strip()))
                    if tdlist[int(columns[0])-1].text.strip() == columntexts[0] and tdlist[int(columns[1])-1].text.strip() == columntexts[1]:
                        matchlist.append(tdlist[int(columns[1])-1].text.strip())
                        LogUtility.logger.debug('texts:%s,%s\n页面文本：%s,%s'%(columntexts[0],columntexts[1],tdlist[int(columns[0])-1].text.strip(),tdlist[int(columns[1])-1].text.strip()))
                        element = tdlist[int(descolumn)-1]
                        break
        if matchlist == []:
            if len(columns) == 1:
                raise NameError('没有找到匹配项，输入文本%s'%(columntexts[0]))
            else:
                raise NameError('没有找到匹配项，输入文本%s,%s'%(columntexts[0],columntexts[1]))
                
        LogUtility.logger.debug('texts:%s\n页面文本集：%s'%(values,element.get_attribute('title').strip()))
        TestCase().assertEqual(values, element.get_attribute('title').strip())
        
    def assertTableText(self,type,value,matchparas,descolumn,text):
        table = self.findElement(type, value)
        trlist = table.find_elements_by_tag_name('tr')
        if len(trlist)==0:
            raise NameError('表格行数为0，%s:%s,没有定位到正确的表格'%(type,value))
        matchparaslist = matchparas.split(',')
        columns = []
        columntexts = []
        matchlist = []
        j=len(trlist)
        #控制row循环次数
        for i in range(len(matchparaslist)):
            if i%2 == 0: 
                columns.append(matchparaslist[i])
            else:
                columntexts.append(matchparaslist[i])
        for row in trlist:
            tdlist = row.find_elements_by_tag_name('td')
            j -=1
            if j >= 0:
                print(len(columns))
                if len(columns) == 1:
                    print(tdlist[int(columns[0])-1].text.strip())
                    if tdlist[int(columns[0])-1].text.strip() == columntexts[0]:
                        matchlist.append(tdlist[int(columns[0])-1].text.strip())
                        LogUtility.logger.debug('texts:%s\n页面文本:%s'%(columntexts[0],tdlist[int(columns[0])-1].text.strip()))
                        element = tdlist[int(descolumn)-1]
                        break                      
                else:               
                    if tdlist[int(columns[0])-1].text.strip() == columntexts[0] and tdlist[int(columns[1])-1].text.strip() == columntexts[1]:
                        matchlist.append(tdlist[int(columns[1])-1].text.strip())
                        LogUtility.logger.debug('texts:%s,%s\n页面文本：%s,%s'%(columntexts[0],columntexts[1],tdlist[int(columns[0])-1].text.strip(),tdlist[int(columns[1])-1].text.strip()))
                        element = tdlist[int(descolumn)-1]
                        break      
        if matchlist == []:
            if len(columns) == 1:
                raise NameError('没有找到匹配项，输入文本%s'%(columntexts[0]))
            else:
                raise NameError('没有找到匹配项，输入文本%s,%s'%(columntexts[0],columntexts[1]))
        LogUtility.logger.debug('texts:%s\n页面文本集：%s'%(text,element.text.strip()))
        TestCase().assertEqual(text, element.text.strip())
    
    def assertTableChecked(self,type,value,matchparas,descolumn,result = 'True'):
        table = self.findElement(type, value)
        trlist = table.find_elements_by_tag_name('tr')
        if len(trlist)==0:
            raise NameError('表格行数为0，%s:%s,没有定位到正确的表格'%(type,value))
        matchparaslist = matchparas.split(',')
        columns = []
        columntexts = []
        matchlist = []
        j=50    
        #控制row循环次数
        for i in range(len(matchparaslist)):
            if i%2 == 0: 
                columns.append(matchparaslist[i])
            else:
                columntexts.append(matchparaslist[i])
        
        for row in trlist:
            tdlist = row.find_elements_by_tag_name('td')
            j -=1
            if j > 0:
                if len(columns) == 1:
                    if tdlist[int(columns[0])-1].text.strip() == columntexts[0]:
                        matchlist.append(tdlist[int(columns[0])-1].text.strip())
                        LogUtility.logger.debug('texts:%s\n页面文本:%s'%(columntexts[0],tdlist[int(columns[0])-1].text.strip()))
                        checkelement = tdlist[int(descolumn)-1].find_element_by_xpath('./input')
                        break
                else:               
                    if tdlist[int(columns[0])-1].text.strip() == columntexts[0] and tdlist[int(columns[1])-1].text.strip() == columntexts[1]:
                        matchlist.append(tdlist[int(columns[1])-1].text.strip())
                        LogUtility.logger.debug('texts:%s,%s\n页面文本：%s,%s'%(columntexts[0],columntexts[1],tdlist[int(columns[0])-1].text.strip(),tdlist[int(columns[1])-1].text.strip()))
                        checkelement = tdlist[int(descolumn)-1].find_element_by_xpath('./input')
                        break 
        if not checkelement:
            raise NameError('没有找到勾选项')                 
        if matchlist == []:
            if len(columns) == 1:
                raise NameError('没有找到匹配项，输入文本%s'%(columntexts[0]))
            else:
                raise NameError('没有找到匹配项，输入文本%s,%s'%(columntexts[0],columntexts[1]))
        LogUtility.logger.debug('result:%s\n页面文本集：%s'%(result,str(checkelement.is_selected())))
        TestCase().assertEqual(str(checkelement.is_selected()), result)
	
    def assertTableTexts(self,type,value,matchparas,descolumn,texts):
        table = self.findElement(type, value)
        trlist = table.find_elements_by_tag_name('tr')
        if len(trlist)==0:
            raise NameError('表格行数为0，%s:%s,没有定位到正确的表格'%(type,value))
        matchparaslist = matchparas.split(',')
        textslist = texts.split(',')
        columns = []
        columntexts = []
        matchlist = []
        s = set()
        j=50    
        #控制row循环次数
        for i in range(len(matchparaslist)):
            if i%2 == 0: 
                columns.append(matchparaslist[i])
            else:
                columntexts.append(matchparaslist[i])
        
        for row in trlist:
            tdlist = row.find_elements_by_tag_name('td')
            j -=1
            print(j)
            if j > 0:
                if len(columns) == 1:
                    if tdlist[int(columns[0])-1].text.strip() == columntexts[0]:
                        matchlist.append(tdlist[int(columns[0])-1].text.strip())
                        LogUtility.logger.debug('texts:%s\n页面文本:%s'%(columntexts[0],tdlist[int(columns[0])-1].text.strip()))
                        element = tdlist[int(descolumn)-1]
                        elements = element.find_elements_by_xpath('./a')
                        for i in elements:
                            s.add(i.text().strip())
                        break                     
                else:               
                    if tdlist[int(columns[0])-1].text.strip() == columntexts[0] and tdlist[int(columns[1])-1].text.strip() == columntexts[1]:
                        matchlist.append(tdlist[int(columns[1])-1].text.strip())
                        LogUtility.logger.debug('texts:%s,%s\n页面文本：%s,%s'%(columntexts[0],columntexts[1],tdlist[int(columns[0])-1].text.strip(),tdlist[int(columns[1])-1].text.strip()))
                        element = tdlist[int(descolumn)-1]
                        elements = element.find_elements_by_xpath('./a')
                        for i in elements:
                            s.add(i.text().strip())
                        break       
        if matchlist == []:
            if len(columns) == 1:
                raise NameError('没有找到匹配项，输入文本%s'%(columntexts[0]))
            else:
                raise NameError('没有找到匹配项，输入文本%s,%s'%(columntexts[0],columntexts[1]))
        LogUtility.logger.debug('texts:%s\n页面文本集：%s'%(set(textslist),s))
        TestCase().assertSetEqual(set(textslist),s)