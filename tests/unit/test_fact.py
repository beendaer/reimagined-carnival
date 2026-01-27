"""
Unit tests for the Fact model
Testing determined facts coherence within the monolith
"""
import unittest
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'src'))

from models.fact import Fact


class TestFact(unittest.TestCase):
    """Test cases for the Fact model"""
    
    def test_fact_creation(self):
        """Test creating a valid fact"""
        fact = Fact(
            id="test_001",
            category="test",
            statement="This is a test fact",
            verified=True,
            timestamp=datetime.now(),
            tags=["test", "unit"]
        )
        
        self.assertEqual(fact.id, "test_001")
        self.assertEqual(fact.category, "test")
        self.assertTrue(fact.verified)
    
    def test_fact_validation(self):
        """Test fact validation on creation"""
        with self.assertRaises(ValueError):
            Fact(
                id="",
                category="test",
                statement="Invalid fact",
                verified=True,
                timestamp=datetime.now(),
                tags=[]
            )
    
    def test_fact_to_dict(self):
        """Test fact serialization to dictionary"""
        timestamp = datetime.now()
        fact = Fact(
            id="test_002",
            category="test",
            statement="Serialization test",
            verified=False,
            timestamp=timestamp,
            tags=["test"]
        )
        
        fact_dict = fact.to_dict()
        
        self.assertEqual(fact_dict['id'], "test_002")
        self.assertEqual(fact_dict['statement'], "Serialization test")
        self.assertFalse(fact_dict['verified'])
    
    def test_fact_from_dict(self):
        """Test fact deserialization from dictionary"""
        timestamp = datetime.now()
        fact_data = {
            'id': 'test_003',
            'category': 'test',
            'statement': 'Deserialization test',
            'verified': True,
            'timestamp': timestamp.isoformat(),
            'tags': ['test', 'deserialize']
        }
        
        fact = Fact.from_dict(fact_data)
        
        self.assertEqual(fact.id, 'test_003')
        self.assertEqual(fact.statement, 'Deserialization test')
        self.assertTrue(fact.verified)


if __name__ == '__main__':
    unittest.main()
