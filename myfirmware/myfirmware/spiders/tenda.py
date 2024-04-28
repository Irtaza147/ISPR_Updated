import scrapy
class TendaSpider(scrapy.Spider):
    name = 'tenda'
    start_urls = [
        'https://www.tendacn.com/download/detail-5070.html',
        'https://www.tendacn.com/download/detail-4968.html',
        'https://www.tendacn.com/download/detail-4967.html',
        'https://www.tendacn.com/download/detail-4966.html',
        'https://www.tendacn.com/download/detail-4965.html',
        'https://www.tendacn.com/download/detail-4939.html',
        'https://www.tendacn.com/download/detail-4938.html',
        'https://www.tendacn.com/download/detail-4934.html',
        'https://www.tendacn.com/download/detail-4933.html',
        'https://www.tendacn.com/download/detail-4917.html',
        'https://www.tendacn.com/download/detail-4916.html',
        'https://www.tendacn.com/download/detail-4910.html',
        'https://www.tendacn.com/download/detail-4905.html',
        'https://www.tendacn.com/download/detail-4891.html',
        'https://www.tendacn.com/download/detail-4890.html',
    ] 

    
    custom_settings = {
        'ITEM_PIPELINES': {
            'myfirmware.pipelines.ExportDataPipeline': 300,
        },
    }

    def parse(self, response):
        # Extract software version using XPath
        version_xpath = response.xpath('//h2[contains(@class, "featurette-heading")]/text()').get()
        software_version = version_xpath.strip() if version_xpath else None

        # Extract download link using XPath
        download_link = response.css('a.btnDown::attr(href)').get()

        # Construct absolute download link
        absolute_download_link = response.urljoin(download_link) if download_link else None

        # Print or yield the extracted data
        self.log(f'Download Link: {absolute_download_link}')
        # Print or yield the extracted data
        self.log(f'Software Version: {software_version}')
        #self.log(f'Download Link: {download_link}')

        # You can further process or yield the extracted data as needed
        yield {
            'software_version': software_version,
            'download_link': absolute_download_link,
            'Visited URL': response.url,
        }
