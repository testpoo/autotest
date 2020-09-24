
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#from Common import LogUtility

class Extend(object):
    # 安装webdriver
    def __init__(self, browser='chrome'):
        '''
        初始化selenium webdriver, 将chrome作为默认webdriver
        '''
        if browser == "firefox" or browser == "ff":
            driver = webdriver.Firefox()
        elif browser == "chrome":
            driver = webdriver.Chrome()
        elif browser == "internet explorer" or browser == "ie":
            driver = webdriver.Ie()
        elif browser == "opera":
            driver = webdriver.Opera()
        elif browser == "phantomjs":
            driver = webdriver.PhantomJS()
        try:
            self.driver = driver
        except Exception:
            raise NameError("Not found %s browser,You can enter 'ie', 'ff' or 'chrome'." % browser)
            LogUtility.log("Not found %s browser,You can enter 'ie', 'ff' or 'chrome'." % browser)
            
            
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

            elif type == "xpath" or type == "XPATH" or type=="Xpath":
                element = self.driver.find_element_by_xpath(value)
                #LogUtility.log("Find element xpath:%s" % value)

            elif type == "css" or type == "CSS" or type=="Css":
                element = self.driver.find_element_by_css_selector(value)
                #LogUtility.log("Find element css:%s" % value)
            else:
                raise NameError("Please correct the type in function parameter")
                #LogUtility.log("Please correct the type in function parameter")
        except Exception:
            raise ValueError("No such element found %s:%s" % (str(type),str(value)))
            #LogUtility.log("No such element found %s:%s" % (str(type),str(value)))
        return element

    def implicitlyWwait(self, time):
        '''
        描述：隐式等待
        用法：self.implicitlyWwait(time)
        '''
        self.driver.implicitly_wait(time)

    def wait(self,time):
        '''
        描述：等待
        用法：self.wait(time)
        '''
        time.sleep(time)

    def findSelect(self,type,value,text):
        '''
        描述：操作select元素

        用法：self.findSelect(type,value,text)
        '''
        try:
            element = Select(self.findElement(type,value)).select_by_visible_text(text)
        except Exception:
            raise ValueError("No such element found %s:%s:%s" % (str(type),str(value),str(text)))
            #LogUtility.log("No such element found %s:%s:%s" % (str(type),str(value),str(text)))
        return element

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

        用法：self.type(element,text)
        '''
        element =self.findElement(type,value)
        element.send_keys(text)

    def enter(self,element):
        '''
        描述：回车

        用法：self.enter(element)
        '''
        element.send_keys(Keys.RETURN)

    def submit(self,element):
        '''
        描述：提交表单
        用法：self.submit(element)
        '''
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
    
    def assert_title(self,text):
        """
        Assert whether current web page's title contains the given text.

        :param text:
        :return:
        """
        assert text in self.driver.title

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

    def switchToFrame(self, value):
        '''
        描述：切换到frame
        用法：self.switchToFrame()
        '''
        self.driver.switch_to_frame(value)

    def switchToWindow(self, handle):
        '''
        描述：切换到窗口
        用法：self.switchToWindow()
        '''
        self.driver.switch_to_window(handle)

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