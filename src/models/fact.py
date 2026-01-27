"""
Fact Model - Represents a determined fact within the monolith
This model ensures coherence of facts across the TAAS system
"""
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime


@dataclass
class Fact:
    """
    A determined fact that maintains coherence within the monolith.
    Following industry best practices for data integrity and validation.
    """
    id: str
    category: str
    statement: str
    verified: bool
    timestamp: datetime
    tags: List[str]
    metadata: Optional[dict] = None
    
    def __post_init__(self):
        """Validate fact data on initialization"""
        if not self.id or not self.statement:
            raise ValueError("Fact must have an id and statement")
        if not self.category:
            raise ValueError("Fact must have a category")
    
    def to_dict(self) -> dict:
        """Convert fact to dictionary for serialization"""
        return {
            'id': self.id,
            'category': self.category,
            'statement': self.statement,
            'verified': self.verified,
            'timestamp': self.timestamp.isoformat(),
            'tags': self.tags,
            'metadata': self.metadata or {}
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Fact':
        """Create a Fact from dictionary data"""
        data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
