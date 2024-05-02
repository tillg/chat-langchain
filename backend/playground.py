from backend.chain import chat
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#print(answer_chain.invoke({"chat_history": None, "question": "What is the capital of france?"}))

print (chat(question="What is the capital of france?",
           llm_model="juhu",
           ))

