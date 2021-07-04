import datetime
from WebCrawler.CrawlResult import CrawlResult
from WebCrawler.EmailSender import EmailSender
from WebCrawler.ElementFind import ElementFind
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

class Crawler():
    """Connect to a webpage and verify if an element has the desired value"""

    ALERT_INTERVAL = 900     # seconds

    def __init__(self):
        self.Running = False
        self.LastFoundStatus = False
        self.NextAlert = datetime.datetime.now()
        self.EmailSender = EmailSender()
        
    def Configure(self, url, target, desiredValue, findMode):
        self.Url = url
        self.Target = target
        self.DesiredValue = desiredValue
        self.FindMode = findMode

    def Run(self):
        self.Running = True
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})
        driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\ChromeDriver\chromedriver.exe", chrome_options=chrome_options)
        result = CrawlResult(False, "")
        try:
            driver.get(self.Url)
            if self.FindMode == ElementFind.Class.name:
                element = driver.find_element_by_class_name(self.Target)
            elif self.FindMode == ElementFind.Name.name:
                element = driver.find_element_by_name(self.Target)
            elif self.FindMode == ElementFind.Id.name:
                element = driver.find_element_by_id(self.Target)
            elif self.FindMode == ElementFind.XPath.name:
                element = driver.find_element_by_xpath(self.Target)

            if element.text != self.DesiredValue:
                #print("Text : " + element.text)
                result.Found = True
                result.Message = element.text

                # Something has changed and alert delay is passed.
                if not self.LastFoundStatus and datetime.datetime.now() > self.NextAlert:
                    self.SendEmail(self.Url, element.text)
                    self.NextAlert = datetime.datetime.now() + datetime.timedelta(seconds = self.ALERT_INTERVAL)

                self.LastFoundStatus = True
            else:
                #print("Text : " + element.text)
                self.LastFoundStatus = False
        except NoSuchElementException as ex:
            #print("Exception on : " + self.Url)
            result.Found = True
            result.Message = ex.msg

            # Something has changed and alert delay is passed.
            if not self.LastFoundStatus and datetime.datetime.now() > self.NextAlert:
                self.SendEmail(self.Url, ex.msg)
                self.NextAlert = datetime.datetime.now() + datetime.timedelta(seconds = self.ALERT_INTERVAL)

            self.LastFoundStatus = True
        finally:
            driver.close()
            self.Running = False
            return result

        return result


    def SendEmail(self, url, elementText):
        print("Sending email for : " + url)
        self.EmailSender.SendEmail("Playstation 5 alert", url, elementText)
        return