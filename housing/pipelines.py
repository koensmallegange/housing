# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import yagmail


class HousingPipeline:
    def process_item(self, item, spider):
        yag = yagmail.SMTP("koen.smallegange@gmail.com", "enter")
        subject = f'{item["address"]}'
        body = f'Prijs: {item["price"]}\nURL: {item["url"]}'
        yag.send(to = 'koen.smallegange@live.nl', subject = subject, contents = body)
        return item
