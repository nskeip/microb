#-*- coding: UTF-8 -*-
from sqlalchemy import create_engine, Column
from sqlalchemy.orm import scoped_session, backref, relation
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.types import String, Text, Integer, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import ForeignKey
import settings

engine = create_engine(settings.DATABASE_URI, convert_unicode=True)
db_session = scoped_session(scoped_session(sessionmaker(autocommit=False,
                                                        autoflush=False,
                                                        bind=engine)))

Model = declarative_base(name='Model')

Model.query = db_session.query_property()

def init_db():
    Model.metadata.create_all(bind=engine)

class Post(Model):
    __tablename__ = 'posts'
    id = Column('id', Integer, primary_key=True)
    title = Column(String(70))
    date = Column(DateTime)
    text = Column(Text)
    published = Column(Boolean)

