import streamlit as st
import os
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from utils.prompt_utils import get_custom_prompt
from utils.vector_utils import load_vectorstore, get_available_products
from langchain.schema import HumanMessage, AIMessage
from utils.firestore_utils import save_chat_history, load_chat_history, delete_chat_history

load_dotenv()

def get_conversation_chain(retriever, prompt,memory):
    llm = ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        model="mistralai/mistral-7b-instruct:free",
        temperature=0.2,
        max_tokens=512,
    )


    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt}
    )
    
def handle_userinput(user_question):
    with st.spinner("Thinking..."):
        response = st.session_state.conversation({'question': user_question})
        st.session_state.chat_history = response['chat_history']

        save_chat_history(st.session_state.user["uid"],st.session_state.selected_product, st.session_state.chat_history)
     
    st.rerun()   


def chatbot_ui():
    st.header("Product Support Chatbot  🛍️🛒")
    st.markdown("How can I help you troubleshoot your product?  🔧⚙️")
    

    vectorstore = load_vectorstore()
    available_products = get_available_products(vectorstore)
    user_question = st.chat_input("What do you want to know?")
    if "selected_product" not in st.session_state:
        st.session_state.selected_product = available_products[0] if available_products else None

    # Initialize chat history for the default/current product
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = load_chat_history(
            st.session_state.user["uid"],
            st.session_state.selected_product
        )

    # Initialize conversation chain
    if "conversation" not in st.session_state:
        memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
        memory.chat_memory.messages = st.session_state.chat_history
        prompt_template = get_custom_prompt()
        retriever = vectorstore.as_retriever(search_kwargs={"filter": {"product": st.session_state.selected_product}})
        st.session_state.conversation = get_conversation_chain(retriever, prompt_template, memory)



    # Display the chat history
    chat_html = '<div class="chat-container">'
    for msg in st.session_state.chat_history:
        if isinstance(msg, HumanMessage):
            chat_html += user_template.replace("{{MSG}}", msg.content)
        elif isinstance(msg, AIMessage):
            chat_html += bot_template.replace("{{MSG}}", msg.content)
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    
    # --- Sidebar for product selection ---
    with st.sidebar:
        st.subheader("Select Product Manual")
        def on_product_change():
            
            st.session_state.chat_history = load_chat_history(
                st.session_state.user["uid"],
                st.session_state.selected_product # The key from selectbox holds the new value
            )
            # Re-create the memory and conversation chain with the new history and retriever
            memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
            memory.chat_memory.messages = st.session_state.chat_history
            
            retriever = vectorstore.as_retriever(search_kwargs={"filter": {"product": st.session_state.selected_product}})
            prompt_template = get_custom_prompt()
            st.session_state.conversation = get_conversation_chain(retriever, prompt_template, memory)
        

        st.selectbox(
            "Product",
            options=available_products,
            key="selected_product",
            on_change=on_product_change # Use a callback to handle changes
        )
        
        st.write("---")

        #  Add the Clear History Button ---
        if st.button("🗑️ Clear Chat History"):
            with st.spinner("Clearing history..."):
                # Get current user and product context
                user_id = st.session_state.user["uid"]
                product = st.session_state.selected_product
                
                # 1. Delete the history from Firestore
                delete_chat_history(user_id, product)
                
                # 2. Clear the history in the current session state
                st.session_state.chat_history = []
                
                # 3. Re-initialize the conversation chain with an empty memory
                memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
                retriever = vectorstore.as_retriever(search_kwargs={"filter": {"product": product}})
                prompt_template = get_custom_prompt()
                st.session_state.conversation = get_conversation_chain(retriever, prompt_template, memory)
                st.rerun()
        
   
    if user_question:
        handle_userinput(user_question)




