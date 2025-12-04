from dotenv import load_dotenv

from pprint import pprint


load_dotenv()

from retailchatbot.chains.text_to_sql import db_chain
from retailchatbot.chains.generation_chain import rag_gen_chain
from retailchatbot.rag_ingestion.vector_db_ingestion import retriever

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def test_text_to_sql_chain()->None:
    question = "what's the price of 3 bed , 2 bath and 0.11 acre_lot flat in Massachusetts"
    res = db_chain.invoke(question)
    pprint(res)

def test_rag_chain() -> None:
    question = "tell me what does it mean by 'Champions Take The Luck out of The Game' in the context of real estate investment"
    docs = retriever.invoke(question)
    pprint("\n [INFO] Documents: \n")
    pprint(format_docs(docs))
    generation = rag_gen_chain.invoke({"context": format_docs(docs), "question": question})
    pprint("\n [INFO] Generation: \n")
    pprint(generation)