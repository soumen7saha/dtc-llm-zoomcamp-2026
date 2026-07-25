import sys

from dotenv import load_dotenv
from openai import OpenAI

from starter import documents, index
from metrics import RAGTraced

def create_assistant():
    load_dotenv()

    documents = load_faq_data()

    return RAGTraced(
        index=index,
        llm_client=OpenAI()
    )


if __name__ == "__main__":
    assistant = create_assistant()

    query = "How do I join the course?"
    if len(sys.argv) > 1:
        query = sys.argv[1]

    answer = assistant.rag(query)
    print(answer)

    save_conversation(assistant.last_call, query, "llm-zoomcamp")
