"""
Validation Service - Third-party validation for fact quality assurance
Investigates, checks records, and evaluates coherence vs noise
"""
from enum import Enum
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from src.models.fact import Fact
from src.core.facts_registry import FactsRegistry


class ValidationStatus(Enum):
    """Validation status enumeration"""
    COHERENT = "coherent"
    NOISE = "noise"
    SUSPICIOUS = "suspicious"
    UNVALIDATED = "unvalidated"


class ValidationResult:
    """
    Result of a validation check
    
    Attributes:
        fact_id: ID of the validated fact
        status: Validation status
        confidence: Confidence score (0.0 to 1.0)
        findings: List of findings/issues
        metadata: Additional metadata
    """
    
    def __init__(
        self,
        fact_id: str,
        status: ValidationStatus,
        confidence: float,
        findings: List[str],
        metadata: Dict[str, Any]
    ):
        """
        Initialize validation result
        
        Args:
            fact_id: The fact identifier
            status: Validation status
            confidence: Confidence score between 0 and 1
            findings: List of findings
            metadata: Additional metadata
            
        Raises:
            ValueError: If confidence is not between 0 and 1
        """
        if not 0.0 <= confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")
        
        self.fact_id = fact_id
        self.status = status
        self.confidence = confidence
        self.findings = findings
        self.metadata = metadata
        self.timestamp = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation"""
        return {
            'fact_id': self.fact_id,
            'status': self.status.value,
            'confidence': self.confidence,
            'findings': self.findings,
            'metadata': self.metadata,
            'timestamp': self.timestamp.isoformat()
        }


class ValidationService:
    """
    Third-party validation service for fact quality assurance
    
    Provides investigation, record checking, and coherence evaluation
    to distinguish coherent information from noise
    """
    
    def __init__(self, registry: Optional[FactsRegistry] = None):
        """
        Initialize the validation service
        
        Args:
            registry: Facts registry instance (creates new if not provided)
        """
        self.registry = registry if registry is not None else FactsRegistry()
        self.validation_results: Dict[str, ValidationResult] = {}
        
        # Initialize validation rules
        self.validation_rules: List[Callable[[Fact], Dict[str, Any]]] = [
            self._check_statement_length,
            self._check_category_validity,
            self._check_tag_coherence,
        ]
    
    def investigate_fact(self, fact: Fact) -> Dict[str, Any]:
        """
        Investigate a fact and return detailed information
        
        Args:
            fact: The fact to investigate
            
        Returns:
            Dictionary containing investigation details
        """
        tag_coherence = self._analyze_tag_coherence(fact)
        
        return {
            'fact_id': fact.id,
            'category': fact.category,
            'statement_length': len(fact.statement),
            'tag_count': len(fact.tags),
            'verified': fact.verified,
            'tag_coherence': tag_coherence,
            'has_metadata': bool(fact.metadata),
            'timestamp': fact.timestamp.isoformat()
        }
    
    def check_records(self, fact_id: str) -> Dict[str, Any]:
        """
        Check records for a specific fact
        
        Args:
            fact_id: The fact identifier to check
            
        Returns:
            Dictionary containing record check results
        """
        fact = self.registry.get_fact(fact_id)
        
        if fact is None:
            return {
                'found': False,
                'error': f"Fact '{fact_id}' not found in registry"
            }
        
        return {
            'found': True,
            'fact_id': fact.id,
            'has_valid_id': bool(fact.id and fact.id.strip()),
            'has_valid_statement': bool(fact.statement and len(fact.statement) >= 5),
            'has_category': bool(fact.category),
            'tags_present': bool(fact.tags),
            'verified': fact.verified,
            'record_complete': all([
                fact.id,
                fact.category,
                fact.statement,
                fact.timestamp
            ])
        }
    
    def evaluate_coherence(self, fact: Fact) -> ValidationResult:
        """
        Evaluate coherence of a fact to distinguish from noise
        Enhanced with deception detection
        
        Args:
            fact: The fact to evaluate
            
        Returns:
            ValidationResult with coherence assessment
        """
        findings = []
        confidence = 1.0
        
        # Run all validation rules
        for rule in self.validation_rules:
            result = rule(fact)
            if not result['passed']:
                findings.append(result['message'])
                confidence -= result.get('penalty', 0.2)
        
        # Check for external claims
        if fact.metadata.get('external_claim'):
            findings.append("External claims require verifiable evidence")
            confidence -= 0.1
        
        # Add deception detection
        from services.deception_detector import (
            detect_user_correction,
            detect_unverified_claims
        )
        
        # Detect user corrections in the statement
        deception_result = detect_user_correction(fact.statement)
        
        if deception_result.detected:
            # Reduce confidence based on deception probability
            confidence *= (1.0 - deception_result.probability * 0.5)
            findings.append(f"Deception detected: {deception_result.deception_type}")
        
        # Check for unverified claims
        claim_result = detect_unverified_claims(fact.statement)
        if claim_result.detected:
            findings.append("Unverified claims require external validation")
        
        # Ensure confidence stays in bounds
        confidence = max(0.0, min(1.0, confidence))
        
        # Determine status based on confidence and findings
        if confidence >= 0.8 and not findings:
            status = ValidationStatus.COHERENT
        elif confidence >= 0.7:
            status = ValidationStatus.COHERENT
        elif confidence >= 0.4:
            status = ValidationStatus.SUSPICIOUS
        else:
            status = ValidationStatus.NOISE
        
        result = ValidationResult(
            fact_id=fact.id,
            status=status,
            confidence=confidence,
            findings=findings,
            metadata={
                'rules_checked': len(self.validation_rules),
                'deception_checked': True
            }
        )
        
        # Store the result
        self.validation_results[fact.id] = result
        
        return result
    
    def validate_all_facts(self) -> List[ValidationResult]:
        """
        Validate all facts in the registry
        
        Returns:
            List of validation results for all facts
        """
        results = []
        for fact in self.registry.get_all_facts():
            result = self.evaluate_coherence(fact)
            results.append(result)
        return results
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get summary of all validation results
        
        Returns:
            Dictionary containing validation statistics
        """
        if not self.validation_results:
            return {
                'total_validated': 0,
                'coherent': 0,
                'suspicious': 0,
                'noise': 0,
                'average_confidence': 0.0,
                'coherence_rate': 0.0
            }
        
        total = len(self.validation_results)
        coherent = sum(1 for r in self.validation_results.values() 
                      if r.status == ValidationStatus.COHERENT)
        suspicious = sum(1 for r in self.validation_results.values() 
                        if r.status == ValidationStatus.SUSPICIOUS)
        noise = sum(1 for r in self.validation_results.values() 
                   if r.status == ValidationStatus.NOISE)
        
        avg_confidence = sum(r.confidence for r in self.validation_results.values()) / total
        coherence_rate = (coherent / total * 100) if total > 0 else 0.0
        
        return {
            'total_validated': total,
            'coherent': coherent,
            'suspicious': suspicious,
            'noise': noise,
            'average_confidence': round(avg_confidence, 3),
            'coherence_rate': round(coherence_rate, 2)
        }
    
    def _check_statement_length(self, fact: Fact) -> Dict[str, Any]:
        """
        Validation rule: Check statement length
        
        Args:
            fact: The fact to check
            
        Returns:
            Dictionary with validation result
        """
        min_length = 5
        passed = len(fact.statement) >= min_length
        
        return {
            'passed': passed,
            'message': f"Statement too short (min {min_length} characters)" if not passed else "",
            'penalty': 0.4 if not passed else 0.0
        }
    
    def _check_category_validity(self, fact: Fact) -> Dict[str, Any]:
        """
        Validation rule: Check category validity
        
        Args:
            fact: The fact to check
            
        Returns:
            Dictionary with validation result
        """
        passed = bool(fact.category and fact.category.strip())
        
        return {
            'passed': passed,
            'message': "Category is missing or invalid" if not passed else "",
            'penalty': 0.3 if not passed else 0.0
        }
    
    def _check_tag_coherence(self, fact: Fact) -> Dict[str, Any]:
        """
        Validation rule: Check tag coherence
        
        Args:
            fact: The fact to check
            
        Returns:
            Dictionary with validation result
        """
        passed = len(fact.tags) > 0
        
        return {
            'passed': passed,
            'message': "No tags present - affects discoverability" if not passed else "",
            'penalty': 0.15 if not passed else 0.0
        }
    
    def _analyze_tag_coherence(self, fact: Fact) -> float:
        """
        Analyze tag coherence score
        
        Args:
            fact: The fact to analyze
            
        Returns:
            Coherence score between 0.0 and 1.0
        """
        if not fact.tags:
            return 0.0
        
        tag_count = len(fact.tags)
        
        # Ideal range is 2-5 tags
        if 2 <= tag_count <= 5:
            return 1.0
        elif tag_count == 1:
            return 0.6
        elif 6 <= tag_count <= 10:
            return 0.7
        else:  # More than 10 tags
            return 0.4
