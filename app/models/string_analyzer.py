#!/usr/bin/env python
"""StringAnalyzer model"""
from sqlalchemy import Column, String, Integer, JSON
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class StringAnalyzer(Base):
    """StringAnalyzer Model to store string analysis results"""
    __tablename__ = 'string_analyzers'

    id = Column(String(60), primary_key=True, nullable=False)
    value = Column(String(256), nullable=False)
    properties = Column(JSON, nullable=False)
    created_at = Column(String(60), nullable=False)

    def __init__(self, id: str, value: str, properties: dict, created_at):
        """Initializes the StringAnalyzer instance"""
        self.id = id
        self.value = value
        self.properties = properties
        self.created_at = created_at


