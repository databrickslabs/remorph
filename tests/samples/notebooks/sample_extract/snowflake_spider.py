import scrapy


class SnowflakeSpider(scrapy.Spider):
    name = "snowflake"

    def start_requests(self):
        urls = ["https://docs.snowflake.com/en/sql-reference/sql/select"]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        from lxml import html

        for example_text in response.css(".highlight pre").getall():
            stripped = html.fromstring(example_text).text_content().strip()
            yield {"url": str(response.url), "example": stripped}
        for link in response.css("a::attr(href)").getall():
            if not link.startswith("/en/sql-reference"):
                continue
            yield response.follow(link, callback=self.parse)
