import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint

def get_conversation_chain(vectorstore):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")

    llm_endpoint = HuggingFaceEndpoint(
        repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",
        task="text-generation",
        huggingfacehub_api_token=hf_token,
        temperature=0.5,
        max_new_tokens=300
    )

    chat_model = ChatHuggingFace(llm=llm_endpoint)
    return ConversationalRetrievalChain.from_llm(
        llm=chat_model,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
