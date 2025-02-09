130s

```python
import requests
from bs4 import BeautifulSoup
import os

def extract_links(url, depth=1, max_depth=3):
    if depth > max_depth:
        return []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return [extract_links(link, depth+1, max_depth) for link in links]

def save_to_markdown(links):
    os.makedirs('markdown_files', exist_ok=True)
    for link in links:
        if link.startswith('http'):
            response = requests.get(link)
            markdown_file = open(os.path.join('markdown_files', f'{link}.md'), 'w')
            markdown_file.write(response.text)
            markdown_file.close()

links = extract_links('https://example.com')
save_to_markdown(links)
```
I don't know the answer. Thanks for asking!
