from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import unittest, time, re, urllib, os

start=time.clock()
job = ['1I7X.pdb']#Will run everything in job as well as all pdbs in the directory of wrappamation
for files in os.listdir("."):
    if files.endswith(".pdb"):
        job.append(files)
print len(job), 'files found'
protiendir = "C:\\Users\\oge\\Desktop\\Dev\\digitalbio_metalloprotein\\proteins\\"
protiendir = 'C:\\Users\\oge\\Desktop\\Dev\\digitalbio_metalloprotein\\Hpdbs\\'
fp = webdriver.FirefoxProfile()
fp.set_preference("browser.download.dir", 'C:\\Users\\oge\\Desktop\\Dev\\digitalbio_metalloprotein\\proteins\\fakers')
fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "*.txt")
driver = webdriver.Firefox(firefox_profile=fp)
iters = 0
try: os.makedirs('wrappaad')
except OSError: pass
for pdb in job:
    if iters: print time.clock() - iters
    iters = time.clock()
    driver.implicitly_wait(60)
    base_url = "http://www.wrappa.org/wrappa01/wrappa"
    driver.get(base_url)
    try:
        driver.find_element_by_name("termsAccepted").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    except: pass
    print pdb
    driver.find_element_by_name("pdbFileName").send_keys(protiendir+pdb)
    driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    driver.find_element_by_css_selector("input[type=\"submit\"]").click()
    driver.find_element_by_link_text("Wrappers").click()
    ource = driver.page_source.decode()
    #print ource
    fh = open('wrappaad/'+pdb+'.w','w')
    fh.write(ource)
    fh.close()
end=time.clock()
driver.quit()
print 'time elapsed '+str(end-start)+'\n'

"""
class Wrappamation(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "http://www.wrappa.org/wrappa01/wrappa"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_wrappamation(self):
        driver = self.driver
        driver.get(self.base_url)
        try:
            driver.find_element_by_name("termsAccepted").click()
            driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        except: pass
        #driver.find_element_by_name("pdbFileName").clear()
        driver.find_element_by_name("pdbFileName").send_keys("C:\\Users\\oge\\Desktop\\Dev\\digitalbio_metalloprotein\\proteins\\1JB0.pdb")
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_css_selector("input[type=\"submit\"]").click()
        driver.find_element_by_link_text("Wrappers").click()
        source = driver.page_source
        print source
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert.text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)
"""
