"""
Configuration for the TAAS Monolith
Following industry best practices for configuration management
"""

# Monolith Configuration
MONOLITH_CONFIG = {
    'name': 'TAAS Monolith',
    'version': '1.0.0',
    'description': 'Testing as a Service Monolith with Coherent Facts Registry',
    
    # Facts Registry Configuration
    'facts_registry': {
        'enable_persistence': True,
        'auto_verify': True,
        'max_facts': 10000
    },
    
    # Test Service Configuration
    'test_service': {
        'parallel_execution': False,
        'timeout_seconds': 30,
        'retry_failed_tests': False
    },
    
    # Logging Configuration
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    }
}

# Environment-specific configurations
ENVIRONMENTS = {
    'development': {
        'debug': True,
        'test_mode': True
    },
    'production': {
        'debug': False,
        'test_mode': False
    }
}
