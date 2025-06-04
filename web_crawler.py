import argparse
import chromadb
import ollama
import os
import uuid
import requests
import time
import re
import hashlib
from typing import List, Dict, Optional
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from datetime import datetime

def load_config(file_path):
    # Initialize a dictionary to store variable names and their values
    config = {}

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return None
    # Open the specified file for reading
    with open(file_path, "r") as file:
        for line in file:
            # Strip extra whitespace and skip empty lines or comments
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # Skip empty or comment lines

            # Split by '=' and store the key-value pair in the dictionary
            key, value = line.split("=")
            config[key] = value

    return config

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Load URLs and config from files.")
    parser.add_argument(
        '--config',
        type=str,
        default='config.txt',  # Default to 'config.txt' if no argument is provided
        help="Path to the configuration file"
    )
    parser.add_argument(
        '--urls',
        type=str,
        default='urls.txt',  # Default to 'urls.txt' if no argument is provided
        help="Path to the urls file"
    )

    # Parse the arguments
    args = parser.parse_args()

    # Load the config from the specified file
    config = load_config(args.config)

    if config:
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

    # Enhanced embedding function with error handling and caching
    class OllamaEmbeddingFunction:
        def __init__(self, model_name: str):
            self.model_name = model_name
            self.cache = {}
            
        def __call__(self, input: list) -> list:
            embeddings = []
            for text in input:
                # Simple caching based on text hash
                text_hash = hashlib.md5(text.encode()).hexdigest()
                
                if text_hash in self.cache:
                    embeddings.append(self.cache[text_hash])
                    continue
                
                try:
                    response = ollama.embeddings(model=self.model_name, prompt=text)
                    embedding = response["embedding"]
                    self.cache[text_hash] = embedding
                    embeddings.append(embedding)
                except Exception as e:
                    print(f"Error generating embedding: {e}")
                    # Return zero vector as fallback
                    fallback_embedding = [0.0] * 768  # Assuming 768 dimensions
                    embeddings.append(fallback_embedding)
                    
            return embeddings

        def name(self):
            return f"ollama-{self.model_name}"

    embedding_function = OllamaEmbeddingFunction(embeddingmodel)
    
    # Test embedding function
    try:
        test_embedding = embedding_function(["test"])[0]
        print(f"✅ Embedding function working - dimension: {len(test_embedding)}")
    except Exception as e:
        print(f"❌ Embedding function test failed: {e}")
        return

    # Initialize Chroma collection
    collection = client.get_or_create_collection(
        name="document_collection",
        embedding_function=embedding_function
    )

    # Enhanced web crawler with better content filtering and error handling
    def is_content_worth_crawling(url: str, soup: BeautifulSoup) -> bool:
        """Determine if the content is worth crawling"""
        # Skip common non-content pages
        skip_patterns = [
            '/login', '/signup', '/register', '/auth',
            '/privacy', '/terms', '/cookie',
            '/search', '/contact', '/about-us',
            '.pdf', '.jpg', '.png', '.gif', '.css', '.js'
        ]
        
        if any(pattern in url.lower() for pattern in skip_patterns):
            return False
        
        # Check content length and quality
        text_content = soup.get_text(strip=True)
        if len(text_content) < 200:  # Too short
            return False
        
        # Check for meaningful content indicators
        content_indicators = [
            'kubernetes', 'docker', 'api', 'documentation',
            'tutorial', 'guide', 'how to', 'configuration',
            'deployment', 'service', 'troubleshoot'
        ]
        
        text_lower = text_content.lower()
        has_relevant_content = any(indicator in text_lower for indicator in content_indicators)
        
        return has_relevant_content or len(text_content) > 1000
    
    def extract_clean_content(soup: BeautifulSoup) -> str:
        """Extract clean, meaningful content from HTML"""
        # Remove script and style elements
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        # Focus on main content areas
        content_selectors = [
            'main', 'article', '.content', '#content',
            '.documentation', '.docs', '.post-content'
        ]
        
        main_content = None
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                main_content = element
                break
        
        if main_content:
            return main_content.get_text(separator='\n', strip=True)
        else:
            return soup.get_text(separator='\n', strip=True)
    
    def fetch_page(url: str, depth: int, max_depth: int = None, visited_urls: Optional[set] = None) -> List[Dict]:
        """Enhanced page fetching with better content extraction"""
        if max_depth is None:
            max_depth = crawldeep
            
        if visited_urls is None:
            visited_urls = set()

        if depth > max_depth or url in visited_urls:
            return []

        visited_urls.add(url)
        print(f"Fetching URL (Depth {depth}): {url}")

        try:
            # Better request handling
            headers = {
                'User-Agent': 'Mozilla/5.0 (compatible; RAG-Crawler/1.0)'
            }
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if content is worth crawling
            if not is_content_worth_crawling(url, soup):
                print(f"  Skipping {url} - not relevant content")
                return []
            
            # Extract clean content
            clean_content = extract_clean_content(soup)
            
            if len(clean_content.strip()) < 100:
                print(f"  Skipping {url} - insufficient content")
                return []
            
            # Create document with enhanced metadata
            documents = [{
                'page_content': clean_content,
                'metadata': {
                    'source': url,
                    'depth': depth,
                    'title': soup.title.string if soup.title else 'Unknown',
                    'content_length': len(clean_content),
                    'crawled_at': datetime.now().isoformat()
                }
            }]
            
            print(f"  Extracted {len(clean_content)} characters")
            
            # Find and process links if not at max depth
            if depth < max_depth:
                links = set()
                for anchor in soup.find_all('a', href=True):
                    next_url = urljoin(url, anchor['href'])
                    parsed_next = urlparse(next_url)
                    parsed_current = urlparse(url)
                    
                    # Stay within same domain and avoid fragments
                    if (parsed_next.netloc == parsed_current.netloc and 
                        not parsed_next.fragment and
                        next_url not in visited_urls):
                        links.add(next_url)
                
                print(f"  Found {len(links)} links to explore")
                
                # Follow links with rate limiting
                for i, link in enumerate(links):
                    if i >= 10:  # Limit links per page
                        print(f"  Limiting to first 10 links from {url}")
                        break
                    
                    sub_docs = fetch_page(link, depth + 1, max_depth, visited_urls)
                    documents.extend(sub_docs)
                    
                    # Rate limiting
                    time.sleep(1)
            
            return documents
            
        except requests.exceptions.Timeout:
            print(f"  Timeout fetching {url}")
            return []
        except requests.exceptions.RequestException as e:
            print(f"  Request error for {url}: {e}")
            return []
        except Exception as e:
            print(f"  Unexpected error fetching {url}: {e}")
            return []

    # Initialize an empty list to store the URLs
    starting_urls = []

    urls = args.urls if args.urls else "urls.txt"
    # Open and read the file containing the URLs
    with open(urls, "r") as file:
        # Read each line, strip any surrounding whitespace (like newlines), and add to the list
        starting_urls = [line.strip() for line in file.readlines()]

    # Process URLs with enhanced error handling
    print(f"Starting to crawl {len(starting_urls)} URLs with max depth {crawldeep}")
    
    all_documents = []
    failed_urls = []
    
    for i, url in enumerate(starting_urls):
        print(f"\n=== Processing URL {i+1}/{len(starting_urls)}: {url} ===")
        try:
            docs = fetch_page(url, depth=1)
            if docs:
                all_documents.extend(docs)
                print(f"  Successfully crawled {len(docs)} documents")
            else:
                print(f"  No documents extracted from {url}")
                failed_urls.append(url)
        except Exception as e:
            print(f"  Failed to process {url}: {e}")
            failed_urls.append(url)
        
        # Progress update
        if i < len(starting_urls) - 1:
            print(f"  Waiting before next URL...")
            time.sleep(2)
    
    print(f"\n📊 Crawling Summary:")
    print(f"  URLs processed: {len(starting_urls)}")
    print(f"  Documents extracted: {len(all_documents)}")
    print(f"  Failed URLs: {len(failed_urls)}")
    
    if failed_urls:
        print(f"  Failed URLs: {', '.join(failed_urls)}")
    
    if not all_documents:
        print("⚠️ No documents were successfully crawled. Please check your URLs.")
        return

    # Enhanced document preprocessing and chunking
    def preprocess_content(content: str, source_url: str) -> str:
        """Clean and enhance content before chunking"""
        # Remove excessive whitespace
        content = re.sub(r'\s+', ' ', content)
        
        # Remove navigation elements and common noise
        noise_patterns = [
            r'Skip to main content',
            r'Navigation menu',
            r'©.*?\d{4}.*?',
            r'All rights reserved',
            r'Cookie policy',
            r'Privacy policy'
        ]
        
        for pattern in noise_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE)
        
        # Add source context
        domain = urlparse(source_url).netloc
        content = f"Source: {domain}\n\n{content}"
        
        return content.strip()
    
    def create_smart_chunking_strategy(content: str, source_url: str) -> List[str]:
        """Intelligent chunking based on content type and structure"""
        # Detect content type
        is_markdown = '.md' in source_url or any(marker in content for marker in ['##', '###', '```'])
        is_code_heavy = content.count('```') > 2 or content.count('def ') > 3
        
        if is_markdown:
            # Use markdown-aware splitter
            splitter = MarkdownTextSplitter(
                chunk_size=2000,
                chunk_overlap=200,
                length_function=len
            )
        elif is_code_heavy:
            # Smaller chunks for code-heavy content
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1500,
                chunk_overlap=150,
                separators=["\n\n", "\n", "```", "def ", "class ", " "],
                length_function=len
            )
        else:
            # General content
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=2500,
                chunk_overlap=250,
                separators=["\n\n", "\n", ". ", " "],
                length_function=len
            )
        
        return splitter.split_text(content)
    
    def generate_content_hash(content: str) -> str:
        """Generate hash for deduplication"""
        return hashlib.md5(content.encode()).hexdigest()
    
    # Content deduplication tracking
    processed_hashes = set()
    duplicate_count = 0

    # Enhanced document processing with better metadata and deduplication
    total_chunks = 0
    processed_docs = 0
    
    for doc_idx, doc in enumerate(all_documents):
        try:
            source_url = doc.metadata.get('source', 'unknown')
            print(f"Processing document {doc_idx + 1}/{len(all_documents)}: {source_url}")
            
            # Preprocess content
            cleaned_content = preprocess_content(doc.page_content, source_url)
            
            # Skip if content is too short or low quality
            if len(cleaned_content.strip()) < 100:
                print(f"  Skipping - content too short ({len(cleaned_content)} chars)")
                continue
            
            # Smart chunking
            text_chunks = create_smart_chunking_strategy(cleaned_content, source_url)
            
            chunk_count = 0
            for i, chunk_content in enumerate(text_chunks):
                # Skip empty or very short chunks
                if len(chunk_content.strip()) < 50:
                    continue
                
                # Check for duplicates
                content_hash = generate_content_hash(chunk_content)
                if content_hash in processed_hashes:
                    duplicate_count += 1
                    continue
                
                processed_hashes.add(content_hash)
                
                # Enhanced metadata
                chunk_metadata = {
                    "source": source_url,
                    "chunk_id": i,
                    "doc_index": doc_idx,
                    "total_chunks": len(text_chunks),
                    "chunk_size": len(chunk_content),
                    "processed_date": datetime.now().isoformat(),
                    "content_hash": content_hash,
                    "domain": urlparse(source_url).netloc
                }
                
                # Detect content type for better categorization
                if 'kubernetes' in chunk_content.lower() or 'kubectl' in chunk_content.lower():
                    chunk_metadata["category"] = "kubernetes"
                elif 'docker' in chunk_content.lower() or 'container' in chunk_content.lower():
                    chunk_metadata["category"] = "docker"
                elif any(lang in chunk_content.lower() for lang in ['python', 'javascript', 'go', 'java']):
                    chunk_metadata["category"] = "programming"
                else:
                    chunk_metadata["category"] = "general"
                
                try:
                    # Generate embeddings
                    embedding = embedding_function([chunk_content])[0]
                    
                    # Generate unique document ID
                    doc_id = f"doc_{doc_idx}_chunk_{i}_{content_hash[:8]}"
                    
                    # Add to collection
                    collection.add(
                        documents=[chunk_content],
                        metadatas=[chunk_metadata],
                        ids=[doc_id],
                        embeddings=[embedding]
                    )
                    
                    chunk_count += 1
                    total_chunks += 1
                    
                except Exception as e:
                    print(f"  Error processing chunk {i}: {e}")
                    continue
            
            processed_docs += 1
            print(f"  Processed {chunk_count} chunks from document")
            
            # Rate limiting to avoid overloading
            if doc_idx % 5 == 0 and doc_idx > 0:
                print(f"  Processed {doc_idx + 1} documents, taking a short break...")
                time.sleep(2)
            else:
                time.sleep(0.5)
                
        except Exception as e:
            print(f"Error processing document {doc_idx}: {e}")
            continue
    
    # Final statistics
    print(f"\n✅ Processing complete!")
    print(f"  Documents processed: {processed_docs}/{len(all_documents)}")
    print(f"  Total chunks created: {total_chunks}")
    print(f"  Duplicates skipped: {duplicate_count}")
    print(f"  Final collection size: {collection.count()}")
    
    # Validate collection
    try:
        sample_query = collection.query(
            query_texts=["kubernetes"],
            n_results=1
        )
        if sample_query['documents']:
            print(f"✅ Vector store validation successful")
        else:
            print(f"⚠️ Warning: Vector store appears empty")
    except Exception as e:
        print(f"❌ Vector store validation failed: {e}")

    print(f"\n🎉 Web crawling and data loading complete!")
    print(f"Your enhanced RAG system is ready with {total_chunks} indexed chunks.")

if __name__ == "__main__":
    main()
