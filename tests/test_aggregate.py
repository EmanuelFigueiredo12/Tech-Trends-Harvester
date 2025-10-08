"""
Tests for aggregation functions
Author: Rich Lewis
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.aggregate import categorize_term


def test_categorize_term():
    """Test term categorization"""
    # AI/ML
    assert categorize_term("machine learning tutorial") == "AI/ML"
    assert categorize_term("GPT-4 prompts") == "AI/ML"
    
    # Cloud/DevOps
    assert categorize_term("kubernetes deployment") == "Cloud/DevOps"
    assert categorize_term("docker containers") == "Cloud/DevOps"
    
    # Frontend
    assert categorize_term("react hooks") == "Frontend"
    assert categorize_term("vue components") == "Frontend"
    
    # Backend
    assert categorize_term("REST API design") == "Backend"
    assert categorize_term("GraphQL server") == "Backend"
    
    # Database
    assert categorize_term("PostgreSQL optimization") == "Database"
    assert categorize_term("MongoDB queries") == "Database"
    
    # Language
    assert categorize_term("Python 3.12 features") == "Language"
    assert categorize_term("Rust programming") == "Language"
    
    # Tools
    assert categorize_term("VS Code extensions") == "Tools"
    assert categorize_term("Git workflows") == "Tools"
    
    # Security
    assert categorize_term("OAuth implementation") == "Security"
    assert categorize_term("JWT tokens") == "Security"
    
    # Default
    assert categorize_term("random tech stuff") == "Tech"


if __name__ == "__main__":
    test_categorize_term()
    print("[OK] test_categorize_term")
    print("\n[SUCCESS] All tests passed!")
