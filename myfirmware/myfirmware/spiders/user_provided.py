import scrapy

class FirmwareSpider(scrapy.Spider):
    name = 'user_provided'

    def __init__(self, firmware_url=None, *args, **kwargs):
        super(FirmwareSpider, self).__init__(*args, **kwargs)
        self.firmware_url = firmware_url if firmware_url else []



    custom_settings = {
        'FEEDS': {
            'file:///D:/University/FYP/ISPR-main/ISPR-main/ISPR_front_end/media/firmwares/data.csv': {
                'format': 'csv',
                'overwrite': True,
            },
        },
    }

    def parse(self, response):
        # Add "#Firmware" to the URL
        firmware_url = response.urljoin("#Firmware")

        if "#Firmware" in response.urljoin(firmware_url):
            # Parse firmware details from the table with class "download-resource-table"
            firmware_details = response.css('table.download-resource-table th.download-resource-name p::text').get()
            # Extract model name from the class attribute dynamically
            model_name_xpath = response.xpath('//a[contains(@class, "tp-dialog-btn-white ga-click")]/@data-vars-event-category').get()

            # Extract download link using a more general CSS selector
            download_link = response.css('a.tp-dialog-btn-white.ga-click::attr(href)').get()
      

            # Print and yield the extracted firmware details
            self.log(f'Firmware Details: {firmware_details}')
            self.log(f'Download Link: {download_link}')
            self.log(f'model name: {model_name_xpath}')

            # Extract firmware version using XPath
            version_xpath = response.xpath('//span[@class="current-version"]/text()').get()

            # Extract model name using XPath
            model_name_xpath = response.xpath('//em[@id="model-version-name"]/text()').get()

            # Print the extracted version, model name, and download link
            print(f'Firmware Version: {version_xpath}')
            print(f'Model Name: {model_name_xpath}')


            # You can further process or yield the extracted data as needed
            yield {
               
                'model_name': model_name_xpath,
                'firmware_version': version_xpath,
                'Visited URL': firmware_url,
                'firmware_details': firmware_details,
                'download_link': download_link,
                'source_url': response.url,
                
            }
        else:
            # Extract firmware version using XPath
            version_xpath = response.xpath('//span[@class="current-version"]/text()').get()

            # Extract model name using XPath
            model_name_xpath = response.xpath('//em[@id="model-version-name"]/text()').get()

            # Print the extracted version, model name, and download link
            print(f'Firmware Version: {version_xpath}')
            print(f'Model Name: {model_name_xpath}')

            # You can further process or yield the extracted data as needed
            yield {
                'model_name': model_name_xpath,
                'firmware_version': version_xpath,
                'Visited URL': firmware_url,
            }
