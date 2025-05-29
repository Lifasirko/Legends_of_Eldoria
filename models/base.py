from sqlalchemy import Column, Integer, String, JSON, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String)
    locale = Column(String, default='uk')
    created_at = Column(DateTime, server_default=func.now())
    last_seen = Column(DateTime, server_default=func.now(), onupdate=func.now())
    characters = relationship("Character", back_populates="owner")

class Character(Base):
    __tablename__ = 'characters'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    class_name = Column(String, nullable=False)
    level = Column(Integer, default=1)
    stats = Column(JSON, nullable=False)
    xp = Column(Integer, default=0)
    last_action = Column(DateTime, server_default=func.now())

    owner = relationship("User", back_populates="characters")
    inventory_items = relationship("Inventory", back_populates="character")
    quests = relationship("QuestProgress", back_populates="character")
    transactions = relationship("Transaction", back_populates="character")

class Inventory(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    quantity = Column(Integer, default=1)
    metadata = Column(JSON)

    character = relationship("Character", back_populates="inventory_items")
    item = relationship("Item", back_populates="inventory_entries")

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    rarity = Column(String, nullable=False)
    base_stats = Column(JSON)
    craft_recipe = Column(JSON)

    inventory_entries = relationship("Inventory", back_populates="item")

class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    class_name = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    cost = Column(Integer, nullable=False)
    cooldown = Column(Integer, nullable=False)
    effect = Column(JSON)

class Quest(Base):
    __tablename__ = 'quests'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    requirements = Column(JSON)
    rewards = Column(JSON)

class QuestProgress(Base):
    __tablename__ = 'quest_progress'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=False, index=True)
    quest_id = Column(Integer, ForeignKey('quests.id'), nullable=False)
    progress = Column(JSON)
    status = Column(String, default='in_progress')

    character = relationship("Character", back_populates="quests")
    quest = relationship("Quest")

class Guild(Base):
    __tablename__ = 'guilds'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    leader_id = Column(Integer, ForeignKey('users.id'))
    members = Column(JSON)
    fund_gold = Column(Integer, default=0)
    fund_gems = Column(Integer, default=0)

class Auction(Base):
    __tablename__ = 'auction'
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('characters.id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    price_gold = Column(Integer)
    price_gems = Column(Integer)
    expires_at = Column(DateTime)

class Trade(Base):
    __tablename__ = 'trades'
    id = Column(Integer, primary_key=True)
    from_id = Column(Integer, ForeignKey('characters.id'), nullable=False)
    to_id = Column(Integer, ForeignKey('characters.id'), nullable=False)
    items = Column(JSON)
    gold = Column(Integer)
    gems = Column(Integer)
    status = Column(String, default='pending')

class BattleSession(Base):
    __tablename__ = 'battle_sessions'
    id = Column(Integer, primary_key=True)
    participants = Column(JSON)
    state = Column(JSON)
    created_at = Column(DateTime, server_default=func.now())

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    character_id = Column(Integer, ForeignKey('characters.id'), nullable=False)
    type = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    currency = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    character = relationship("Character", back_populates="transactions")

class Localization(Base):
    __tablename__ = 'localization'
    key = Column(String, primary_key=True)
    locale = Column(String, primary_key=True)
    text = Column(String, nullable=False) 