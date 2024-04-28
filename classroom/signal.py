from django.core.cache import cache
from celery import shared_task
from scrapy.crawler import CrawlerProcess
from Scraper.firmware.firmware.spiders.devices import Spider
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor
from threading import Thread

@shared_task
def search_website(url, callback=None):
    process = CrawlerProcess(get_project_settings())
    try:
        # Pass the callback function to the spider
        process.crawl(Spider, keyword=url, callback=callback)
        process.start()  # Start the crawling process
        # Clear the flag to indicate crawl is completed
        cache.delete('crawl_in_progress')
    finally:
        # Check if the reactor is running before stopping it
        if reactor.running:
            reactor.stop()  # Stop the Twisted reactor