from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = (String, nullable=False)
    password = (String, nullable=False)

def __repr__(self):
    return f"<User(id='{self.id}', username='{self.username}')>"

DATABASE_URL = 'postgresql+psycopg2://postgres:Dimalera0805@localhost:5432/mydatabase'
engine = create_engine(DATABASE_URL)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

new_user = User(username = 'testuser', password = 'testpassword')
session.add(new_user)
session.commit()

all_users = session.query(User).all()
for user in all_users:
    print(user)
