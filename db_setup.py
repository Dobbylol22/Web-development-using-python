from sqlalchemy import (Column,String,Integer,ForeignKey)
from sqlalchemy.orm import (relationship,backref)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base=declarative_base()

class Owner(Base):
	__tablename__='owners'
	id=Column(Integer,primary_key=True)
	name=Column(String(100),nullable=False)
	email=Column(String(200),nullable=False)
	password=Column(String(25),nullable=False)

class Item(Base):
	__tablename__='items'
	id=Column(Integer,primary_key=True)
	brandname=Column(String(100),nullable=False)
	image=Column(String(500),nullable=False)
	model=Column(String(100),nullable=False)
	cost=Column(Integer)
	description=Column(String(500),nullable=False)
	owner_id=Column(Integer,ForeignKey('owners.id'))
	owner=relationship(Owner,backref='items')
engine=create_engine('sqlite:///mydb.db')
Base.metadata.create_all(engine)
