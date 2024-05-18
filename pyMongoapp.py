from datetime import datetime
import pprint
from pymongo import MongoClient

# Conectar ao servidor MongoDB usando a string de conexão do MongoDB Atlas
client = MongoClient("mongodb+srv://mrlodin1:220197lady@cluster0.o8ecf4s.mongodb.net/")

# Definir o documento a ser inserido
post = {
    "author": "Mike",
    "text": "My first mongodb application based on python",
    "tags": ["Mongo", "Python3", "pymongo"],
    "date": datetime.utcnow()  # Uso correto de datetime.utcnow()
}

# Conectar ao banco de dados (substitua 'test' pelo nome do seu banco de dados, se necessário)
db = client.test

# Inserir o documento na coleção 'posts'
posts = db.posts
post_id = posts.insert_one(post).inserted_id  # Correção: `inserted_id` em vez de `insert_id`
print(post_id)

# print(db.posts.find_one())

# bulk inserts
new_posts = [
    {
        "author": "Mike",
        "text": "another post",
        "tags": ["bulk", "post", "insert"],
        "date": datetime.utcnow()
    },      
    {
        "author": "João",
        "text": "Post from João. New post available",
        "title": "Mongo is fun",
        "date": datetime(2009, 11, 10, 10, 45)
    }
]

result = posts.insert_many(new_posts)
print(result.inserted_ids)  

print("\nRecuperação final")

pprint.pprint(db.posts.find_one())