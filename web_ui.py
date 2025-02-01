import ollama
import chromadb
import os
import gradio as gr
import css
import time
from functools import lru_cache

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
vectorresults = int(config.get("vectorresults", 5))
servername = config.get("servername","127.0.0.1")
serverport = int(config.get("serverport", 8080))
theme = config.get("theme","Soft")

# Initialize the ChromaDB client
client = chromadb.PersistentClient(path=vectorstore)
collection = client.get_collection("document_collection")

# Function to query and retrieve from the vector store
def query_vector_store(prompt, n_results=vectorresults):  # Reduced n_results to 5 for faster retrieval
    response = ollama.embeddings(model=embeddingmodel, prompt=prompt)
    query_embedding = response["embedding"]

    # Querying vector database
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)
    if results['metadatas']:
        sources = [metadata['source'] for metadata in results['metadatas'][0]]
    else:
        sources = ["No result found."]
    print("Using sources")
    print(sources)
    return sources

# Function to generate a response from the LLM
def generate_response(prompt):
    response = ollama.generate(model=mainmodel, prompt=prompt)
    return response['response']

# Set LLM temperature
def set_temperature(new_temperature):
    global llm
    llm = lambda prompt: ollama.generate(model=mainmodel, prompt=prompt)['response']

# Template for the prompt
template = """Use the following pieces of context to answer the question.
If pieces of context do not contain the answer use your internal knowledge.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Use three sentences maximum for the answer. Keep the answer as concise as possible.
Always say "thanks for asking!" at the end of the answer.
{context}
Question: {question}
Answer:"""

# Function to get the answer
def get_answer(question, temperature):
    set_temperature(temperature)  # Adjust the model's temperature
    retrieved_sources = query_vector_store(question, n_results=5)  # Optimized for fewer results
    context = ", ".join(retrieved_sources)
    combined_prompt = template.format(context=context, question=question)
    response = generate_response(combined_prompt)
    return response

# Gradio interface function
def get_answer_with_temp(question, temperature):
    return get_answer(question, temperature)

# Set up Gradio interface
frontend = gr.Interface(
    fn=get_answer_with_temp,
    inputs=[
        gr.Textbox(lines=2, placeholder="Type your question here", label="Question"),
        gr.Slider(minimum=0, maximum=10, step=1, label="Creativity Level (Temperature)")
    ],
    outputs=gr.Textbox(label="Answer", lines=5, max_lines=200, placeholder="Due to CPU inference, please allow time to process"),
    title="Locally Hosted LLM ChatBot",
    theme=theme,
    description="Enter a question to get an answer. Adjust the model's temperature to control randomness.",
    css=css.custom_css
)

# Launch Gradio interface
frontend.launch(
    server_name=servername,
    server_port=serverport,
    inbrowser=True,
    share=False
)

# Caching mechanism for embedding to prevent redundant calls to Ollama
@lru_cache(maxsize=100)
def get_embedding_from_prompt(prompt):
    response = ollama.embeddings(model=embeddingmodel, prompt=prompt)
    return response["embedding"]
