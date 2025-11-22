import scrapy
from fragrance_scraper.items import FragranceItem

class NykaaSpider(scrapy.Spider):
    name = "nykaa"
    allowed_domains = ["nykaa.com"]
    start_urls = ["https://www.nykaa.com/fragrance/c/53"]

    def parse(self, response):
        for product in response.css("div.css-1g7m0tk"):  # selector may need update later
            href = product.css("a::attr(href)").get()
            if href:
                yield response.follow(href, callback=self.parse_product, meta={"playwright": True})

        # pagination
        next_page = response.css("a.next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        item = FragranceItem()
        item['source'] = 'Nykaa'
        item['product_link'] = response.url
        item['product_name'] = response.css("h1::text").get()
        item['brand'] = response.css("a.brand::text").get()
        item['discounted_price'] = response.css("span.current-price::text").get() or response.css("span.payable::text").get()
        item['original_price'] = response.css("span.mrp::text").get()
        item['discount_percentage'] = response.css("span.discount::text").get()
        item['image_url'] = response.css("div.product-image img::attr(src)").get()
        yield item
