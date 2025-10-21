#!/usr/bin/env python
"""Databse Storage Schema using SQLAlchemy and SQLite"""
import sqlite3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage:
    """Manages storage of SQLAlchemy database using SQLite"""
    __engine = None
    __session = None # Session class instance

    def __init__(self):
        pass