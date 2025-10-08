"""
Tests for utility functions
Author: Rich Lewis
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.util import tokenize_title, is_question, extract_question_intent, is_interesting_term


def test_tokenize_title():
    """Test title tokenization"""
    result = tokenize_title("Building a REST API with Python and FastAPI")
    assert "python" in result
    assert "fastapi" in result
    # "rest" and "api" are in BORING_TERMS and filtered out
    assert "building" in result  # Long enough (8 chars) to pass min_length filter


def test_is_question():
    """Test question detection"""
    assert is_question("How to deploy Docker containers?") == True
    assert is_question("What is Kubernetes?") == True
    assert is_question("Why use TypeScript over JavaScript?") == True
    assert is_question("Building a web app") == False
    assert is_question("Python tutorial") == False


def test_extract_question_intent():
    """Test question intent extraction"""
    assert extract_question_intent("How to deploy Docker?") == "how-to"
    assert extract_question_intent("What is Kubernetes?") == "what-is"
    assert extract_question_intent("Why use TypeScript?") == "explainer"
    assert extract_question_intent("Best framework for React?") == "best"
    assert extract_question_intent("Python vs JavaScript comparison") == "comparison"


def test_is_interesting_term():
    """Test term interest filtering"""
    # Interesting tech terms
    assert is_interesting_term("kubernetes") == True
    assert is_interesting_term("typescript") == True
    assert is_interesting_term("machine learning") == True
    
    # Boring terms
    assert is_interesting_term("lib") == False
    assert is_interesting_term("utils") == False
    assert is_interesting_term("the") == False


if __name__ == "__main__":
    # Run tests manually
    test_tokenize_title()
    print("[OK] test_tokenize_title")
    
    test_is_question()
    print("[OK] test_is_question")
    
    test_extract_question_intent()
    print("[OK] test_extract_question_intent")
    
    test_is_interesting_term()
    print("[OK] test_is_interesting_term")
    
    print("\n[SUCCESS] All tests passed!")
