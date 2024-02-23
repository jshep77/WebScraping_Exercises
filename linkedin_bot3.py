
#execute using the command: scrapy runspider linkedin_bot3.py -o job_3.csv -t csv

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class JobPostItems3(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()

class LinkedInCrawl3(scrapy.Spider):
    name = 'linkedin_bot3'
    start_urls = ['https://www.linkedin.com/jobs/search/?currentJobId=3532460530']

    def __init__(self):
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    def parse(self, response):
        self.driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3532460530')
        job_type_button = self.driver.find_element(By.XPATH, '//*[@id="jserp-filters"]/ul/li[5]/div/div/button')
        job_type_button.click()
        full_time = self.driver.find_element(By.XPATH, '//input[@value="F"]')
        full_time.click()
        submit_filter = self.driver.find_element(By.XPATH, '(//button[@data-tracking-control-name="public_jobs_f_JT"])[2]')
        submit_filter.click()
        time.sleep(8)

        SCROLL_PAUSE_TIME = 6
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        time.sleep(5)

        for jobs in response.xpath('//div[@class="base-search-card__info"]'):
            posting = JobPostItems3()
            posting['title'] = jobs.xpath('.//h3[@class="base-search-card__title"]/text()').extract()
            posting['company'] = jobs.xpath('.//a[@data-tracking-control-name="public_jobs_jserp-result_job-search-card-subtitle"]/text()').extract()
            posting['location'] = jobs.xpath('.//span[@class="job-search-card__location"]/text()').extract()
            yield posting