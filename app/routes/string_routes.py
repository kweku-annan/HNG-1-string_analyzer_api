#!/usr/bin/env python
"""Defines routes for string analysis operations."""
from crypt import methods

from flask import Blueprint, request, jsonify
from requests.utils import parse_dict_header

from app.models.string_analyzer import StringAnalyzer

from app.schemas.dbStorage import DBStorage
from app.utils.analysis_helper import generate_sha256_hash, string_properties_summary, word_count

string_bp = Blueprint('string_analysis', __name__)
storage = DBStorage()

@string_bp.route('/strings', methods=['POST'])
def create_string():
    from datetime import datetime, timezone
    """Creates a new string analysis record."""
    data = request.get_json()
    value = data.get('value')

    if not isinstance(value, str):
        return jsonify({"422 Unprocessable Entity": 'Invalid data type for "value" (must be string)'}), 422
    if storage.exists(value):
        return jsonify({"409 Conflict": "String already exists in the system"}), 409
    if not value:
        return jsonify({"400 Bad Request": 'Invalid request body or missing "value" field'}), 400

    id = generate_sha256_hash(value)
    properties = string_properties_summary(value)
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    string_record = StringAnalyzer(id=id, value=value, properties=properties, created_at=created_at)
    storage.save(string_record)
    return jsonify(storage.to_dict(string_record)), 201

@string_bp.route('/strings/<string:value>', methods=['GET'])
def get_string(value):
    """Retrieves a string analysis record by its value."""
    string_record = storage.get_by_value(value)
    if not string_record:
        return jsonify({"4o4 Not Found": "String does not exist in the system"}), 404
    return jsonify(string_record.to_dict()), 200

# Get all strings with filtering
@string_bp.route('/strings', methods=['GET'])
def get_all_strings():
    """Retrieves all string analysis records with parameters"""

    # Get all the query parameters
    is_palindrome = request.args.get('is_palindrome')
    min_length = request.args.get('min_length')
    max_length = request.args.get('max_length')
    word_count_ = request.args.get('word_count')
    contains_character = request.args.get('contains_character')

    # Convert and validate the parameters
    filters = {}
    filters_applied = {}

    try:
        # Handle is palindrome filter
        if is_palindrome is not None:
            if is_palindrome.lower() == 'true':
                filters['is_palindrome'] = True
                filters_applied['is_palindrome'] = True
            elif is_palindrome.lower() == 'false':
                filters['is_palindrome'] = False
                filters_applied['is_palindrome'] = False
            else:
                return jsonify({"400 Bad Request": 'Invalid value for "is_palindrome" (must be true or false)'}), 400

        # Handle min length filter
        if min_length is not None:
            filters['min_length'] = int(min_length)
            filters_applied['min_length'] = int(min_length)

        # Handle max length filter
        if max_length is not None:
            filters['max_length'] = int(max_length)
            filters_applied['max_length'] = int(max_length)

        # Handle word count filter
        if word_count_ is not None:
            filters['word_count'] = int(word_count_)
            filters_applied['word_count'] = int(word_count_)

        # Handle contains character filter
        if contains_character is not None:
            if len(contains_character) != 1:
                return jsonify({"400 Bad Request": 'Invalid value for "contains_character" (must be a single character)'}), 400
            filters['contains_character'] = contains_character
            filters_applied['contains_character'] = contains_character

    except ValueError:
        return jsonify({"400 Bad Request": "Invalid query parameter type"}), 400

    # Query the database with filters
    results = storage.get_all(filters)

    # Convert each object to dictionary
    data = []
    for obj in results:
        data.append(storage.to_dict(obj))

    # Build response
    response = {
        "data": data,
        "count": len(data),
        "filters_applied": filters_applied
    }
    return jsonify(response), 200

@string_bp.route('/strings/filter-by-natural-language', methods=['GET'])
def filter_by_natural_language():
    query = request.args.get('query')

    if not query:
        return jsonify({"400 Bad Request": 'Missing "query" parameter'}), 400

    # Convert to lowercases for easier matching
    query_lower = query.lower()

    # Create a dictionary to hold parsed filters
    parsed_filters = {}

    # Check for palindrome keywords
    if 'palindrome' in query_lower or 'palindromic' in query_lower:
        if 'not' in query_lower or "isn't" in query_lower or "is not" in query_lower:
            parsed_filters['is_palindrome'] = False
        else:
            parsed_filters['is_palindrome'] = True

    # Check for word count
    if 'word' or 'single word' or 'one word' or '1 word' in query_lower:
        parsed_filters['word_count'] = 1
    elif 'two words' or '2 words' in query_lower:
        parsed_filters['word_count'] = 2
    elif 'three words' or '3 words' in query_lower:
        parsed_filters['word_count'] = 3
    elif 'multiple words' in query_lower:
        parsed_filters['word_count'] = 'multiple'

    # Check for length patterns
    # Pattern : longer than X
    import re
    longer_than = re.search(r'longer than (\d+)', query_lower)
    if longer_than:
        parsed_filters['min_length'] = int(longer_than.group(1)) + 1

    # Pattern : shorter than X
    shorter_than = re.search(r'shorter than (\d+)', query_lower)
    if shorter_than:
        parsed_filters['max_length'] = int(shorter_than.group(1)) - 1

    # Check for "Contains letter/character X" or "Includes letter/character X"
    contains_match = re.search(r'(contains|includes|containing) (letter|character) (\w)', query_lower)
    if contains_match:
        parsed_filters['contains_character'] = contains_match.group(3)
    else:
        contains_match = re.search(r'contain(?:s|ing)? (?:the )?(?:letter |character )?([a-z])', query_lower)
        if contains_match:
            parsed_filters['contains_character'] = contains_match.group(1)

    # Special Case: "first vowel" means a
    if 'first vowel' in query_lower:
        parsed_filters['contains_character'] = 'a'

    if not parsed_filters:
        return jsonify({"error": "Unable to parse natural language query"}), 400

    # Query the database with parsed filters
    try:
        results = storage.get_all(parsed_filters)
    except Exception as e:
        return jsonify({"error": "Query parsed but resulted in conflicting filters"}), 400

    # Convert each object to dictionary
    data = [storage.to_dict() for obj in results]

    # Build response
    response = {
        "data": data,
        "count": len(data),
        "interpreted_query": {
            "original": query,
            "parsed_filters": parsed_filters
        }
    }
    return jsonify(response), 200

@string_bp.route('/strings/<string:value>', methods=['DELETE'])
def delete_string(value):
    """Deletes a string analysis record by its value"""
    # Check if the string exists
    string_record = storage.get_by_value(value)
    if not string_record:
        return jsonify({"404 Not Found": "String does not exist in the system"}), 404

    # Delete the string record
    storage.delete(string_record)
    return jsonify({}), 204



