import argparse
import chromadb
import css # this file is local
import gradio as gr
import ollama
import os
import time
import re
import numpy as np
from functools import lru_cache
from typing import List, Dict, Tuple
from datetime import datetime
import json

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
    # Parse the arguments
    args = parser.parse_args()

    # Load the config from the specified file
    config = load_config(args.config)

    if config:
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

    # Enhanced query preprocessing
    def preprocess_query(query: str) -> str:
        """Enhance query with context and reformulation for better retrieval"""
        # Remove unnecessary words and normalize
        query = re.sub(r'\b(how to|what is|tell me about|explain)\b', '', query, flags=re.IGNORECASE)
        query = re.sub(r'\s+', ' ', query).strip()

        # Add technical context keywords for better matching
        technical_keywords = {
            'kubernetes': ['k8s', 'kubectl', 'pod', 'deployment', 'service'],
            'docker': ['container', 'image', 'dockerfile'],
            'programming': ['code', 'function', 'method', 'class'],
            'error': ['troubleshoot', 'debug', 'fix', 'issue']
        }

        enhanced_query = query
        for domain, keywords in technical_keywords.items():
            if any(keyword in query.lower() for keyword in keywords):
                enhanced_query += f" {domain}"

        return enhanced_query

    # Enhanced caching mechanism for embeddings
    @lru_cache(maxsize=500)  # Increased cache size
    def get_embedding_from_prompt(prompt: str) -> List[float]:
        """Get embedding with enhanced caching and error handling"""
        try:
            response = ollama.embeddings(model=embeddingmodel, prompt=prompt)
            return response["embedding"]
        except Exception as e:
            print(f"Error generating embedding for prompt: {prompt[:50]}... Error: {e}")
            # Return a zero vector as fallback
            return [0.0] * 768  # Assuming 768-dimensional embeddings

    # Advanced retrieval with reranking
    def query_vector_store(prompt: str, n_results: int = None) -> List[Dict]:
        """Enhanced retrieval with semantic reranking and context filtering"""
        if n_results is None:
            n_results = min(vectorresults * 2, 10)  # Retrieve more candidates for reranking

        # Preprocess query
        enhanced_prompt = preprocess_query(prompt)

        # Get embedding with caching
        query_embedding = get_embedding_from_prompt(enhanced_prompt)

        # Retrieve candidates
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=['documents', 'metadatas', 'distances']
        )

        if not results['documents'] or not results['documents'][0]:
            return [{"content": "No relevant information found.", "source": "system", "score": 0.0}]

        # Calculate semantic similarity scores
        documents = results['documents'][0]
        metadatas = results['metadatas'][0] if results['metadatas'] else [{}] * len(documents)
        distances = results['distances'][0] if results['distances'] else [1.0] * len(documents)

        # Enhanced scoring with multiple factors
        scored_results = []
        for i, (doc, metadata, distance) in enumerate(zip(documents, metadatas, distances)):
            # Convert distance to similarity score (lower distance = higher similarity)
            similarity_score = max(0, 1 - distance)

            # Content relevance scoring
            content_score = calculate_content_relevance(prompt.lower(), doc.lower())

            # Recency bonus for newer content (if timestamp available)
            recency_score = 1.0  # Default

            # Combined score
            final_score = (similarity_score * 0.6 + content_score * 0.3 + recency_score * 0.1)

            scored_results.append({
                "content": doc,
                "source": metadata.get('source', 'unknown'),
                "score": final_score,
                "chunk_id": metadata.get('chunk_id', i)
            })

        # Sort by score and return top results
        scored_results.sort(key=lambda x: x['score'], reverse=True)
        return scored_results[:vectorresults]

    def calculate_content_relevance(query: str, content: str) -> float:
        """Calculate content relevance based on keyword overlap and semantic indicators"""
        query_words = set(re.findall(r'\w+', query.lower()))
        content_words = set(re.findall(r'\w+', content.lower()))

        if not query_words:
            return 0.0

        # Exact word overlap
        overlap = len(query_words.intersection(content_words))
        overlap_score = overlap / len(query_words)

        # Bonus for exact phrase matches
        phrase_bonus = 0.2 if query in content.lower() else 0.0

        # Technical term bonus
        technical_terms = ['kubernetes', 'docker', 'api', 'deployment', 'service', 'pod']
        tech_bonus = 0.1 if any(term in content.lower() for term in technical_terms if term in query) else 0.0

        return min(1.0, overlap_score + phrase_bonus + tech_bonus)

    # Function to generate a response from the LLM
    def generate_response(prompt):
        response = ollama.generate(model=mainmodel, prompt=prompt)
        return response['response']

    # Set LLM temperature
    def set_temperature(new_temperature):
        global llm
        llm = lambda prompt: ollama.generate(model=mainmodel, prompt=prompt)['response']

    # Enhanced template with better context utilization
    def create_dynamic_prompt(question: str, context_items: List[Dict], temperature: float) -> str:
        """Create a dynamic prompt based on context quality and question type"""

        # Analyze question type
        question_lower = question.lower()
        is_how_to = any(phrase in question_lower for phrase in ['how to', 'how do', 'how can'])
        is_what_is = any(phrase in question_lower for phrase in ['what is', 'what are', 'define'])
        is_troubleshoot = any(phrase in question_lower for phrase in ['error', 'issue', 'problem', 'not working', 'fail'])

        # Build context with relevance scores
        context_parts = []
        high_confidence_sources = []

        for item in context_items:
            score = item.get('score', 0)
            source = item.get('source', 'unknown')
            content = item.get('content', '')

            if score > 0.7:
                high_confidence_sources.append(source)
                context_parts.append(f"[HIGH RELEVANCE - {source}]: {content}")
            elif score > 0.4:
                context_parts.append(f"[RELEVANT - {source}]: {content}")
            else:
                context_parts.append(f"[REFERENCE - {source}]: {content}")

        context_text = "\n\n".join(context_parts)

        # Dynamic instruction based on question type and context quality
        if is_troubleshoot:
            instruction = """Analyze the context to provide a troubleshooting solution. If the context contains relevant error information or solutions, use them as your primary source. Provide step-by-step guidance when possible."""
        elif is_how_to:
            instruction = """Provide a clear, step-by-step explanation based on the context. Focus on practical implementation details."""
        elif is_what_is:
            instruction = """Provide a comprehensive definition or explanation using the context. Include relevant technical details and examples."""
        else:
            instruction = """Answer the question using the provided context. Be specific and cite relevant information from the sources."""

        # Adjust response style based on temperature
        style_guide = """
Response Guidelines:
- Be precise and technical when appropriate
- Use information from HIGH RELEVANCE sources primarily
- If context is insufficient, clearly state limitations
- Provide actionable information when possible
- Keep responses focused and well-structured"""

        if high_confidence_sources:
            source_note = f"\nPrimary sources: {', '.join(set(high_confidence_sources))}"
        else:
            source_note = "\nNote: Limited relevant context available, supplementing with general knowledge."

        template = f"""{instruction}

Context Information:
{context_text}
{style_guide}
{source_note}

Question: {question}

Answer:"""

        return template

    # Enhanced answer generation with conversation history and error handling
    def get_answer(question: str, temperature: float, conversation_history: str = "") -> str:
        """Generate enhanced answers with context-aware prompting"""
        try:
            set_temperature(temperature)

            # Add conversation context to query if available
            enhanced_question = question
            if conversation_history:
                # Extract recent context (last 200 chars) to maintain conversation flow
                recent_context = conversation_history[-200:] if len(conversation_history) > 200 else conversation_history
                enhanced_question = f"Context from conversation: {recent_context}\n\nCurrent question: {question}"

            # Retrieve and rank context
            context_items = query_vector_store(enhanced_question)

            # Log retrieval quality for debugging
            avg_score = sum(item.get('score', 0) for item in context_items) / len(context_items) if context_items else 0
            print(f"Retrieved {len(context_items)} contexts with avg relevance: {avg_score:.2f}")

            # Create dynamic prompt
            combined_prompt = create_dynamic_prompt(question, context_items, temperature)

            # Generate response
            response = generate_response(combined_prompt)

            # Post-process response
            processed_response = post_process_response(response, context_items)

            return processed_response

        except Exception as e:
            print(f"Error generating answer: {e}")
            return f"I encountered an issue processing your question. Please try rephrasing or contact support. Error: {str(e)}"

    def post_process_response(response: str, context_items: List[Dict]) -> str:
        """Post-process the response for better formatting and source attribution"""
        # Add source references if high-confidence sources were used
        high_conf_sources = [item['source'] for item in context_items if item.get('score', 0) > 0.7]

        if high_conf_sources and len(set(high_conf_sources)) <= 3:
            source_list = ', '.join(set(high_conf_sources))
            response += f"\n\n*Sources: {source_list}*"

        # Clean up formatting
        response = re.sub(r'\n{3,}', '\n\n', response)  # Remove excessive newlines
        response = response.strip()

        return response

    # Enhanced Gradio interface function with conversation state
    conversation_state = {"history": ""}

    def get_answer_with_temp(question: str, temperature: float, history: str = "") -> Tuple[str, str]:
        """Enhanced interface function with conversation memory"""
        if not question.strip():
            return "Please enter a question.", history

        # Generate answer
        answer = get_answer(question, temperature, history)

        # Update conversation history
        timestamp = datetime.now().strftime("%H:%M")
        new_history_entry = f"[{timestamp}] Q: {question}\nA: {answer}\n\n"
        updated_history = history + new_history_entry

        # Keep history manageable (last 2000 chars)
        if len(updated_history) > 2000:
            # Keep last 1500 chars to maintain context
            updated_history = "..." + updated_history[-1500:]

        return answer, updated_history

    # Enhanced Gradio interface with better UX
    with gr.Blocks(theme=theme, css=css.custom_css, title="Enhanced RAG Chatbot") as frontend:
        gr.Markdown(
            """# 🤖 Enhanced RAG Chatbot

Ask questions about your knowledge base. The system will find relevant information and provide comprehensive answers.

**Tips for better results:**
            - Be specific in your questions
            - Use technical terms when appropriate
            - Ask follow-up questions for clarification
            """
        )

        with gr.Row():
            with gr.Column(scale=3):
                question_input = gr.Textbox(
                    lines=3,
                    placeholder="Ask a question about Kubernetes, Docker, programming, or any topic in your knowledge base...",
                    label="Your Question",
                    show_label=True
                )

                with gr.Row():
                    temperature_slider = gr.Slider(
                        minimum=0.1,
                        maximum=1.0,
                        step=0.1,
                        value=0.3,
                        label="Response Creativity (0.1=focused, 1.0=creative)"
                    )
                    submit_btn = gr.Button("🔍 Ask", variant="primary")

            with gr.Column(scale=1):
                gr.Markdown(
                    """### Quick Examples
                    - "How to list failing pods in Kubernetes?"
                    - "What is a Docker container?"
                    - "Troubleshoot deployment issues"
                    - "Explain service mesh concepts"
                    """
                )

        with gr.Row():
            answer_output = gr.Textbox(
                label="Answer",
                lines=8,
                max_lines=50,
                placeholder="Your answer will appear here. Processing may take a few moments...",
                show_copy_button=True
            )

        # Conversation history (hidden state)
        history_state = gr.State(value="")

        with gr.Accordion("💬 Conversation History", open=False):
            history_display = gr.Textbox(
                label="Recent Conversation",
                lines=10,
                max_lines=20,
                interactive=False,
                placeholder="Your conversation history will appear here..."
            )

        # Event handlers
        def process_question(question, temperature, history):
            answer, updated_history = get_answer_with_temp(question, temperature, history)
            return answer, updated_history, updated_history, ""

        submit_btn.click(
            fn=process_question,
            inputs=[question_input, temperature_slider, history_state],
            outputs=[answer_output, history_state, history_display, question_input]
        )

        question_input.submit(
            fn=process_question,
            inputs=[question_input, temperature_slider, history_state],
            outputs=[answer_output, history_state, history_display, question_input]
        )

        # Clear conversation button
        with gr.Row():
            clear_btn = gr.Button("🗑️ Clear Conversation", variant="secondary")
            clear_btn.click(
                fn=lambda: ("", "", ""),
                outputs=[history_state, history_display, question_input]
            )

    # Performance monitoring
    def log_performance_metrics():
        """Log system performance metrics"""
        cache_info = get_embedding_from_prompt.cache_info()
        #print(f"Embedding cache stats - Hits: {cache_info.hits}, Misses: {cache_info.misses}, Hit rate: {cache_info.hits/(cache_info.hits+cache_info.misses)*100:.1f}%")

    # Launch enhanced Gradio interface with better configuration
    print(f"🚀 Starting Enhanced RAG Chatbot...")
    print(f"📊 Configuration: {vectorresults} results, {embeddingmodel} embeddings, {mainmodel} generation")
    log_performance_metrics()

    frontend.launch(
        server_name=servername,
        server_port=serverport,
        inbrowser=True,
        share=False,
        show_error=True,
        quiet=False
    )

    # Cleanup on exit
    print("Final performance metrics:")
    log_performance_metrics()


    # Startup validation
    def validate_system():
        """Validate system components on startup"""
        try:
            # Test embedding model
            test_embedding = get_embedding_from_prompt("test")
            print(f"✅ Embedding model working - dimension: {len(test_embedding)}")

            # Test main model
            test_response = generate_response("Hello")
            print(f"✅ Main model working - response length: {len(test_response)}")

            # Test vector store
            collection_count = collection.count()
            print(f"✅ Vector store ready - {collection_count} documents indexed")

            return True
        except Exception as e:
            print(f"❌ System validation failed: {e}")
            return False

    # Run startup validation
    if not validate_system():
        print("⚠️ System validation failed - some features may not work correctly")

if __name__ == "__main__":
    main()
