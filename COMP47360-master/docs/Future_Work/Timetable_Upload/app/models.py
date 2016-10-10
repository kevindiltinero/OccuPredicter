# coding: utf-8
from sqlalchemy import Column, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Clas(Base):
    __tablename__ = 'class'

    room_id = Column(ForeignKey(u'room.room_id'), primary_key=True, nullable=False, server_default=text("''"))
    timestamp = Column(Integer, primary_key=True, nullable=False, server_default=text("'0'"))
    code = Column(ForeignKey(u'module.code'), primary_key=True, nullable=False, index=True, server_default=text("''"))

    module = relationship(u'Module')
    room = relationship(u'Room')


class Module(Base):
    __tablename__ = 'module'

    code = Column(String(45), primary_key=True)
    total_students = Column(Integer)


class Room(Base):
    __tablename__ = 'room'

    room_id = Column(String(45), primary_key=True)
    capacity = Column(Integer)
    type = Column(String(45))
    building = Column(String(45))


class Survey(Base):
    __tablename__ = 'survey'

    survey_id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey(u'room.room_id'), index=True)
    timestamp = Column(Integer)
    occupied = Column(Integer)
    occupancy = Column(Integer)

    room = relationship(u'Room')


class Wifi(Base):
    __tablename__ = 'wifi'

    record_id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey(u'room.room_id'), index=True)
    timestamp = Column(Integer)
    authenticated = Column(Integer)
    associated = Column(Integer)

    room = relationship(u'Room')
