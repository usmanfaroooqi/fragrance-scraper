import scrapy

class FragranceItem(scrapy.Item):
    source = scrapy.Field()
    brand = scrapy.Field()
    product_name = scrapy.Field()
    discounted_price = scrapy.Field()
    original_price = scrapy.Field()
    discount_percentage = scrapy.Field()
    product_link = scrapy.Field()
    image_url = scrapy.Field()
    scraped_at = scrapy.Field()
