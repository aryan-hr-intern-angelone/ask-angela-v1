# Ask Angela v1

Ask Angela is a Retrieval-Augmented Generation (RAG) chatbot integrated with Slack, designed to assist employees by answering queries related to internal HR policies (e.g., leave, benefits, reimbursements etc).

## Key Features

- Natural language interface on Slack for seamless access.
- RAG pipeline:
    - Retriever pulls relevant chunks from HR policy documents stored in a vector database (FAISS).
    - Reranker to rank the the most appropriate matchs in the fetched chunks.
    - Generator (LLM) answers based on those ranked chunks, ensuring grounded responses.
- Metadata filters to search for the most relevant policies in context to user query.
- Semantic Router to detect user intent and execute the respective actions accordingly.
## Document Sources

- The policies are stored in a text format in an S3 bucket from where they are fetched and conveted into embeddings and stored in the vector store.
## Tech Stack

- **LangChain** & **LangSmith** - for RAG implementation, Model Chaining and Logging the LLM model responses.
- **FAISS** - Local Vector Store for storing chunks of data and similarity search.
- **Slack Bolt** - For integrating the chatbot on Slack using the Slack Socket Mode.
- **Embedding Models** - Google Embedding Models (Cloud API) and BAAI/bge-small-en (locally)
- **Reranking Model** - Cohere Reranking Models for rearranging chunks before passing them to LLM.
- **LLM Models** - Google Gemini Models