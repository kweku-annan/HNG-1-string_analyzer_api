#!/usr/bin/env python
"""Databse Storage Schema using SQLAlchemy and SQLite"""
import sqlite3

from sqlalchemy import create_engine, Integer, func, cast
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models.string_analyzer import Base, StringAnalyzer


class DBStorage:
    """Manages storage of SQLAlchemy database using SQLite"""
    __engine = None
    __session = None # Session class instance

    def __init__(self):
        """Creates the engine and session"""
        self.__engine = create_engine('sqlite:///string_analyzer.db', pool_pre_ping=True)

        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session

    def save(self, obj):
        """Saves an object to the database"""
        try:
            self.__session.add(obj)
            self.__session.commit()
        except Exception as e:
            self.__session.rollback()
            raise e

    def close(self):
        """Closes the current session"""
        self.__session.remove()

    def exists(self, value):
        """Checks if a StringAnalyzer with the given value exists"""
        return self.__session.query(StringAnalyzer).filter_by(value=value).first() is not None

    def get_by_value(self, value):
        """Retrieves a StringAnalyzer by its value"""
        # Query and return the object, or None if not found
        return self.__session.query(StringAnalyzer).filter_by(value=value).first()

    def get_all(self, filters=None):
        """Retrieves all StringAnalyzer records, optionally filtered by criteria"""
        query = self.__session.query(StringAnalyzer)
        if filters:
            # Handle is_palindrome filter
            if 'is_palindrome' in filters:
                val = 1 if filters['is_palindrome'] else 0
                query = query.filter(cast(func.json_extract(StringAnalyzer.properties, '$.is_palindrome'), Integer) == val)

            # Handle min_length filter
            if 'min_length' in filters:
                query = query.filter(
                    cast(func.json_extract(StringAnalyzer.properties, '$.length'), Integer) >= filters['min_length']
                )

            # Handle max_length filter
            if 'max_length' in filters:
                query = query.filter(
                    cast(func.json_extract(StringAnalyzer.properties, '$.length'), Integer) <= filters['max_length']
                )

            # Handle word_count filter
            if 'word_count' in filters:
                query = query.filter(
                    cast(func.json_extract(StringAnalyzer.properties, '$.word_count'), Integer) == filters['word_count']
                )

            # Handle contains_character filter
            if 'contains_character' in filters:
                char = filters['contains_character']
                # You need to check if the character exists in the value
                query = query.filter(StringAnalyzer.value.contains(char))

        return query.all()


    def delete(self, value):
        """Deletes a StringAnalyzer by its value"""
        obj = self.get_by_value(value)
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def to_dict(self, obj):
        """Converts a StringAnalyzer object to a dictionary"""
        return {
            'id': obj.id,
            'value': obj.value,
            'properties': obj.properties,
            'created_at': obj.created_at
        }


