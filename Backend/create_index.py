from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from  utils import doctotext,textspliter



text=doctotext("""E:\Document-bot\Brance Hiring Task (July 2023)-20230706T120642Z-001\Brance Hiring Task (July 2023)\KnowledgeDocument(pan_card_services).txt""")
split_texts = textspliter(text,1000,100,'\n')


embeddings = HuggingFaceEmbeddings()
db = FAISS.from_texts(split_texts, embeddings)
FAISS.save_local(db, folder_path='')



