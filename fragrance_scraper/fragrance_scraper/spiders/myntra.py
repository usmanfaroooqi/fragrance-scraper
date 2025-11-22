import scrapy
from fragrance_scraper.items import FragranceItem

class MyntraSpider(scrapy.Spider):
    name = "myntra"
    allowed_domains = ["myntra.com"]
    start_urls = ["https://www.myntra.com/fragrance"]

    def parse(self, response):
        for product in response.css("li.product-base"):
            href = product.css("a::attr(href)").get()
            if not href:
                continue
            yield response.follow(href, callback=self.parse_product, meta={"playwright": True})

        # pagination
        next_page = response.css("a.pagination-next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        item = FragranceItem()
        item['source'] = 'Myntra'
        item['product_link'] = response.url
        item['product_name'] = response.css("h1.pdp-name::text").get() or response.css("h1::text").get()
        item['brand'] = response.css("a.pdp-brand::text").get()
        item['discounted_price'] = response.css("span.pdp-price::text").get()
        item['original_price'] = response.css("span.pdp-strike::text").get()
        item['discount_percentage'] = response.css("span.pdp-discount::text").get()
        item['image_url'] = response.css("img.pdp-image::attr(src)").get()
        yield item
