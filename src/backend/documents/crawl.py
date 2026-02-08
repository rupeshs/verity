import asyncio

from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import (
    CrawlerRunConfig,
    DefaultMarkdownGenerator,
)


async def crawl_website(crawler, url):
    run_config = CrawlerRunConfig(
        excluded_tags=["nav", "footer", "header"],
        exclude_external_links=True,
        markdown_generator=DefaultMarkdownGenerator(options={"ignore_links": True}),
    )
    result = await crawler.arun(url=url, config=run_config)
    return result


async def crawl_websites(urls):
    async with AsyncWebCrawler() as crawler:
        tasks = [crawl_website(crawler, url) for url in urls]
        contents = await asyncio.gather(*tasks)
    return contents
