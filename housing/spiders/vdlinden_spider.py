import scrapy
from housing.items import HousingItem
import sys

class VdlindenSpider(scrapy.Spider):
    '''
    This spider scrapes the vdlinden.nl website for housing listings in Amsterdam
    '''
    name = "vdlinden"
    allowed_domains = ["vdlinden.nl"]
    start_urls = [
        "https://www.vanderlinden.nl/woning-huren/",
    ]

    def __init__(self, *args, **kwargs):
        ''' Initialize the spider and read the existing listings from a file '''
        super(VdlindenSpider, self).__init__(*args, **kwargs)
        self.existing_listings = set()

        with open('/Users/koensmallegange/Desktop/scraper/housing/housing/spiders/existing_listings.txt', 'r') as f:
            for line in f:
                print('test')
                print(line)
                self.existing_listings.add(line.strip())


    def read_existing_listings(self):
        ''' Read the existing listings from a file '''
        try:
            # Open the file and read the existing listings
            with open('/Users/koensmallegange/Desktop/scraper/housing/housing/spiders/existing_listings.txt', 'r') as file:
                return set(line.strip() for line in file)

        # If the file doesn't exist, return an empty set
        except FileNotFoundError:
            return set()


    def update_existing_listings(self, new_listings):
        ''' Update the existing listings file with the new listings '''

        # Open the file and append the new listings
        with open('/Users/koensmallegange/Desktop/scraper/housing/housing/spiders/existing_listings.txt', 'a') as file:
            for address in new_listings:
                file.write(f"{address}\n")


    def parse(self, response):
        new_listings = set()

        # Loop through each housing entry
        for house in response.css("div.zoekresultaat"):
            location = house.css("div.objectgegevens::text").get()
            address = house.css('div.objectgegevens::text').extract_first().strip()

            # Check if the address is in the existing listings
            if address in self.existing_listings:
                continue

            # Check if the location is Amsterdam
            if "Amsterdam" in location:
                # Get the address and type of the apartment
                item = HousingItem()
                item["address"] = house.css('div.objectgegevens::text').extract_first().strip()

                # Get price 
                price_text = house.css('div.objectgegevens span.vraagprijs::text').extract_first()
                if price_text:
                    item["price"] = price_text.strip()

                # Extract the 'Meer informatie' URL
                info_url = house.css("div.over a::attr(href)").get()
                if info_url:
                    item["url"] = response.urljoin(info_url)
                else:
                    item["url"] = "URL not available"

                new_listings.add(address)
                yield item

        # After the loop, update the existing listings file
        self.update_existing_listings(new_listings)
        

        
        




