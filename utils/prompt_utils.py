from langchain.prompts import PromptTemplate

def get_custom_prompt():
    return PromptTemplate(
        input_variables=["context", "question"],
        template="""
        You are an intelligent AI assistant. Based on the following product manual context, answer the question in a single line and be polite.

        Product Manual Context:
        {context}

        Question:
        {question}

        Helpful Answer:"""
    )
