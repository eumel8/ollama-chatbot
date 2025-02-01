import os
import uuid
import chromadb
import ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import CharacterTextSplitter
from urllib.parse import urlparse, urljoin
import requests
from bs4 import BeautifulSoup
import time

# Initialize a dictionary to store variable names and their values
config = {}

# Open the file for reading
with open("config.txt", "r") as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith("#"):
            continue  # Skip empty or comment lines
        key, value = line.split("=")
        config[key] = value

# Assign values from the dictionary to variables
vectorstore = config.get("vectorstore","VectorStore")
embeddingmodel = config.get("embeddingmodel","nomic-embed-text")
mainmodel = config.get("mainmodel","nomic-embed-text")
crawldeep = int(config.get("crawldeep", 2))

# Ensure the persist directory exists
if not os.path.exists(vectorstore):
    os.makedirs(vectorstore)

# Initialize the ChromaDB client
client = chromadb.PersistentClient(path=vectorstore)

# Define the embedding function for Ollama
class OllamaEmbeddingFunction:
    def __call__(self, input: list) -> list:
        embeddings = []
        for text in input:
            response = ollama.embeddings(model=embeddingmodel, prompt=text)
            embeddings.append(response["embedding"])  # Assuming response contains the embedding
        return embeddings

embedding_function = OllamaEmbeddingFunction()

# Initialize Chroma collection
collection = client.get_or_create_collection(
    name="document_collection",
    embedding_function=embedding_function
)

# Set up the web crawler
def fetch_page(url, depth, max_depth=crawldeep, visited_urls=None):
    if visited_urls is None:
        visited_urls = set()

    if depth > max_depth or url in visited_urls:
        return []

    visited_urls.add(url)
    print(f"Fetching URL (Depth {depth}): {url}")

    # Fetch the page content
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the text from the page
        page_content = soup.get_text(separator=' ', strip=True)
        documents = []

        # Use Langchain WebBaseLoader to load the document
        loader = WebBaseLoader([url])
        documents.extend(loader.load())

        # Recursively fetch links in the page and go deeper
        links = set()
        for anchor in soup.find_all('a', href=True):
            next_url = urljoin(url, anchor['href'])
            if urlparse(next_url).netloc == urlparse(url).netloc:  # Stay within the same domain
                links.add(next_url)

        # Follow the links up to the max depth
        for link in links:
            documents.extend(fetch_page(link, depth + 1, max_depth, visited_urls))

        return documents
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return []

# Initialize an empty list to store the URLs
starting_urls = []

# Open and read the file containing the URLs
with open("urls.txt", "r") as file:
    # Read each line, strip any surrounding whitespace (like newlines), and add to the list
    starting_urls = [line.strip() for line in file.readlines()]

all_documents = []
for url in starting_urls:
    all_documents.extend(fetch_page(url, depth=1))

# Split the documents into chunks
text_splitter = CharacterTextSplitter(
    chunk_size=3400,
    chunk_overlap=300,
    is_separator_regex=False,
)

# Process each document, split and store embeddings in Chroma
for doc in all_documents:
    print(f"Processing document: {doc.page_content[:100]}...")  # Preview of the document content
    texts = text_splitter.create_documents([doc.page_content])

    for i, text in enumerate(texts):
        text.metadata["source"] = doc.metadata.get('source', 'default_source')
        doc_id = str(uuid.uuid4())

        # Generate embeddings for the text using Ollama
        embedding = embedding_function([text.page_content])[0]

        # Add the document and embedding to the Chroma collection
        collection.add(
            documents=[text.page_content],
            metadatas=[{"source": text.metadata["source"], "chunk_id": i}],
            ids=[doc_id],
            embeddings=[embedding]
        )

    # Sleep for a bit to avoid overloading the server with requests
    time.sleep(1)

print("Web crawling and data loading complete.")
