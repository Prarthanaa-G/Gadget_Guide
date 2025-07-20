import streamlit as st
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document

def build_vectorstore_from_manuals(path="vectorstore/faiss_index"):
    """
    Builds the FAISS index from all PDFs in the 'manuals' directory.
    This function runs only if the index doesn't already exist.
    """
    st.info("No existing vector store found. Building a new one from manuals...")
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    manuals_dir = os.path.join(PROJECT_ROOT, "vectorstore", "manuals")

    all_docs = []
    
    # Check if the manuals directory exists and has PDFs
    if not os.path.exists(manuals_dir) or not any(fname.endswith('.pdf') for fname in os.listdir(manuals_dir)):
        st.warning("The 'manuals' directory is empty or missing. The chatbot will not have any knowledge.")
        return None

    # Process each PDF
    for filename in os.listdir(manuals_dir):
        if filename.endswith(".pdf"):
            file_path = os.path.join(manuals_dir, filename)
            reader = PdfReader(file_path)
            text = "".join(page.extract_text() or "" for page in reader.pages)
            
            text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = text_splitter.split_text(text)
            
            product_name = filename.replace(".pdf", "").replace("_", " ").title()
            docs = [Document(page_content=chunk, metadata={"product": product_name, "source_file": filename}) for chunk in chunks]
            all_docs.extend(docs)

    # Create and save the FAISS index
    embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-small-v2")
    vector_store = FAISS.from_documents(all_docs, embeddings)
    vector_store.save_local(path)
    st.success("New vector store built successfully!")
    return vector_store

@st.cache_resource
def load_vectorstore(path="vectorstore/faiss_index"):
    """
    Loads the FAISS vector store. If it doesn't exist, it builds it first.
    """
    if not os.path.exists(path):
        # Build the store if it's not found
        return build_vectorstore_from_manuals(path)
    else:
        # Load the existing store
        embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-small-v2")
        return FAISS.load_local(path, embeddings, allow_dangerous_deserialization=True)


@st.cache_data
def get_available_products(_vectorstore):
    """Extract list of unique product names from FAISS metadata"""
    if not _vectorstore:
        return []
    metadata_list = [doc.metadata for doc in _vectorstore.docstore._dict.values()]
    return sorted(list(set(meta["product"] for meta in metadata_list if "product" in meta)))


def delete_product_from_store(product_name: str, path="vectorstore/faiss_index"):
    """
    Finds and deletes all data for a specific product from the vector store
    and also deletes the original source PDF file.
    """
    try:
        vector_store = load_vectorstore(path)
        ids_to_delete = [
            doc_id for doc_id, doc in vector_store.docstore._dict.items()
            if doc.metadata.get("product") == product_name
        ]

        if not ids_to_delete:
            st.warning(f"No documents found for product '{product_name}'.")
            return False

      
        source_file_name = vector_store.docstore._dict[ids_to_delete[0]].metadata.get("source_file")
        if source_file_name:
            file_path = os.path.join("vectorstore", "manuals", source_file_name)
            try:
                os.remove(file_path)
            except FileNotFoundError:

                pass


        vector_store.delete(ids_to_delete)
        vector_store.save_local(path)
        load_vectorstore.clear()
        get_available_products.clear()
        
        return True
    except Exception as e:
        st.error(f"An error occurred while deleting the product: {e}")
        return False