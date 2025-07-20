import streamlit as st
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from utils.vector_utils import load_vectorstore, get_available_products, delete_product_from_store
import os

def admin_ui():
    st.title("📥 Admin Panel")
    
    # --- 1. UPLOAD A NEW MANUAL ---
    st.subheader("Upload a New Product Manual")
    
    # Use a form to handle the upload and prevent the loop
    with st.form("upload_form", clear_on_submit=True):
        pdf = st.file_uploader("Upload a manual (PDF)", type="pdf")
        submitted = st.form_submit_button("Upload and Process")

    if submitted and pdf is not None:
        with st.spinner("Processing PDF..."):
            try:
                manuals_dir = os.path.join("vectorstore", "manuals")
                os.makedirs(manuals_dir, exist_ok=True)
                file_path = os.path.join(manuals_dir, pdf.name)
                with open(file_path, "wb") as f:
                    f.write(pdf.getvalue())
                
                reader = PdfReader(pdf)
                text = "".join(page.extract_text() or "" for page in reader.pages)
                
                if not text.strip():
                    st.warning("The uploaded PDF seems to be empty or contains only images. No text could be extracted.")
                else:
                    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
                    chunks = text_splitter.split_text(text)
                    
                    product_name = pdf.name.replace(".pdf", "").replace("_", " ").title()
                    docs = [Document(page_content=chunk, metadata={"product": product_name, "source_file": pdf.name}) for chunk in chunks]

                    vector_store = load_vectorstore()
                    vector_store.add_documents(docs)
                    vector_store.save_local("vectorstore/faiss_index")
                    
                    load_vectorstore.clear()
                    get_available_products.clear()
                    
                    st.success(f"Successfully uploaded '{product_name}'.")

            except PdfReadError:
                st.error("The uploaded file is not a valid PDF.")
            except Exception as e:
                st.error("An unexpected error occurred during upload.")
                st.exception(e)

    st.write("---")

    # --- 2. REMOVE AN EXISTING MANUAL ---
    st.subheader("Remove an Existing Product Manual")
    # This section remains the same and is correct
    available_products = get_available_products(load_vectorstore())
    
    if not available_products:
        st.info("No manuals are currently in the knowledge base.")
    else:
        product_to_delete = st.selectbox(
            "Select a manual to remove permanently",
            options=available_products,
            index=None,
            placeholder="Choose a manual..."
        )

        if product_to_delete:
            if st.button(f"Delete '{product_to_delete}' Manual", type="primary"):
                with st.spinner(f"Deleting all chunks for '{product_to_delete}'..."):
                    success = delete_product_from_store(product_to_delete)
                    if success:
                        st.success(f"Successfully removed all data for '{product_to_delete}'.")
                        st.rerun()





# import streamlit as st
# from PyPDF2 import PdfReader
# from PyPDF2.errors import PdfReadError  # 1. Import the specific error type
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.schema import Document
# from utils.vector_utils import load_vectorstore, get_available_products,delete_product_from_store
# import os

# def admin_ui():
#     st.title("📥 Admin Panel – Upload Product Manuals")
#     st.write("Upload a new PDF manual to add it to the chatbot's knowledge base.")
    
#     pdf = st.file_uploader("Upload a product manual (PDF)", type="pdf", key="admin_pdf_uploader")

#     if pdf:
#         with st.spinner("Processing PDF and updating knowledge base..."):
#             try:
#                 # Save the uploaded file first
#                 manuals_dir = os.path.join("vectorstore", "manuals")
#                 os.makedirs(manuals_dir, exist_ok=True)
#                 file_path = os.path.join(manuals_dir, pdf.name)
                
#                 with open(file_path, "wb") as f:
#                     f.write(pdf.getvalue())
                
#                 # Try to read the PDF
#                 reader = PdfReader(pdf)
#                 text = ""
#                 for page in reader.pages:
#                     text += page.extract_text() or ""

#                 # --- The rest of your processing logic ---
#                 text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#                 chunks = text_splitter.split_text(text)
                
#                 product_name = pdf.name.replace(".pdf", "").replace("_", " ").title()
#                 docs = [Document(page_content=chunk, metadata={"product": product_name, "source_file": pdf.name}) for chunk in chunks]

#                 vector_store = load_vectorstore()
#                 vector_store.add_documents(docs)
#                 vector_store.save_local("vectorstore/faiss_index")
                
#                 load_vectorstore.clear()
#                 get_available_products.clear()
                
#                 st.success(f"Successfully uploaded '{product_name}' and updated the chatbot.")
                

#             # 2. Add a specific except block for PDF errors
#             except PdfReadError:
#                 st.error("The uploaded file is not a valid PDF. Please check the file and try again.")
            
#             # 3. Keep the general exception for any other errors
#             except Exception as e:
#                 st.error("An unexpected error occurred during the upload process.")
#                 st.exception(e)
                
                
#     st.write("---")


#     st.subheader("Remove an Existing Product Manual")
    
#     available_products = get_available_products(load_vectorstore())
    
#     if not available_products:
#         st.info("No manuals are currently in the knowledge base.")
#     else:
#         product_to_delete = st.selectbox(
#             "Select a manual to remove permanently",
#             options=available_products,
#             index=None,
#             placeholder="Choose a manual..."
#         )

#         if product_to_delete:
#             if st.button(f"Delete '{product_to_delete}' Manual", type="primary"):
#                 with st.spinner(f"Deleting all chunks for '{product_to_delete}'..."):
#                     # Call the new utility function to handle the deletion logic
#                     success = delete_product_from_store(product_to_delete)
#                     if success:
#                         st.success(f"Successfully removed all data for '{product_to_delete}'.")
#                         st.rerun()



