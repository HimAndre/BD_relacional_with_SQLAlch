from multiprocessing import connection
from sqlalchemy.orm import declarative_base, relationship, Session
from sqlalchemy import Column, create_engine, func, inspect, String, ForeignKey, Integer, select

Base = declarative_base()

class User(Base):
    __tablename__ = "user_account"
    # atributos
    id = Column(Integer, primary_key=True)
    name = Column(String) 
    fullname = Column(String)

    address = relationship(
        "Address", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"User(id={self.id}, name={self.name}, fullname={self.fullname})"
    
class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True)
    email_address = Column(String(30), nullable=False)
    user_id = Column(Integer, ForeignKey("user_account.id"), nullable=False)

    user = relationship("User", back_populates="address")

    def __repr__(self):
        return f"Address(id={self.id}, email_address={self.email_address})"

print(User.__tablename__)
print(Address.__tablename__)

# Conexão com banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

# Investiga o esquema do banco de dados
inspetor_engine = inspect(engine)
print(inspetor_engine.has_table("user_account"))

print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

with Session(engine) as session:
    juliana = User(
        name='juliana',
        fullname="juliana Mascarenhas",
        address=[Address(email_address="julianam@email.com")]
    )

    sandy = User(
        name="sandy",
        fullname="Sandy Cardoso",
        address=[Address(email_address="sandy@email.br"),
                 Address(email_address="sandy@email.org")]
    )

    patrick = User(name="patrick", fullname= "Patrick Cardoso")

    # Enviando para o BD (persistência de dados)
    session.add_all([juliana, sandy, patrick])

    session.commit()

stmt = select(User).where(User.name.in_(['juliana', 'sandy']))
print('recuperando usuarios a partir de condicao de filtragem')
for user in session.scalars(stmt):
    print(user)

stmt_address = select(Address).where(Address.id.in_([2]))
print('recuperando os endereçoes de email de sandy')
for address in session.scalars(stmt_address):
    print(address)

order_stmt = select(User).order_by(User.fullname.desc())
print("\nRecuperando info de maneira ordenada")
for result in session.scalars(order_stmt):
    print(result)

stmt_join = select(User.fullname, Address.email_address).join_from(Address, User)
print("\n")
for result in session.scalars(stmt_join):
    print(result)

connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("\nexcutando statement a partir da connection")
for result in results:
    print(result)

stmt_count = (select(func.count("*")).select_from(User))
print("Total de instancias em User")
for result in session.scalars(stmt_count):
    print(result)
