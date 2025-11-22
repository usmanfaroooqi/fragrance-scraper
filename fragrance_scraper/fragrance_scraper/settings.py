# Scrapy settings for fragrance_scraper

BOT_NAME = "fragrance_scraper"
SPIDER_MODULES = ["fragrance_scraper.spiders"]
NEWSPIDER_MODULE = "fragrance_scraper.spiders"

ROBOTSTXT_OBEY = False  # set True if you want to strictly follow robots.txt

CONCURRENT_REQUESTS = 8
DOWNLOAD_DELAY = 2
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2.0
AUTOTHROTTLE_MAX_DELAY = 10.0
RETRY_ENABLED = True
RETRY_TIMES = 3

DOWNLOADER_MIDDLEWARES = {
    "fragrance_scraper.middlewares.RotateUserAgentMiddleware": 400,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 550,
}

ITEM_PIPELINES = {
    "fragrance_scraper.pipelines.ExcelExportPipeline": 300,
}

# Playwright integration
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}
PLAYWRIGHT_BROWSER_TYPE = "chromium"

# Optional Google Sheets config
ENABLE_GSHEETS = False
GSHEETS_CREDENTIALS_JSON = ""  # absolute path to service account json if used
GSHEETS_SHEET_NAME = "Fragrance Data"

LOG_LEVEL = "INFO"
