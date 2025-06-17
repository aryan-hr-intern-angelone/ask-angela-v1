import os
from langchain.schema import Document
from langchain.vectorstores.utils import DistanceStrategy
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
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

def get_splitter_by_token_count(token_count):
    seprators = ["\n\n", "\n", ".", " "]
    if token_count < 500:
        return RecursiveCharacterTextSplitter(chunk_size=token_count, chunk_overlap=0)
    elif token_count < 1000:
        return RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=50, separators=seprators)
    elif token_count < 2000:
        return RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100, separators=seprators)
    elif token_count < 4000:
        return RecursiveCharacterTextSplitter(chunk_size=768, chunk_overlap=128, separators=seprators)
    elif token_count < 7000:
        return RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=128, separators=seprators)
    elif token_count < 12000:
        return RecursiveCharacterTextSplitter(chunk_size=384, chunk_overlap=128, separators=seprators)
    else:
        return RecursiveCharacterTextSplitter(chunk_size=256, chunk_overlap=128, separators=seprators)
    
def get_text_chunks(text):
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size=1024,
    #     chunk_overlap=128,
    #     separators=["\n\n", "\n", ".", " "]
    # )
    text_splitter = get_splitter_by_token_count(len(text)/4)
    
    chunks = text_splitter.split_text(text)
    return chunks

def create_vector_store_full_docs(text, file_id, file_name):
    index_dir = env.faiss.INDEX_DIR
    full_text_path = env.faiss.FULL_TEXT_PATH
    
    os.makedirs(index_dir, exist_ok=True)
    index_file = os.path.join(index_dir, full_text_path)
    
    embeddings = GoogleGenerativeAIEmbeddings(model=env.models.EMBEDDING_MODEL)
    document = [Document(
        page_content=text,
        metadata={
            "source_id": file_id,
            "source": file_name
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
    
def create_vector_store(chunks, file_id, file_name):
    try:
        index_dir = env.faiss.INDEX_DIR
        chunks_path = env.faiss.TEXT_CHUNK_PATH
        
        os.makedirs(index_dir, exist_ok=True)
        index_file = os.path.join(index_dir, chunks_path)

        embeddings = GoogleGenerativeAIEmbeddings(model=env.models.EMBEDDING_MODEL)
        documents = [Document(page_content=chunk, metadata={"source_id": file_id, "source": file_name}) for chunk in chunks]

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
