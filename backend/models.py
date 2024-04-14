# -*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey,Table
import config

engine = create_engine(config.DB_URL, echo=True)

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


t_user_server = Table('t_user_server', Base.metadata,
    Column('u_id', Integer, ForeignKey('t_user.id')),
    Column('s_id', Integer, ForeignKey('t_server.id'))
)

class User(Base):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), nullable=False)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    email = Column(String(75), nullable=True)
    password = Column(String(128), nullable=False)
    is_super=Column(Boolean,default=False,nullable=False)
    servers=relationship('Server',secondary=t_user_server)

    def __repr__(self):
        return "<User('%s')>" % (self.username)

class Server(Base):
    
    __tablename__ ='t_server'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    host = Column(String(30), nullable=False)
    port = Column(Integer, nullable=False)
    username = Column(String(75), nullable=False)
    secret = Column(String(128), nullable=False)
    remark = Column(String(256), nullable=True)
    group_id=Column(Integer,ForeignKey('t_group.id'))
    group = relationship("Group")

    def __repr__(self):
        return "<Server('%s')>" % (self.username)

class Group(Base):
    
    __tablename__ ='t_group'
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    servers=relationship("Server")

    def __repr__(self):
        return "<Group('%s')>" % (self.username)


users_table = User.__table__

metadata = Base.metadata


def create_all():
    metadata.create_all(engine)