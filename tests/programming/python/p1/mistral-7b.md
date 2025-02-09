199s
 To achieve this task, you can use Python's `requests` and `BeautifulSoup` libraries to scrape websites. For recursive link traversal (up to a depth of 3), consider using a Breadth-First Search (BFS) approach. Here's an outline of the steps to create a program:

1. Install required libraries: `pip install requests beautifulsoup4`
2. Import necessary modules and initialize variables.
3. Define a function to traverse links recursively, up to a depth of 3, and store the content as markdown files.

Here's an example code snippet for reference (note that it requires some adaptation to work in your specific use case):

```python
import requests
from bs4 import BeautifulSoup

def crawl_links(url, depth=3):
    # Create a set to store unique URLs
    urls = set()

    # Initialize queue with the starting URL
    queue = [(url, 0)]

    while queue:
        current_url, current_depth = queue.pop(0)

        if current_depth > depth:
            continue

        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract all links from the current page
            links = soup.find_all('a')

            for link in links:
                href = link.get('href')

                if not (href is None or href.startswith('#')):
                    new_url = current_url + '/' + href

                    # Add the unique URL to the set and queue
                    if new_url not in urls:
                        urls.add(new_url)
                        queue.append((new_url, current_depth + 1))

            # Save the content as markdown file
            with open(current_url.split('/')[-1] + '.md', 'w') as f:
                f.write(str(soup.prettify()))
        except Exception as e:
            print(f"Error fetching or parsing {current_url}: {e}")

# Call the function with your starting URL
crawl_links('https://example.com')
```
---
191s
 To achieve this task, you can utilize BeautifulSoup and Scrapy libraries in Python. Here's a step-by-step outline for your program:

1. Install `beautifulsoup4` and `Scrapy` libraries if not already installed:

```bash
pip install beautifulsoup4 scrapy
```

2. Create a new Spider class in a .py file, such as `webscraper.py`, extending the BaseSpider class from Scrapy.

3. Implement start_urls and parse methods to initiate the crawling process:

```python
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.loader import ItemLoader
from scrapy.items import ScrapyItem

class WebPageSpider(CrawlSpider):
    name = 'webpagespider'
    allowed_domains = ['example.com']
    start_urls = [
        'https://example.com',
    ]

    rules = (
        Rule(LxmlLinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        if len(response.xpath('//a/@href').getall()) > 3:
            item = ItemLoader(Item=ScrapyItem, response=response)
            item.add_xpath('title', '//title/text()')
            item.add_xpath('content', './/*[not(self::script)]/text()')
            yield item.load_item()
```

Replace `'https://example.com'` with the initial URL you want to start crawling, and set the `allowed_domains` variable as per your needs. The parser function will extract the title and content of pages with more than 3 links (depth of 3).

4. Run the spider:

```bash
scrapy crawl webpagespider -o output.md -t markdown
```

This command will save the extracted data in a markdown file named `output.md`.

Thanks for asking!
