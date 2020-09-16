from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base #permite tener acceso al object relational maper que nos permite trabajar con objetos de python en lugar de querys de sql directamente
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///newspaper.db')

Session = sessionmaker(bind = engine)

Base = declarative_base() #de aqui extenderan todos nuestros modelos
