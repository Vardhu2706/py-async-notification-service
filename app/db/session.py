# session.py

from sqlmodel import create_engine

engine = create_engine("sqlite:///notifications.db")