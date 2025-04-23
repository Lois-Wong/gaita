import openai
from openai import OpenAI
from config_render import OPENAI_API_KEY
from heapq import nlargest
import numpy as np

client = OpenAI(
  api_key= OPENAI_API_KEY
)
import rag_utils
import pandas as pd
import json

embedding_model_name = "text-embedding-3-small"
file_name = 'all_courses_with_embeddings.csv'

df = pd.read_csv(file_name)
df['embedding'] = df['embedding'].apply(lambda x: np.array(json.loads(x)))

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
            corpus.iloc[i]
        ) # return the document at the index of similarity i
    return options_returned

def get_response(user_input):
    relevant_documents = return_options(user_input, df)
    # take out just the title and description
    relevant_documents_title_desc = [doc['title_and_desc'] for doc in relevant_documents]
    # take out just the links
    relevant_documents_links = [doc['Link'] for doc in relevant_documents]
    # create a string of enumerated documents
    list_of_relevant_documents = [f"{i+1}. {doc}" for i, doc in enumerate(relevant_documents_title_desc)]
    relevant_documents_text = "\n".join(list_of_relevant_documents)
    # create string of enumerated links
    list_of_relevant_documents_links = [f"{i+1}. {link}" for i, link in enumerate(relevant_documents_links)]
    relevant_documents_links_text = "\n".join(list_of_relevant_documents_links)
    response = get_response_from_openai(user_input, relevant_documents_text, relevant_documents_links_text)
    return response

def get_response_from_openai(user_input, relevant_documents_text, relevant_documents_links_text):
    prompt = f"""
    You are trying to help this user find an online Computer Science course
    From my database of CS courses, here were some recommendations based on the user input: {relevant_documents_text}
    The user input is: '{user_input}'
    Compile a recommendation to the user based on the recommended Computer Science courses and the user input, 
    returning the top 3 courses with their links embedded in the title: {relevant_documents_links_text} from the database.
    The courses are ranked in order of best fit for the user, and please provide a brief explanation for why each course is a fit.

    Please return the course recommendations in a clean, readable format with proper spacing and line breaks.
    Please provide the courses in the following format:

    1. **[Course Name]** [1-3 sentence summary focused on relevance to user's goal. Highlight key relevant topics and unique benefits.]  

    2. **[Course Name]** [1-3 sentence summary focused on relevance to user's goal]
    
    3. **[Course Name]** [1-3 sentence summary focused on relevance to user's goal]


    At the end of your response, the user a relevant follow-up question that helps assess whether 
    the user is truly ready to take the recommended courses. Identify 
    any prerequisite knowledge the user may need to learn in order to succeed in the recommended course. 

    """
    try:
        # Make the request to the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are a bot that makes recommendations for Computer Science courses. Instead of markdown syntax, you return text formatted in HTML syntax, with tags such as <b> for boldface, <a> for links, etc."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
        )
        # Process the response
        chatgpt_response = response.choices[0].message.content
        return chatgpt_response
    except openai.OpenAIError as e:
        return f"OpenAI API error occurred: {e}"
    except Exception as e:
        return f"An error occurred: {e}"
    
