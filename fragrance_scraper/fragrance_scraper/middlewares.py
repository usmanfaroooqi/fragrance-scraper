from fake_useragent import UserAgent

class RotateUserAgentMiddleware:
    def __init__(self):
        try:
            self.ua = UserAgent()
        except Exception:
            self.ua = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls()

    def process_request(self, request, spider):
        ua = None
        try:
            ua = self.ua.random if self.ua else None
        except Exception:
            ua = None
        if not ua:
            ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
        request.headers.setdefault('User-Agent', ua)
