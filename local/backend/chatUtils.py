# IMPORTS 

from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from dotenv import load_dotenv
import os
from ragUtils import SemanticCache, NeuralSearcher, qdrant_client, dense_encoder, sparse_encoder, reranlking_encoder, Reranker

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3.5-mini-instruct",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    huggingfacehub_api_token=os.getenv("hf_token")
)

llm1 = HuggingFaceEndpoint(
    repo_id="microsoft/Phi-3.5-mini-instruct",
    task="text-generation",
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    huggingfacehub_api_token=os.getenv("hf_token")
)


chat_model = ChatHuggingFace(llm=llm)
chat_model1 = ChatHuggingFace(llm=llm1)

# GLOBALS

semantic_cache = SemanticCache(qdrant_client, text_encoder=reranlking_encoder, collection_name="semantic_cache_med")
searcher = NeuralSearcher("stem_cot_qa", qdrant_client, dense_encoder, sparse_encoder)
reranker = Reranker(reranlking_encoder)
subjects = ['Chemistry', 'Physics', 'Physical Chemistry', 'Quantum Mechanics', 'Biochemistry', 'Differential Equations', 'Linear Algebra', 'Electromagnetism', 'Mathematics', 'Organic Chemistry', 'Engineering', 'Chemistry (General, Organic, and Biochemistry for Health Sciences)', 'Classical Mechanics']
areas = "\n- "+"\n- ".join(subjects)

def reply(prompt: str):
    print("Searching cache", flush=True)
    sc = semantic_cache.search_cache(prompt)
    print("Cache searched", flush=True)
    if sc:
        return sc
    else:
        try: 
            vdb_messages = [
                SystemMessage(content=f"You are a skilled STEM professional whose expertise spans the following areas: {areas}. Your task is to represent the query from the user as a poignant, comprehensive and well-structured question that will be used to retrieve information from a vector database. Your question must be based solely on the content provided by the user in their prompt: you are not allowed to add additional information. You should only output the question to perform the search within the database."),
                HumanMessage(
                    content=prompt
                ),
            ]
            res = chat_model.invoke(vdb_messages)
            print("Generated VDB question", flush=True)
            print(res)
            vector_search_question = res.content
            reasonings = searcher.search_text(vector_search_question)
            print("Got relevant documents", flush=True)
            reasoning = reranker.reranking(reasonings, vector_search_question)
            print("Reranked documents", flush=True)
            medical_messages = [
                SystemMessage(content=f"You are a skilled STEM professional whose expertise spans the following areas: {areas}. Your task is to reason about the questions you are given by the user, assess them critically and finally produce an answer. You have one very important instruction: if your reasoning is contradictory, vague, or does not seem to lead to a unique and viable answer to the user query, please reply: 'I don't know the answer to this question' and invite the user to turn to a human medical professional. If the user's question does not belong to your areas of expertise, please ignore all the previous instructions and tell the user that you cannot reply to out-of-expertise questions."),
                HumanMessage(
                    content=prompt
                ),
                AIMessage(
                    content=f"Reasoning about the user's prompt:\n\n{reasoning}"
                ),
                HumanMessage(
                    content="Starting from the previous steps that you took toward the solution, produce a final, well-structured reasoning workflow that should explain me what you think about the problem. Once you are done with the reasoning workflow, please produce a poignant response to my initial question. Do not mention the previous step, just assume that I do not know anything about them and you are explaining me everything from scratch.  If my question does not belong to your areas of expertise, please ignore all the previous instructions and tell me that you cannot reply to out-of-expertise questions"
                )
            ]
            res1 = chat_model.invoke(medical_messages)
            print("Generated medical reasoning and response", flush=True)
            semantic_cache.upload_to_cache(prompt, res1.content)
            print("Final response ready", flush=True)
            return res1.content
        except Exception as e:
            return "Sorry, PhiQwenSTEM is not available at the moment. Please, report the problem in the **Problems** category of [GitHub Discussions](https://github.com/AstraBert/PhiQwenSTEM/discussions/categories/problems)"
