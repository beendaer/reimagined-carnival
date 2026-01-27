"""
Validation Service - Third-party validation for research framework
Investigates facts, checks records, and evaluates coherence vs noise
"""
from typing import List, Dict, Any, Optional
from enum import Enum
from dataclasses import dataclass
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from models.fact import Fact
from core.facts_registry import FactsRegistry


class ValidationStatus(Enum):
    """Status of fact validation"""
    COHERENT = "coherent"
    NOISE = "noise"
    SUSPICIOUS = "suspicious"
    UNVALIDATED = "unvalidated"


@dataclass
class ValidationResult:
    """Result of third-party validation"""
    fact_id: str
    status: ValidationStatus
    confidence: float  # 0.0 to 1.0
    findings: List[str]
    metadata: Dict[str, Any]
    
    def __post_init__(self):
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")


class ValidationService:
    """
    Third-party validation service for research framework.
    Investigates facts, checks records, and evaluates coherence.
    Follows best practices for validation and quality assurance.
    """
    
    def __init__(self, facts_registry: FactsRegistry = None):
        self.facts_registry = facts_registry or FactsRegistry()
        self.validation_results: Dict[str, ValidationResult] = {}
        self.validation_rules: List[callable] = []
        self._initialize_default_rules()
    
    def _initialize_default_rules(self) -> None:
        """Initialize default validation rules"""
        self.validation_rules = [
            self._check_statement_length,
            self._check_category_validity,
            self._check_tag_coherence,
            self._check_timestamp_validity,
        ]
    
    def investigate_fact(self, fact: Fact) -> Dict[str, Any]:
        """
        Investigate a fact to gather information for validation.
        Best practice: thorough investigation before validation.
        """
        investigation = {
            'fact_id': fact.id,
            'category': fact.category,
            'statement_length': len(fact.statement),
            'tag_count': len(fact.tags),
            'has_metadata': fact.metadata is not None and len(fact.metadata) > 0,
            'verified': fact.verified,
            'timestamp': fact.timestamp.isoformat(),
        }
        
        # Check for related facts in same category
        related_facts = self.facts_registry.get_facts_by_category(fact.category)
        # Count related facts (may include the fact itself if already registered)
        investigation['related_facts_count'] = max(0, len(related_facts) - (1 if fact in related_facts else 0))
        
        # Analyze tags for coherence
        investigation['tag_coherence'] = self._analyze_tag_coherence(fact)
        
        return investigation
    
    def check_records(self, fact_id: str) -> Dict[str, Any]:
        """
        Check records for a specific fact.
        Best practice: validate against registry records.
        """
        fact = self.facts_registry.get_fact(fact_id)
        if not fact:
            return {
                'found': False,
                'error': f"Fact {fact_id} not found in registry"
            }
        
        # Verify record integrity
        checks = {
            'found': True,
            'fact_id': fact_id,
            'has_valid_id': bool(fact.id),
            'has_valid_statement': bool(fact.statement) and len(fact.statement) > 0,
            'has_category': bool(fact.category),
            'has_timestamp': fact.timestamp is not None,
            'tags_present': len(fact.tags) > 0,
        }
        
        # Check for duplicates or conflicts
        category_facts = self.facts_registry.get_facts_by_category(fact.category)
        checks['category_fact_count'] = len(category_facts)
        
        return checks
    
    def evaluate_coherence(self, fact: Fact) -> ValidationResult:
        """
        Evaluate if a fact represents coherent information or noise.
        Best practice: multi-criteria evaluation for accuracy.
        """
        findings = []
        confidence = 1.0
        
        # Run all validation rules
        for rule in self.validation_rules:
            rule_result = rule(fact)
            if not rule_result['passed']:
                findings.append(rule_result['message'])
                confidence *= rule_result['confidence_impact']
        
        # Additional coherence checks
        investigation = self.investigate_fact(fact)
        
        # Check for related facts (coherence with category)
        if investigation['related_facts_count'] == 0:
            findings.append("No related facts in category - potential isolation")
            confidence *= 0.95
        
        # Determine validation status
        if confidence >= 0.8:
            status = ValidationStatus.COHERENT
        elif confidence >= 0.5:
            status = ValidationStatus.SUSPICIOUS
        else:
            status = ValidationStatus.NOISE
        
        result = ValidationResult(
            fact_id=fact.id,
            status=status,
            confidence=confidence,
            findings=findings if findings else ["Fact passes all validation checks"],
            metadata={
                'investigation': investigation,
                'rules_applied': len(self.validation_rules)
            }
        )
        
        self.validation_results[fact.id] = result
        return result
    
    def validate_all_facts(self) -> List[ValidationResult]:
        """
        Validate all facts in the registry.
        Best practice: comprehensive validation of entire dataset.
        """
        results = []
        
        # Validate each fact
        for fact_id in self.facts_registry._facts.keys():
            fact = self.facts_registry.get_fact(fact_id)
            if fact:
                result = self.evaluate_coherence(fact)
                results.append(result)
        
        return results
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get summary of validation results.
        Best practice: provide actionable insights.
        """
        if not self.validation_results:
            return {
                'total_validated': 0,
                'coherent': 0,
                'suspicious': 0,
                'noise': 0,
                'average_confidence': 0.0
            }
        
        coherent = sum(1 for r in self.validation_results.values() 
                      if r.status == ValidationStatus.COHERENT)
        suspicious = sum(1 for r in self.validation_results.values() 
                        if r.status == ValidationStatus.SUSPICIOUS)
        noise = sum(1 for r in self.validation_results.values() 
                   if r.status == ValidationStatus.NOISE)
        
        avg_confidence = sum(r.confidence for r in self.validation_results.values()) / len(self.validation_results)
        
        return {
            'total_validated': len(self.validation_results),
            'coherent': coherent,
            'suspicious': suspicious,
            'noise': noise,
            'average_confidence': avg_confidence,
            'coherence_rate': (coherent / len(self.validation_results)) * 100
        }
    
    # Validation rule methods
    
    def _check_statement_length(self, fact: Fact) -> Dict[str, Any]:
        """Check if statement has reasonable length"""
        statement_len = len(fact.statement)
        if statement_len < 5:
            return {
                'passed': False,
                'message': "Statement is too short (< 5 characters)",
                'confidence_impact': 0.5
            }
        elif statement_len > 1000:
            return {
                'passed': False,
                'message': "Statement is excessively long (> 1000 characters)",
                'confidence_impact': 0.8
            }
        return {'passed': True, 'message': '', 'confidence_impact': 1.0}
    
    def _check_category_validity(self, fact: Fact) -> Dict[str, Any]:
        """Check if category is valid and not empty"""
        if not fact.category or len(fact.category.strip()) == 0:
            return {
                'passed': False,
                'message': "Category is empty or invalid",
                'confidence_impact': 0.6
            }
        return {'passed': True, 'message': '', 'confidence_impact': 1.0}
    
    def _check_tag_coherence(self, fact: Fact) -> Dict[str, Any]:
        """Check if tags are coherent with category"""
        if not fact.tags:
            return {
                'passed': False,
                'message': "No tags provided",
                'confidence_impact': 0.9
            }
        
        # Check if category appears in tags (best practice)
        category_words = fact.category.lower().split('_')
        tag_words = [tag.lower() for tag in fact.tags]
        
        has_category_overlap = any(word in ' '.join(tag_words) for word in category_words)
        if not has_category_overlap and len(fact.tags) > 0:
            return {
                'passed': False,
                'message': "Tags may not be coherent with category",
                'confidence_impact': 0.95
            }
        
        return {'passed': True, 'message': '', 'confidence_impact': 1.0}
    
    def _check_timestamp_validity(self, fact: Fact) -> Dict[str, Any]:
        """Check if timestamp is valid"""
        if not fact.timestamp:
            return {
                'passed': False,
                'message': "Missing timestamp",
                'confidence_impact': 0.9
            }
        return {'passed': True, 'message': '', 'confidence_impact': 1.0}
    
    def _analyze_tag_coherence(self, fact: Fact) -> float:
        """Analyze coherence score of tags (0.0 to 1.0)"""
        if not fact.tags:
            return 0.0
        
        # Check tag quality
        score = 1.0
        
        # Penalize too many tags (noise)
        if len(fact.tags) > 10:
            score *= 0.7
        
        # Penalize duplicate tags
        if len(fact.tags) != len(set(fact.tags)):
            score *= 0.8
        
        # Check for empty tags
        if any(not tag.strip() for tag in fact.tags):
            score *= 0.5
        
        return score
