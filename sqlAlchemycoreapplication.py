from importlib import metadata
from sqlalchemy import Column, ForeignKey, select, text
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Nullable
import sqlalchemy

engine = create_engine("sqlite:///:memory")

metadata_obj = MetaData()
user = Table(
   "user",
   metadata_obj,
   Column("user_id", Integer, primary_key=True),
   Column("user_name", String(40), nullable=False),
   Column("email_address", String(60)),
   Column("nickname", String(50), nullable=False),
)

user_prefs = Table(
    "user_prefs", metadata_obj,
    Column("pref_id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey("user.user_id"), nullable=False),
    Column("pref_name", String(40), nullable=False),
    Column("pref_value", String(100)),
)

print("\nInfo da tabela financial_info")
print(user_prefs.primary_key)
print(user_prefs.constraints)


for table in metadata_obj.sorted_tables:
    print(table)

metadata_obj.create_all(engine)


metadata_bd_obj = MetaData()
financial_info = Table(
    "financial_info",
    metadata_bd_obj,
    Column("Id", Integer, primary_key=True),
    Column("value", String(100), nullable=False),   
)

print("\nInfo da tabela financial_info")
print(financial_info.primary_key)
print(financial_info.constraints)

with engine.connect() as connection:

    sql = text("SELECT * FROM user")
    result = connection.execute(sql)
    for row in result:
        print(row)

with engine.connect() as connection:
    sql_insert = text("INSERT INTO user (user_id, user_name, email_address, nickname) VALUES (:user_id, :user_name, :email_address, :nickname)")
    params = {
        'user_id': 1,
        'user_name': 'juliana',
        'email_address': 'email@email.com',
        'nickname': 'ju'
    }
    connection.execute(sql_insert, params)

    # Seleção e impressão dos dados inseridos
    sql = text("SELECT * FROM user")
    result = connection.execute(sql)
    for row in result:
        print(row)
