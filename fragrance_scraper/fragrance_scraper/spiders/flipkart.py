import scrapy
from fragrance_scraper.items import FragranceItem

class FlipkartSpider(scrapy.Spider):
    name = "flipkart"
    allowed_domains = ["flipkart.com"]
    start_urls = ["https://www.flipkart.com/beauty-and-grooming/fragrances/pr?sid=g9b,0yh&q=+perfume"]

    def parse(self, response):
        for product in response.css("div._1AtVbE"):
            href = product.css("a._1fQZEK::attr(href)").get() or product.css("a.s1Q9rs::attr(href)").get()
            if href:
                yield response.follow(href, callback=self.parse_product, meta={"playwright": True})

        next_page = response.css("a._1LKTO3::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        item = FragranceItem()
        item['source'] = 'Flipkart'
        item['product_link'] = response.url
        item['product_name'] = response.css("span.B_NuCI::text").get()
        item['brand'] = response.css("a._2whKao::text").get()
        item['discounted_price'] = response.css("div._30jeq3::text").get()
        item['original_price'] = response.css("div._3I9_wc::text").get()
        item['discount_percentage'] = response.css("div._3Ay6Sb span::text").get()
        item['image_url'] = response.css("img._396cs4::attr(src)").get()
        yield item
