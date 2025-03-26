import os

# RDS connection details
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_NAME = os.getenv("DB_NAME", "tony")
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Database configuration
engine = create_engine(DB_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Episode(Base):
    __tablename__ = 'episodes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    video_id = Column(String, nullable=False)
    created = Column(DateTime, default=func.now())
    is_validation = Column(Boolean)
    unbelievable = Column(Integer)
    oh_shit = Column(Integer)
    absolutely_incredible = Column(Integer)
    insane = Column(Integer)
    holy_shit = Column(Integer)
    holy_fucking_shit = Column(Integer)
    what_the_fuck = Column(Integer)
    wow = Column(Integer)
    jesus_christ = Column(Integer)
    incredible = Column(Integer)
    that_was_wild = Column(Integer)
    that_was_amazing = Column(Integer)
    oh_my_god = Column(Integer)
    comments = relationship("Comment", back_populates="episodes")

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    episode_id = Column(Integer, ForeignKey('episodes.id'), nullable=False)
    comment_youtube_id = Column(String, nullable=False)
    episodes = relationship("Episode", back_populates="comments")


# Utility functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def add_record(db, record):
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

def get_record(db, model, record_id):
    return db.query(model).filter(model.id == record_id).first()

def get_all_records(db, model):
    return db.query(model).all()

def delete_record(db, model, record_id):
    record = db.query(model).filter(model.id == record_id).first()
    if record:
        db.delete(record)
        db.commit()
    return record

def update_record(db, model, record_id, update_data):
    record = db.query(model).filter(model.id == record_id).first()
    if record:
        for key, value in update_data.items():
            setattr(record, key, value)
        db.commit()
    return record
# Initialize DB (run once to create tables)
def init_db():
    Base.metadata.create_all(bind=engine)

def write(record):
    db_gen = get_db()
    db = next(db_gen)
    record = add_record(db, record)
    db.close()
    return record


def update(record, model):
    db_gen = get_db()
    db = next(db_gen)
    record = update_record(db, model, record.id, record.__dict__)
    db.close()
    return record