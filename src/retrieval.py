import faiss
import numpy as np
from langchain_ollama import OllamaEmbeddings
from preprocess import load_documents, process_documents

def create_embeddings(processed_docs):
    if not processed_docs:
        print("ไม่มีข้อมูลเอกสารสำหรับสร้าง embeddings")
        return None, None

    embedding_model = OllamaEmbeddings(model="nomic-embed-text")
    texts = [doc['content'] for doc in processed_docs]
    
    embeddings = embedding_model.embed_documents(texts)
    embeddings = np.array(embeddings).astype("float32")

    return embeddings, processed_docs  # เก็บ metadata

def create_faiss_index(embeddings):
    if embeddings is None:
        print("ไม่สามารถสร้าง FAISS index ได้เนื่องจากไม่มี embeddings")
        return None

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    print(f"สร้าง FAISS index สำเร็จ: {index.ntotal} รายการ")
    return index

def build_index():
    docs = load_documents('data')
    processed_docs = process_documents(docs)
    embeddings, metadata = create_embeddings(processed_docs)

    if embeddings is None:
        return None, None

    index = create_faiss_index(embeddings)
    return index, metadata

if __name__ == '__main__':
    idx, meta = build_index()