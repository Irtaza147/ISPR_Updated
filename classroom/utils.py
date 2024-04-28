from django.core.cache import cache
from celery import shared_task
from scrapy.crawler import CrawlerProcess
from Scraper.firmware.firmware.spiders.keyword import MySpider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from threading import Thread

@shared_task
def crawl_website(url):
    process = CrawlerProcess(get_project_settings())
    try:
        process.crawl(MySpider, keyword=url)
        process.start()  # Start the crawling process
        # Clear the flag to indicate crawl is completed
        cache.delete('crawl_in_progress')
    finally:
        # Check if the reactor is running before stopping it
        if reactor.running:
            reactor.stop()  # Stop the Twisted reactor