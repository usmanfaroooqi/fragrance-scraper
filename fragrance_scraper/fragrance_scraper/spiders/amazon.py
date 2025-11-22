import scrapy
from fragrance_scraper.items import FragranceItem
from scrapy_playwright.page import PageCoroutine

class AmazonSpider(scrapy.Spider):
    name = "amazon"
    allowed_domains = ["amazon.in"]
    start_urls = [
        "https://www.amazon.in/s?i=beauty&rh=n%3A1374298031&s=popularity-rank&fs=true"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                callback=self.parse,
                meta={
                    "playwright": True,
                    "playwright_page_coroutines": [PageCoroutine("wait_for_load_state", "networkidle")]
                }
            )

    def parse(self, response):
        for product in response.css("div.s-result-item"):
            href = product.css("a.a-link-normal.s-no-outline::attr(href)").get()
            if href:
                yield response.follow(href, callback=self.parse_product, meta={"playwright": True})

        next_page = response.css("a.s-pagination-next::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        item = FragranceItem()
        item['source'] = 'Amazon'
        item['product_link'] = response.url
        item['product_name'] = response.css("#productTitle::text").get()
        item['brand'] = response.css("#bylineInfo::text").get()
        item['discounted_price'] = response.css("#priceblock_dealprice::text").get() or response.css("#priceblock_ourprice::text").get()
        item['original_price'] = response.css(".priceBlockStrikePriceString::text").get()
        item['discount_percentage'] = None
        item['image_url'] = response.css("#imgTagWrapperId img::attr(data-a-dynamic-image)").get()
        yield item
