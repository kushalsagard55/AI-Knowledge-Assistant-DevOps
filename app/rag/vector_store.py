from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.embeddings import embedding_model

VECTOR_DB_PATH = "vector_store"


def build_vector_store(document_text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    chunks = splitter.split_text(document_text)

    if not chunks:
        raise ValueError("No text chunks were created from the uploaded document.")

    Path(VECTOR_DB_PATH).mkdir(exist_ok=True)

    db = FAISS.from_texts(
        chunks,
        embedding_model,
    )

    db.save_local(VECTOR_DB_PATH)

    return len(chunks)

def search_documents(question: str):

    db = FAISS.load_local(
        VECTOR_DB_PATH,
        embedding_model,
        allow_dangerous_deserialization=True,
    )

    docs = db.similarity_search(
        question,
        k=3,
    )

    print("\n" + "=" * 70)
    print("QUESTION:", question)
    print("DOCUMENTS FOUND:", len(docs))

    for i, doc in enumerate(docs):
        print(f"\n----- DOCUMENT {i+1} -----")
        print(doc.page_content[:500])

    print("=" * 70 + "\n")

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    return context