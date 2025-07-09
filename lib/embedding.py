import os
from langchain.schema import Document
from langchain.vectorstores.utils import DistanceStrategy
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from dataclasses import dataclass
from config.env import env

# def get_pdf_text(pdf_stream):
#     try:
#         stream = fitz.open(stream=pdf_stream, filetype="pdf")
#         md_text = pymupdf4llm.to_markdown(stream)
#         return md_text
#     except Exception as e:    
#         print(e)

# def get_pdf_text(pdf_stream):
#     text = ""
#     # print("reading pdf stream")
#     # pdf_reader = PdfReader(pdf_stream)
#     # for page in pdf_reader.pages:
#     #     extracted = page.extract_text()
#     #     if extracted:
#     #         text += extracted
#     try:
#         stream = fitz.open(stream=pdf_stream, filetype="pdf")
#         md_text = pymupdf4llm.to_markdown(stream)
#         return md_text
#     except Exception as e:
#         print(e)
#     # return text

@dataclass
class ChunkingStrategy():
    chunk_size: str
    chunk_overlap: str
    
def get_chunking_configuration(token_count: float):
    if token_count < 500:
        return ChunkingStrategy(token_count, 0)
    elif token_count < 1000:
        return ChunkingStrategy(300, 50)
    elif token_count < 2000:
        return ChunkingStrategy(512, 100)
    elif token_count < 4000:
        return ChunkingStrategy(768, 128)
    elif token_count < 7000:
        return ChunkingStrategy(512, 128)
    elif token_count < 12000:
        return ChunkingStrategy(384, 128)
    else:
        return ChunkingStrategy(236, 128)
    
def get_text_chunks(text):
    approx_tokens = len(text)/4
    config = get_chunking_configuration(approx_tokens)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.chunk_size,
        chunk_overlap=config.chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )
    
    chunks = text_splitter.split_text(text)
    return chunks, config, approx_tokens

def create_vector_store_full_docs(text: str, file_id: str, file_name: str, approx_tokens: float):
    index_dir = env.faiss.INDEX_DIR
    full_text_path = env.faiss.FULL_TEXT_PATH
    
    os.makedirs(index_dir, exist_ok=True)
    index_file = os.path.join(index_dir, full_text_path)
    
    embeddings = GoogleGenerativeAIEmbeddings(model=env.models.EMBEDDING_MODEL)
    document = [Document(
        page_content=text,
        metadata={
            "source_id": file_id,
            "source": file_name,
            "total_tokens": approx_tokens
        }
    )]
    
    new_store = FAISS.from_documents(document, embeddings)
    
    if os.path.exists(index_file):
        existing_text_store = FAISS.load_local(index_file, embeddings, allow_dangerous_deserialization=True)
        existing_text_store.merge_from(new_store)
        existing_text_store.save_local(index_file)
    else:
        print("Index for full text store not found, Creating one...")
        new_store.save_local(index_file)
    
def create_vector_store(
    chunks: str, 
    file_id: str, 
    file_name: str, 
    approx_tokens: float,
    config: ChunkingStrategy
):
    try:
        index_dir = env.faiss.INDEX_DIR
        chunks_path = env.faiss.TEXT_CHUNK_PATH
        
        os.makedirs(index_dir, exist_ok=True)
        index_file = os.path.join(index_dir, chunks_path)

        embeddings = GoogleGenerativeAIEmbeddings(model=env.models.EMBEDDING_MODEL)
        
        # TODO: Add the chunk word count, and remove the chunk_size, chunk_overlap and total_token
        documents = [Document(
            page_content=chunk, 
            metadata={
                "source_id": file_id, 
                "source": file_name, 
                "total_token": approx_tokens
            }) 
        for chunk in chunks]

        new_store = FAISS.from_documents(
            documents,
            embeddings,
            distance_strategy=DistanceStrategy.COSINE
        )

        if os.path.exists(index_file):
            existing_chunks_store = FAISS.load_local(index_file, embeddings, allow_dangerous_deserialization=True)
            existing_chunks_store.merge_from(new_store)
            existing_chunks_store.save_local(index_file)
        else:
            print("Index file for chunks store not found, Creating one...")
            new_store.save_local(index_file)
    except Exception as e:
        print(e)
        
def delete_vector_store(file_name: str):
    try:
        index_dir = env.faiss.INDEX_DIR
        chunks_path = env.faiss.TEXT_CHUNK_PATH
        full_text_path = env.faiss.FULL_TEXT_PATH
        
        embeddings = GoogleGenerativeAIEmbeddings(model=env.models.EMBEDDING_MODEL)
        chunks_store = FAISS.load_local(f"{index_dir}/{chunks_path}", embeddings=embeddings, allow_dangerous_deserialization=True)
        full_text_store = FAISS.load_local(f"{index_dir}/{full_text_path}", embeddings=embeddings, allow_dangerous_deserialization=True)
        
        chunks_doc_ids = [key for key, val in chunks_store.docstore._dict.items() if val.metadata.get("source") == file_name]
        full_text_doc_ids = [key for key, val in full_text_path.docstore._dict.items() if val.metadata.get("source") == file_name]
        
        chunks_store.delete(ids=chunks_doc_ids)
        full_text_store.delete(ids=full_text_doc_ids)
        
        chunks_store.save_local(f"{index_dir}/{chunks_path}")
        full_text_store.save_local(f"{index_dir}/{full_text_store}")
        
        print(f"Succesfully deleted {file_name} from both chunks store and full text store")
    except Exception as e:
        print(f"Error while removing {file_name} from the vector store")
        raise e