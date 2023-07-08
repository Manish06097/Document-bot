import PyPDF2
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain import OpenAI
from langchain.chains import RetrievalQA 
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from dotenv import load_dotenv
load_dotenv()
apikey = os.getenv('APIKEY')



def doctotext(filename):
    with open(filename,'r') as file:
        text = file.read()
    print(text)
       
        
    return text


def textspliter(text,chunksize,chunkoverlap,separator):
    text_splitter = CharacterTextSplitter(chunk_size=chunksize, chunk_overlap=chunkoverlap,separator=separator)
    texts = text_splitter.split_text(text)   
    return texts


def process_message(user_message: str,name) -> str:
    qa = RetrievalQA.from_chain_type(llm=OpenAI(model='text-davinci-003',openai_api_key=apikey), chain_type='stuff', retriever=name.as_retriever())
    ans = qa.run("if the user question not in the provided content or que is incomplete than ask user to give more information or ask relevent que to the document and  make the output more representable like in bullet points and also output should be precise and relevent and short -: "+user_message)
    
    return f"{ans}"

def accuracy_message(user_message: str,name) -> str:
    qa = RetrievalQA.from_chain_type(llm=OpenAI(model='text-davinci-003',openai_api_key=apikey), chain_type='stuff', retriever=name.as_retriever())
    ans = qa.run("output should be precise and relevent and short -: "+user_message)
    
    return f"{ans}"

def accuracycheck(model,name,que,expected):
    
    df=pd.read_csv('annoteted_data.csv',sep="|")
    sample_questions = que
    expected_answers = expected
    generated_answers = ''
    generated_answers=accuracy_message(que,name)
    # Encode the sentences into vectors
    expected_answer_vec = model.encode(expected_answers).squeeze()
    generated_answer_vec = model.encode(generated_answers).squeeze()

    # Calculate cosine similarity between expected and generated answer vectors
    similarity_score = cosine_similarity([expected_answer_vec], [generated_answer_vec])[0][0] 
    return       {
              "Question":sample_questions,
              "Expected Answer":  expected_answers,
              'Generated Answer': generated_answers,
              'Similarity Score:': similarity_score.item(),
                            
            }
