from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
import os
import datetime

Base = declarative_base()


def create_tables(engine):
    Base.metadata.create_all(engine)


def drop_tables(engine):
    Base.metadata.drop_all(engine)


def create_session(engine):
    return Session(bind=engine)

def _get_date():
    return datetime.datetime.now()    

class Heartbeat(Base):
    __tablename__ = 'HEARTBEAT'
    id = Column(Integer, primary_key=True)
    time =  Column(DateTime, default=_get_date)
    hostname = Column(String)    

class File(Base):
    __tablename__ = 'FILES'
    id = Column(Integer, primary_key=True)
    name = Column(String)    