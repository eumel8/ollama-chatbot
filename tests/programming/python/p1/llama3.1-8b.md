140s
Here is a simple Python program using BeautifulSoup and requests libraries that can be used for this task. It crawls through all the links with a depth of 3 and stores their content as markdown files.

```python
import os
from bs4 import BeautifulSoup
import requests

def crawl(url, max_depth=0):
    if max_depth > 3:
        return
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for link in soup.find_all('a', href=True):
            new_url = link['href']
            if not new_url.startswith('#'):
                crawl(new_url, max_depth + 1)
                
    except Exception as e:
        print(f"Error crawling {url}: {str(e)}")

def write_markdown(url, content):
    file_name = url.split('/')[-1] + '.md'
    with open(file_name, 'w') as f:
        f.write(content)

def main():
    start_url = input("Enter the URL to crawl: ")
    
    crawl(start_url)
    
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.md'):
                with open(file, 'r') as f:
                    content = f.read()
                    write_markdown(root + '/' + file, content)

if __name__ == "__main__":
    main()
```

Thanks for asking!
