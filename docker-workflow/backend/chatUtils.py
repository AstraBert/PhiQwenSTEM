# IMPORTS 

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from ragUtils import SemanticCache, NeuralSearcher, qdrant_client, dense_encoder, sparse_encoder, reranlking_encoder, Reranker

h = open("/run/secrets/huggingface_api_token")
content2 = h.read()
h.close()
HF_TOKEN = content2.replace("\n","")

llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3.5-mini-instruct",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    huggingfacehub_api_token=HF_TOKEN,
)

chat_model = ChatHuggingFace(llm=llm)

# GLOBALS

semantic_cache = SemanticCache(qdrant_client, text_encoder=reranlking_encoder, collection_name="semantic_cache_med")
searcher = NeuralSearcher("med_cot_qa", qdrant_client, dense_encoder, sparse_encoder)
reranker = Reranker(reranlking_encoder)

def reply(prompt: str):
    print("Searching cache", flush=True)
    sc = semantic_cache.search_cache(prompt)
    print("Cache searched", flush=True)
    if sc:
        return sc
    else:
        vdb_messages = [
            SystemMessage(content="You are a skilled medical professional whose task is to represent the query from the user as a poignant, comprehensive and well-structured medical question that will be used to retrieve information from a vector database. Your question must be based solely on the content provided by the user in their prompt: you are not allowed to add additional information. You should only output the question to perform the search within the database."),
            HumanMessage(
                content=prompt
            ),
        ]
        res = chat_model.invoke(vdb_messages)
        print("Generated VDB question", flush=True)
        print(res)
        vector_search_question = res.content
        payloads, responses = searcher.search_text(vector_search_question)
        print("Got relevant documents", flush=True)
        response = reranker.reranking(responses, vector_search_question)
        reasoning = [payload["context"] for payload in payloads if payload["response"]==response][0]
        print("Reranked documents", flush=True)
        medical_messages = [
            SystemMessage(content="You are a skilled medical professional whose task is to reason about the questions you are given by the user, assess them critically and finally produce an answer. You have one very important instruction: if your reasoning is contradictory, vague, or does not seem to lead to a unique and viable answer to the user query, please reply: 'I don't know the answer to this question' and invite the user to turn to a human medical professional."),
            HumanMessage(
                content=prompt
            ),
            AIMessage(
                content=f"Reasoning about the user's prompt:\n\n{reasoning}"
            ),
            AIMessage(
                content=f"Potential response to the user's prompt:\n\n{reasoning}"
            ),
            HumanMessage(
                content="Starting from the previous steps that you took toward the solution, produce a final, well-structured reasoning workflow that should explain me what you think about the problem. Once you are done with the reasoning workflow, please produce a final, poignant response to my initial question. Do not mention the previous step, just assume that I do not know anything about them and you are explaining me everything from scratch."
            )
        ]
        res1 = chat_model.invoke(medical_messages)
        print("Generated medical reasoning and response", flush=True)
        final_response = f"""{res1.content}\n\n## DISCLAIMER: PhiCare is an AI Assistant!\n\n**No AI Assistant will ever perform as good as a human medical professional: please, if you need medical care and/or help, seek it from qualified professionals**."""
        semantic_cache.upload_to_cache(prompt, final_response)
        print("Final response ready", flush=True)
        return final_response




