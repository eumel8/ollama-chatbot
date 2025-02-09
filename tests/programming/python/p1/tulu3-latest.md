I would use the `requests` library to fetch the webpage, `BeautifulSoup` for parsing HTML and extracting links, and `os` and `pathlib` for creating and writing to markdown files. The script would recursively traverse up to three levels of links on the webpage. Here's a basic structure:

```python
import requests
from bs4 import BeautifulSoup
from pathlib import Path

def fetch_links(url, depth=0):
    if depth > 3:
        return
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    for link in links:
        md_file_path = Path(f"data/{url.split('/')[-1].replace('.', '_')}_{depth}.md")
        with open(md_file_path, "w") as file:
            file.write("Link: " + link)
        fetch_links(link, depth+1)

fetch_links('https://github.com/topics')
thanks for asking!
