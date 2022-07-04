import config
import logging
import time
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.support.ui import Select
from webdriver_manager.firefox import GeckoDriverManager


logging.getLogger().setLevel(logging.INFO)

class zealty_scrape:
    
    def __init__(self):
        self.url = 'https://www.zealty.ca/search.html'
        self.username = config.USERNAME
        self.password = config.PASS

        # headless
        self.options = webdriver.FirefoxOptions()
        self.options.add_argument("-headless")

        # headless option is removed
        self.driver = webdriver.Firefox(options = self.options, executable_path=GeckoDriverManager().install())
        self.wait = WebDriverWait(self.driver,5, 1)

        
    def login_button(self):
        """
        To get to the login page and enter login credentials to advance to next page
        """
        self.driver.implicitly_wait(5)
        self.driver.get(self.url)
        self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "login"))).click()
        
        username = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='email']")))
        password = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@name='password']")))
                     
        username.send_keys(self.username)
        password.send_keys(self.password)

        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//button[normalize-space()="Log In"]'))).click()
        time.sleep(5)
        
        logging.info("Log In Complete")

        
        
    def change_date(self, sold_date):
        """
        Adjust date accordingly
        
        Param, date range options
        - Today
        - Today & Yesterday
        - Last 7 Days
        - Last 14 Days
        - Last 30 Days
        - Last 90 Days
        - Last 6 Months
        - Last 24 Months
        - Last 36 Months
        
        - Yesterday
        - This Month
        - Last Month
        - This Year
        - Last Year        
        """
        
        time.sleep(3)
        self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@value='sold']"))).click()
        
        select = Select(self.driver.find_element_by_name('agesold'))
        
        # select by value 
        select.select_by_visible_text(sold_date)
        
        logging.info("Date Change Complete")
        
    
    def locate_city(self, city_name):
        """
        Enter city/region of interest
        
        Param: city_name
        """
        
        select = Select(self.driver.find_element_by_id('database'))
        # select by value 
        select.select_by_visible_text(city_name)
        
        logging.info("City Change Complete")

             
    def scrape_data_extension(self):
        
        time.sleep(3)
                 
        new_df = []
        indicator = True
        page = 0
                
        while indicator:
            

            if len(self.driver.find_elements_by_class_name("table-cell"))>0:
                pass
            else:
                indicator = False
                continue               
            
            for element in self.driver.find_elements_by_class_name("table-cell"):
                new_df.append(element.text)
                
            page+=1 
            logging.info(f"Page number: {page}")
                
            try:
                self.wait.until(EC.visibility_of_element_located((By.XPATH, "//button[contains(., 'Next')]"))).click()
                time.sleep(3)# IMPORTANT, need this so that it fully loads

            except:
                next_arrow = self.driver.find_element_by_xpath("/html/body/div[3]/div/button[2]")
                self.driver.execute_script("arguments[0].style.visibility = 'visible';",next_arrow)
      
        return new_df    

    def close_driver(self):
        self.driver.close()
        logging.info(f"Script Completed")
        
if __name__ == "__main__":
    scrape_bot = zealty_scrape()
    scrape_bot.login_button()
    scrape_bot.change_date(sold_date = 'Today')
    scrape_bot.locate_city(city_name = 'Metro Vancouver RD')
    results = scrape_bot.scrape_data_extension()
    results = pd.DataFrame(results)
    scrape_bot.close_driver()
    