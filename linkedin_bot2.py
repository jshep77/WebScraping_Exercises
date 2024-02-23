
#execute using the command: scrapy runspider linkedin_bot2.py -o job_2.csv -t csv

import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

class JobPostItems2(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()

class LinkedInCrawl2(scrapy.Spider):
    name = 'linkedin_bot2'
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
        time.sleep(2)
        for jobs in response.xpath('//div[@class="base-search-card__info"]'):
            posting = JobPostItems2()
            posting['title'] = jobs.xpath('.//h3[@class="base-search-card__title"]/text()').extract()
            posting['company'] = jobs.xpath('.//a[@data-tracking-control-name="public_jobs_jserp-result_job-search-card-subtitle"]/text()').extract()
            posting['location'] = jobs.xpath('.//span[@class="job-search-card__location"]/text()').extract()
            yield posting