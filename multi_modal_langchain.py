import cassio
import os 
import clip_embedding
from langchain.vectorstores import Cassandra
import pandas as pd 
import json 

token = os.environ['ASTRA_DB_APPLICATION_TOKEN']
database_id = os.environ['ASTRA_DB_DATABASE_ID']
keyspace=os.environ.get('ASTRA_DB_KEYSPACE')

cassio.init(token=token, database_id=database_id)
vstore = Cassandra(
    table_name='flickr_langchain',
    embedding=clip_embedding.ClipEmbeddings(),       
    session= None,
    keyspace= None 
)

df = pd.read_csv('flickr/captions.txt')
docs = [ json.dumps({"caption":f'{row["caption"]}',"image":f'{os.getcwd()}/flickr/Images/{row["image"]}'}) for index,row in df.head(10).iterrows()]
vstore.add_texts(docs)

query = '{"caption":"black dog"}'
results = vstore.search(query, search_type='similarity', k=2)
print(results)

query = f"{'image':'{os.getcwd()}/flickr/Images/1001773457_577c3a7d70.jpg'}"
results = vstore.search(query, search_type='similarity', k=2)
print(results)