from fastapi import FastAPI
from pydantic import BaseModel
from langchain.vectorstores import FAISS
from utils import process_message,accuracycheck
from langchain.embeddings import HuggingFaceEmbeddings
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer

# using Sentence Transformer from ber  for similarity check
model = SentenceTransformer('bert-base-nli-mean-tokens')


#using Faiss For creating vector space or 
name = FAISS.load_local(embeddings=HuggingFaceEmbeddings(),folder_path='')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str
    
    
class accuracy(BaseModel):
    question: str
    expected_answer:str

# This endpoint is for chatbot to retrive the answer from the document 
@app.post("/chat")
async def chat_endpoint(message: Message):
    user_message = message.message
    reply = process_message(user_message,name)
    return {"reply": reply}

# this endpoint for the checking the accuracy with sample data
@app.post("/accuracycheck")
def check(accuracy: accuracy):
    user_question = accuracy.question
    user_expected_ans = accuracy.expected_answer

    
    
    return accuracycheck(model,name,user_question,user_expected_ans)
    
    

    