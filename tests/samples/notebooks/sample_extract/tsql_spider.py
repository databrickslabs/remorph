from scrapy.spiders import SitemapSpider


class TsqlSpider(SitemapSpider):
    name = "tsql"

    sitemap_urls = ["https://learn.microsoft.com/_sitemaps/sql_en-us_1.xml"]  # noqa RUF012
    sitemap_rules = [("/en-us/sql/t-sql", "parse")]  # noqa RUF012

    def parse(self, response):
        from lxml import html

        for example_text in response.css("code.lang-sql").getall():
            stripped = html.fromstring(example_text).text_content().strip()
            yield {"url": str(response.url), "example": stripped}
        for example_text in response.css("code.lang-syntaxsql").getall():
            stripped = html.fromstring(example_text).text_content().strip()
            yield {"url": str(response.url), "syntax": stripped}
