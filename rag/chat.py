from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from rag.models import Models
from rag.vector_store import vector_store_obj
from langchain_core.runnables  import RunnableLambda

model = Models()
llm = model.model_google
vector_store = vector_store_obj()


def query(prompt, query, document_id):
    qa_chain = (
            {
                "context": vector_store.as_retriever(search_kwargs={"filter": {"document_id": document_id}}),
                "question": RunnablePassthrough(),
            }
            # | RunnableLambda(debug_retriever)  # Debug step to print chunks
            | prompt
            | llm
            | StrOutputParser()
    )
    response = qa_chain.invoke(query)
    return response


def debug_retriever(inputs):

    retrieved_docs = inputs["context"]
    print("\n🔍 Retrieved Chunks:")
    for i, doc in enumerate(retrieved_docs):
        print(f"Chunk {i + 1}: {doc.page_content}\n")
    return inputs