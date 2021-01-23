from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String


Base = declarative_base()

class ProjectExpenses(Base):
    __tablename__ = "expenses"

    expense_id = Column(Integer, primary_key=True)
    expense_type = Column(String(15))
    project_id = Column(Integer)
    expense_date = Column(String(10))
    expense_amount = Column(Float)

engine = create_engine("postgres://postgres:PsHyPnfnFOIe4ex0@104.154.193.253:5432/projects")

Base.metadata.create_all(engine)