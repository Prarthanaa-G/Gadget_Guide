
from firebase_admin import firestore
from langchain.schema import HumanMessage, AIMessage

def get_db():
    """Returns the Firestore client."""
    return firestore.client()

def save_chat_history(user_uid: str, product_name: str, chat_history):
    """Saves the chat history for a specific product to Firestore."""
    db = get_db()
    # Use a subcollection for products under each user's chat document
    doc_ref = db.collection("chats").document(user_uid).collection("products").document(product_name)
    
    history_to_save = []
    for msg in chat_history:
        if isinstance(msg, HumanMessage):
            history_to_save.append({"type": "human", "content": msg.content})
        elif isinstance(msg, AIMessage):
            history_to_save.append({"type": "ai", "content": msg.content})

    doc_ref.set({"messages": history_to_save})

def load_chat_history(user_uid: str, product_name: str): 
    """Loads chat history for a specific product from Firestore."""
    db = get_db()
    doc_ref = db.collection("chats").document(user_uid).collection("products").document(product_name)
    doc = doc_ref.get()
    
    if doc.exists:
        history_from_db = doc.to_dict().get("messages", [])
        reconstructed_history = []
        for msg_data in history_from_db:
            if msg_data["type"] == "human":
                reconstructed_history.append(HumanMessage(content=msg_data["content"]))
            elif msg_data["type"] == "ai":
                reconstructed_history.append(AIMessage(content=msg_data["content"]))
        return reconstructed_history
    else:
        return []
    
def delete_chat_history(user_uid: str, product_name: str):
    """Deletes the chat history for a specific product from Firestore."""
    try:
        db = get_db()
        doc_ref = db.collection("chats").document(user_uid).collection("products").document(product_name)
        doc_ref.delete()
        return True
    except Exception as e:
        print(f"Error deleting chat history: {e}")
        return False
