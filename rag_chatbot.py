import openai
from openai import OpenAI
from config import OPENAI_API_KEY
from heapq import nlargest
import numpy as np

client = OpenAI(
  api_key= OPENAI_API_KEY
)
import rag_utils
import pandas as pd
import requests
import json

embedding_model_name = "text-embedding-3-small"
file_name = 'all_courses_with_embeddings.csv'

df = pd.read_csv(file_name)

def embedding_cosine_similarity(query, document, query_embedding=None):
    # First, embed the query
    if query_embedding is None:
        query_embedding = rag_utils.get_embedding(query)
    # Next, get the document embedding from the dataset
    document_embedding = document['embedding']
    # Next, compute the cosine similarity between the query and the document
    return np.dot(query_embedding, document_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(document_embedding))

def return_options(query, corpus, similarity_function=embedding_cosine_similarity):
    similarities = []
    options_returned = []
    query_embedding = rag_utils.get_embedding(query)
    for idx, doc in corpus.iterrows():
        similarity = similarity_function(query, doc, query_embedding)
        similarities.append(similarity)
    indices = list(range(len(similarities)))
    for i in nlargest(5, indices, key = lambda x : similarities[x]): # get top 5 similarities
        options_returned.append(
            corpus['title_and_desc'][i]
        ) # return the document at the index of similarity i
    return options_returned

def get_response(user_input):
    relevant_documents = return_options(user_input, df)
    list_of_relevant_documents = [f"{i+1}. {doc}" for i, doc in enumerate(relevant_documents)]
    relevant_documents_text = "\n".join(list_of_relevant_documents)
    return relevant_documents_text