import openai
from openai import OpenAI
import pandas as pd
import os

if os.path.isfile('config.py'):
    from config import OPENAI_API_KEY
else:
    from config_render import OPENAI_API_KEY

embedding_model_name = 'text-embedding-3-small'

### Write function to create vector database
def embed_all_courses(df, embedding_model_name = embedding_model_name, output_file_name='all_courses_with_embeddings.csv'):
    ### Step 1: Combine the title and description of each course
    df['title_and_desc'] = df['Title'] + ': ' + df['Description']
    ### Step 2: Apply the function to the entire dataset
    df['embedding'] = df['title_and_desc'].apply(get_embedding, embedding_model_name)
    ### Step 3: Save the dataset with embeddings
    df.to_csv(output_file_name, index=False)
    return df


### Write function to get embedding of one course
def get_embedding(text, model=embedding_model_name):
    client = OpenAI(
                api_key= OPENAI_API_KEY
            )
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding