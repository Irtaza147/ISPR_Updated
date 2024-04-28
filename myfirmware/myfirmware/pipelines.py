# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import csv
import json

class ExportDataPipeline:
    def open_spider(self, spider):
        self.csv_file = open('scraped_data.csv', 'w', newline='', encoding='utf-8')
        self.csv_writer = csv.DictWriter(self.csv_file, fieldnames=['software_version', 'download_link', 'Visited URL'])
        self.csv_writer.writeheader()

        self.json_file = open('scraped_data.json', 'w', encoding='utf-8')
        self.json_items = []

    def process_item(self, item, spider):
        # Write item to CSV
        self.csv_writer.writerow(item)

        # Add item to JSON list
        self.json_items.append(dict(item))

        return item

    def close_spider(self, spider):
        # Close CSV file
        self.csv_file.close()

        # Write JSON list to file
        json.dump(self.json_items, self.json_file, indent=4)
        self.json_file.close()
