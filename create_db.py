from sqlalchemy import create_engine
from models import Base

def create_database():
    engine = create_engine('sqlite:///cooking_assistant.db')
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    create_database() 