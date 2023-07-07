import streamlit as st
import pandas as pd
import requests
API_URL = "http://127.0.0.1:8000/accuracycheck"


def query(payload):
    response = requests.post(API_URL,json=payload )
    print(response.json())
    return response.json()

df= pd.read_csv('annoteted_data.csv',sep="|")
que = list(df['Question'])
expected_ans = list(df['Answer']) 
dict1= dict(zip(que,expected_ans))






option = st.selectbox(
    'How would you like to be contacted?',
    (["-"] + list(df['Question'])))


if(option =='-'):

    st.write("select question from sample for quality check")
    
else:
    payload={
  "question": option,
  "expected_answer": dict1[option]
}
    
    output = query(payload)
    
    st.title('Accuracy Check')
    st.write(f"Question-: {output['Question']}")
    st.write(f"Expected Answer-: {output['Expected Answer']}")
    st.write(f"Generated Answer-: {output['Generated Answer']}")
    st.write(f"Similarity Score-: {output['Similarity Score:']}")
    