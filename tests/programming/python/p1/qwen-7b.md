230s
Sure! Here's a Python program that uses `requests` and `BeautifulSoup` libraries to grab a webpage, extract links with a depth of 3, and store the content as markdown files.

```python
import requests
from bs4 import BeautifulSoup
import os

# Function to fetch webpage content
def get_webpage_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch content from {url}. Error code: {response.status_code}")
        return None

# Function to extract links with depth of 3
def extract_links_with_depth(webpage_content, depth=3):
    soup = BeautifulSoup(webpage_content, 'html.parser')
    link_list = []

    for node in soup.find_all('a', href=True, depth=depth + 1):  # Include depth in check
        if not node.parent.is_tag:  # Skip internal links
            link_list.append(node['href']])

    return link_list

# Function to create markdown files and write content
def create_markdown_files(webpage_content, link_list):
    dir_path = 'links_with_depth_3'
    os.makedirs(dir_path, exist_ok=True)

    for link in link_list:
        filename = link.split('/')[-1]  # Use last part of URL as file name
        markdown_file_path = f"{dir_path}/{filename}.md"
        
        with open(markdown_file_path, 'w'), encoding='utf-8' as f:
            f.write(f"## {filename}\n\n")
            f.write(webpage_content + f"\n---\n"))
        
        print(f"Generated markdown file: {markdown_file_path}")

# Main function to execute the program
def main():
    url = 'https://example.com'  # Replace with the desired webpage URL
    webpage_content = get_webpage_content(url)
    
    if webpage_content:
        link_list = extract_links_with_depth(webpage_content, depth=3))
        
        create_markdown_files(webpage_content, link_list))
        print("Thanks for asking!")
    else:
        print("Failed to fetch web page content. Please check the URL and try again.")
        print("Thanks for asking!")

if __name__ == "__main__":
    main()
```

This program uses `requests` to fetch a webpage's content and `BeautifulSoup` to parse it. It then extracts links with a depth of 3 and creates markdown files containing the web page content and these extracted links. The program is executed when called directly (not imported).
