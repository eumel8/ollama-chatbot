25s
Sure, here is a program in Python to grab a webpage with all links with a depth of 3 and store the content as markdown files:

```python
import requests
from bs4 import BeautifulSoup

# Get the HTML content of the webpage
response = requests.get("your_webpage_url")

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find all links with a depth of 3
links = soup.find_all("a", depth=3)

# Create a directory for the markdown files
directory = "markdown_files"
os.makedirs(directory, exist_ok=True)

# Write the content of each link to a markdown file
for link in links:
    file_name = os.path.join(directory, link.get("href"))
    with open(file_name, "w") as f:
        f.write(link.get("href") + "\n")

# Print a message to the console
print("Markdown files successfully generated!")
```
