from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Resource(Base):
    """Модель ресурсів"""
    __tablename__ = 'resources'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    spawn_chance = Column(Float, default=0.3)
    min_amount = Column(Integer, default=1)
    max_amount = Column(Integer, default=3)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Enemy(Base):
    """Модель ворогів"""
    __tablename__ = 'enemies'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    hp = Column(Integer, nullable=False)
    attack = Column(Integer, nullable=False)
    defense = Column(Integer, nullable=False)
    exp = Column(Integer, nullable=False)
    gold = Column(Integer, nullable=False)
    spawn_chance = Column(Float, default=0.3)
    track_description = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Player(Base):
    """Модель гравця"""
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    hp = Column(Integer, default=100)
    max_hp = Column(Integer, default=100)
    attack = Column(Integer, default=10)
    defense = Column(Integer, default=5)
    exp = Column(Integer, default=0)
    level = Column(Integer, default=1)
    gold = Column(Integer, default=0)
    location = Column(String, default="start")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Зв'язки
    inventory = relationship("Inventory", back_populates="player")
    tracks = relationship("Track", back_populates="player")

class Inventory(Base):
    """Модель інвентаря"""
    __tablename__ = 'inventory'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    resource_id = Column(Integer, ForeignKey('resources.id'))
    amount = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Зв'язки
    player = relationship("Player", back_populates="inventory")
    resource = relationship("Resource")

class Track(Base):
    """Модель слідів"""
    __tablename__ = 'tracks'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey('players.id'))
    location = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Зв'язки
    player = relationship("Player", back_populates="tracks")

# Функція для створення всіх таблиць
def create_tables(engine):
    Base.metadata.create_all(engine)

# Функція для отримання сесії
def get_session(engine):
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    return Session() 