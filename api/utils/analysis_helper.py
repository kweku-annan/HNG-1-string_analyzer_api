#!/usr/bin/env python
"""String Helper Functions"""

def calculate_length(input_string: str) -> int:
    """Calculates the number of visible characters excluding whitespaces, non-printables, and punctuations"""
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    count = len(input_string)
    return count

# print(calculate_length(" "))


def is_palindrome(input_string: str) -> bool:
    """Returns True if the string reads the same forwards and backwards"""
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    cleaned_string = ''.join(ch.lower() for ch in input_string if ch.isalnum())
    return cleaned_string == cleaned_string[::-1]


def count_unique_characters(input_string: str) -> int:
    """Returns the count of distinct/unique characters in the string"""
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    unique_chars = set(input_string)
    return len(unique_chars)


def word_count(input_string: str) -> int:
    """Returns the number of words in the string"""
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    words = input_string.split()
    return len(words)


def generate_sha256_hash(input_string: str) -> str:
    """Returns the SHA256 hash of the string"""
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    import hashlib
    sha256_hash = hashlib.sha256(input_string.encode()).hexdigest()
    return sha256_hash


def char_frequency(input_string: str) -> dict:
    """Returns a dictionary with the frequency of each character in the string"""
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    frequency = {}
    for ch in input_string:
        frequency[ch] = frequency.get(ch, 0) + 1
    return frequency


def string_properties_summary(input_string: str) -> dict:
    """Returns a summary of various string properties"""
    if not isinstance(input_string, str):
        raise TypeError("Input must be a string")
    properties = {
        "length": calculate_length(input_string),
        "is_palindrome": is_palindrome(input_string),
        "unique_characters": count_unique_characters(input_string),
        "word_count": word_count(input_string),
        "sha256_hash": generate_sha256_hash(input_string),
        "character_frequency": char_frequency(input_string)
    }
    return properties

