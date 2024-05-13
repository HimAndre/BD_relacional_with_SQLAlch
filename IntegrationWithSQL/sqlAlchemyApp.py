from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy import Column, create_engine, inspect
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String) 
    fullname = Column(String)

    address = relationship(
        "address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"
    


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="Address")

    def __repr__(self):
        return f"Address (id={self.id}, email_address={self.email_address})"


print(User.__tablename__)
print(Address.__tablename__)

#conexão com banco de dados

engine = create_engine("sqlite://")

#criando as classes como tabelas no banco de dados 
Base.metadata.create_all(engine)

#depreciado - será removido em futuro realease
#print (engine.table_name())


# investiga o esquema do banco de dados 

inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))

print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    juliana = User(
        name='juliana',
        fullname="juliana Mascarenhas",
        Address=[Address(email_address="julianam@email.com")]
    )

    sandy = User(
        name="sandy",
        fullname="Sandy Cardoso",
        address=[Address(email_address="sandy@email.br"),
                 Address(email_address="sandy@email.org")]
    )

    patrick = User(name="patrick", fullname= "Patrick Cardoso")

#enviando para o BD(persistencia de dados)
    session.add_all([juliana, sandy, patrick])

    session.commit()



