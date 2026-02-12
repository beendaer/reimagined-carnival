# Database Migration Preparation

**Status:** Prepared but not implemented  
**Target:** PostgreSQL on Azure  
**Current State:** In-memory storage only

---

## Overview

This document outlines the preparation for migrating from in-memory storage to PostgreSQL. The migration is **planned but not yet implemented**. All necessary dependencies and configuration templates are ready.

## Dependencies Installed

The following database-related packages are included in `requirements.txt`:

- `psycopg2-binary>=2.9.9,<3.0.0` - PostgreSQL driver
- `python-dotenv>=1.0.0,<2.0.0` - Environment variable management

## Environment Variables

When PostgreSQL is implemented, the following environment variables will be needed:

```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@host:5432/dbname
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=false

# Alternative format for Azure PostgreSQL
POSTGRES_HOST=reimagined-carnival.postgres.database.azure.com
POSTGRES_PORT=5432
POSTGRES_DB=taas_validation
POSTGRES_USER=app_user
POSTGRES_PASSWORD=<secure_password>
POSTGRES_SSL_MODE=require
```

## Planned Database Schema

### Tables

#### `facts` Table
```sql
CREATE TABLE facts (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    validation_status VARCHAR(50),
    validation_score DECIMAL(5, 2)
);

CREATE INDEX idx_facts_created_at ON facts(created_at);
CREATE INDEX idx_facts_validation_status ON facts(validation_status);
```

#### `validation_results` Table
```sql
CREATE TABLE validation_results (
    id SERIAL PRIMARY KEY,
    fact_id INTEGER REFERENCES facts(id),
    deception_patterns JSONB,
    probability DECIMAL(5, 2),
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_validation_results_fact_id ON validation_results(fact_id);
```

#### `api_requests` Table (Audit/Analytics)
```sql
CREATE TABLE api_requests (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(255),
    method VARCHAR(10),
    response_code INTEGER,
    duration_ms INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_agent TEXT,
    ip_address INET
);

CREATE INDEX idx_api_requests_created_at ON api_requests(created_at);
CREATE INDEX idx_api_requests_endpoint ON api_requests(endpoint);
```

## Migration Strategy

### Phase 1: Dual Write (Current → PostgreSQL)
1. Keep in-memory storage operational
2. Add PostgreSQL writes in parallel
3. Validate data consistency
4. Monitor performance impact

### Phase 2: Dual Read (PostgreSQL primary, in-memory fallback)
1. Switch reads to PostgreSQL
2. Keep in-memory as fallback
3. Monitor query performance
4. Verify data integrity

### Phase 3: Full Migration
1. Remove in-memory storage
2. PostgreSQL as single source of truth
3. Implement connection pooling
4. Add database monitoring

## Connection Management

### Planned Implementation (SQLAlchemy)

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
import os

# Database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL')

# Create engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Azure PostgreSQL Setup

### Resource Configuration
- **Service:** Azure Database for PostgreSQL - Flexible Server
- **Tier:** Standard_D2s_v3 (2 vCores, 8 GB RAM)
- **Storage:** 32 GB with auto-grow enabled
- **Backup:** 7-day retention with geo-redundancy
- **SSL:** Enforced (TLS 1.2+)

### Security
- Firewall rules for GitHub Actions runner IPs
- Private endpoint for production
- Azure AD authentication recommended
- Connection string in Azure Key Vault

## Testing Before Migration

### Local PostgreSQL Setup
```bash
# Using Docker for local testing
docker run --name postgres-local \
  -e POSTGRES_PASSWORD=local_dev_password \
  -e POSTGRES_DB=taas_validation \
  -p 5432:5432 \
  -d postgres:16-alpine

# Connect and verify
psql -h localhost -U postgres -d taas_validation
```

### Test Data Migration
```bash
# Export current in-memory data (when available)
python scripts/export_data.py > data/backup.json

# Import to PostgreSQL (after implementation)
python scripts/import_data.py data/backup.json
```

## Performance Considerations

### Indexing Strategy
- Primary keys on all tables
- Indexes on frequently queried columns
- Partial indexes for common filters
- JSONB indexes for metadata queries

### Query Optimization
- Use prepared statements
- Implement query result caching (Redis)
- Monitor slow query log
- Regular VACUUM and ANALYZE

## Monitoring

### Key Metrics to Track
- Connection pool utilization
- Query execution time (p50, p95, p99)
- Transaction throughput
- Database CPU and memory usage
- Replication lag (if applicable)

### Tools
- Azure Monitor for PostgreSQL
- Application Insights integration
- Custom logging in application

## Rollback Plan

If migration issues occur:
1. Switch application back to in-memory mode
2. Investigate PostgreSQL issues offline
3. Fix and re-test in staging
4. Retry migration with fixes applied

## Next Steps

1. **Staging Environment:** Set up PostgreSQL on Azure staging
2. **ORM Models:** Implement SQLAlchemy models
3. **Repository Layer:** Create database access layer
4. **Integration Tests:** Add tests with test database
5. **Migration Scripts:** Write data migration tools
6. **Documentation:** Update API docs with persistence notes

---

**Note:** This is a preparation document. No database code has been added to the application yet. When implementing, follow the CLI-centric automation approach and ensure all operations are scriptable.
