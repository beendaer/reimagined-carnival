"""
Fact model - Data transfer object for determined facts
Maintains fact data structure and coherence within the monolith
"""
from datetime import datetime
from typing import List, Dict, Any, Optional


class Fact:
    """
    Fact model representing a determined fact in the system
    
    Attributes:
        id: Unique identifier for the fact
        category: Category classification
        statement: The fact statement
        verified: Whether the fact has been verified
        timestamp: When the fact was created
        tags: List of tags for categorization
        metadata: Optional additional metadata
    """
    
    def __init__(
        self,
        id: str,
        category: str,
        statement: str,
        verified: bool,
        timestamp: datetime,
        tags: List[str],
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a Fact instance
        
        Args:
            id: Unique identifier (cannot be empty)
            category: Category classification
            statement: The fact statement
            verified: Verification status
            timestamp: Creation timestamp
            tags: List of tags
            metadata: Optional metadata dictionary
            
        Raises:
            ValueError: If id is empty
        """
        if not id or id.strip() == "":
            raise ValueError("Fact ID cannot be empty")
        
        self.id = id
        self.category = category
        self.statement = statement
        self.verified = verified
        self.timestamp = timestamp
        self.tags = tags if tags else []
        self.metadata = metadata if metadata is not None else {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert fact to dictionary representation
        
        Returns:
            Dictionary representation of the fact
        """
        return {
            'id': self.id,
            'category': self.category,
            'statement': self.statement,
            'verified': self.verified,
            'timestamp': self.timestamp.isoformat(),
            'tags': self.tags,
            'metadata': self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Fact':
        """
        Create a Fact instance from dictionary
        
        Args:
            data: Dictionary containing fact data
            
        Returns:
            New Fact instance
        """
        timestamp_str = data.get('timestamp')
        if isinstance(timestamp_str, str):
            timestamp = datetime.fromisoformat(timestamp_str)
        elif isinstance(timestamp_str, datetime):
            timestamp = timestamp_str
        else:
            timestamp = datetime.now()
        
        return cls(
            id=data['id'],
            category=data['category'],
            statement=data['statement'],
            verified=data['verified'],
            timestamp=timestamp,
            tags=data.get('tags', []),
            metadata=data.get('metadata', {})
        )
    
    def __repr__(self) -> str:
        """String representation of the fact"""
        return f"Fact(id='{self.id}', category='{self.category}', verified={self.verified})"
    
    def __eq__(self, other) -> bool:
        """Check equality based on id"""
        if not isinstance(other, Fact):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        """Hash based on id for use in sets/dicts"""
        return hash(self.id)
