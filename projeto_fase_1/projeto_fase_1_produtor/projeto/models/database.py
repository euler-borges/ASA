# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# import os

# # DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql://postgres:banco123@localhost:5433/pedidos"
# SQLALCHEMY_DATABASE_URL = DATABASE_URL

# engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
