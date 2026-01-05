# SQL Optimization Guidelines

## Overview

All SQL queries must follow high-efficiency patterns, regardless of data volume. These practices ensure scalability and optimal performance from day one.

## Query Structure Order

Follow this execution priority: **Filter → Project → Aggregate → Join → Order**

```python
# SQLAlchemy example following optimal structure
from sqlalchemy import select, func
from sqlalchemy.orm import Session

async def get_customer_totals(
    session: Session,
    start_date: date,
    region: str
) -> list[dict]:
    """
    Get customer order totals with optimal query structure.
    
    Args:
        session: Database session.
        start_date: Filter orders from this date.
        region: Customer region filter.
    
    Returns:
        List of customers with their order totals.
    """
    # 1. Filter early with subquery
    filtered_orders = (
        select(
            Order.customer_id,
            func.sum(Order.amount).label("total")
        )
        .where(Order.created_at >= start_date)  # Filter on indexed column
        .where(Order.status == "completed")      # Additional filter
        .group_by(Order.customer_id)             # Aggregate early
        .subquery()
    )
    
    # 2. Join with smaller result set
    query = (
        select(
            Customer.id,
            Customer.name,
            filtered_orders.c.total
        )
        .join(filtered_orders, Customer.id == filtered_orders.c.customer_id)
        .where(Customer.region == region)
        .order_by(filtered_orders.c.total.desc())  # Order last
        .limit(100)
    )
    
    result = await session.execute(query)
    return result.mappings().all()
```

## Core Principles

### 1. Select Only Required Columns

```python
# ✅ Good: explicit columns
query = select(User.id, User.email, User.name).where(User.active == True)

# ❌ Bad: selecting all columns
query = select(User).where(User.active == True)
```

### 2. Filter Early (Predicate Pushdown)

```python
# ✅ Good: filter before join
subquery = (
    select(Order.customer_id, Order.total)
    .where(Order.created_at >= start_date)
    .subquery()
)
query = select(Customer).join(subquery, Customer.id == subquery.c.customer_id)

# ❌ Bad: filter after join
query = (
    select(Customer, Order)
    .join(Order)
    .where(Order.created_at >= start_date)
)
```

### 3. Avoid Functions on Indexed Columns

```python
# ✅ Good: direct comparison
query = select(Order).where(Order.created_at >= datetime(2025, 1, 1))

# ❌ Bad: function prevents index usage
query = select(Order).where(func.year(Order.created_at) == 2025)

# ❌ Bad: function on column
query = select(User).where(func.lower(User.email) == email.lower())

# ✅ Good: store normalized data or use functional index
query = select(User).where(User.email_normalized == email.lower())
```

### 4. Aggregate Before Joining

```python
# ✅ Good: aggregate in subquery, then join
order_totals = (
    select(
        Order.customer_id,
        func.count(Order.id).label("order_count"),
        func.sum(Order.amount).label("total_amount")
    )
    .group_by(Order.customer_id)
    .subquery()
)

query = (
    select(Customer.name, order_totals.c.order_count, order_totals.c.total_amount)
    .outerjoin(order_totals, Customer.id == order_totals.c.customer_id)
)

# ❌ Bad: join then aggregate (processes more rows)
query = (
    select(
        Customer.name,
        func.count(Order.id),
        func.sum(Order.amount)
    )
    .join(Order)
    .group_by(Customer.id, Customer.name)
)
```

### 5. Use EXISTS Instead of IN for Subqueries

```python
# ✅ Good: EXISTS stops at first match
query = (
    select(Customer)
    .where(
        exists(
            select(Order.id)
            .where(Order.customer_id == Customer.id)
            .where(Order.status == "pending")
        )
    )
)

# ❌ Bad: IN loads all matching IDs
query = (
    select(Customer)
    .where(
        Customer.id.in_(
            select(Order.customer_id).where(Order.status == "pending")
        )
    )
)
```

### 6. Limit Results and Use Pagination

```python
# ✅ Good: always limit results
query = (
    select(Product)
    .where(Product.category == category)
    .order_by(Product.created_at.desc())
    .limit(20)
    .offset(page * 20)
)

# For keyset pagination (more efficient for large offsets)
query = (
    select(Product)
    .where(Product.category == category)
    .where(Product.id > last_seen_id)
    .order_by(Product.id)
    .limit(20)
)
```

### 7. Use Appropriate Join Types

```python
# Use INNER JOIN when you need matching records only
query = select(Order, Customer).join(Customer)

# Use LEFT JOIN when you need all records from left table
query = select(Customer, Order).outerjoin(Order)

# Avoid CROSS JOIN unless explicitly needed
```

## Index-Aware Queries

### Design Queries for Existing Indexes

```python
# If composite index exists on (status, created_at)
# ✅ Good: uses index efficiently (leftmost columns first)
query = (
    select(Order)
    .where(Order.status == "active")
    .where(Order.created_at >= start_date)
)

# ❌ Bad: skips first column of composite index
query = select(Order).where(Order.created_at >= start_date)
```

### Covering Indexes

```python
# If index includes (customer_id, status, amount)
# Query can be satisfied entirely from index
query = (
    select(Order.customer_id, Order.status, Order.amount)
    .where(Order.customer_id == customer_id)
)
```

## Batch Operations

```python
# ✅ Good: batch inserts
async def bulk_insert_users(session: Session, users: list[dict]) -> None:
    """Insert users in batches for efficiency."""
    await session.execute(insert(User), users)
    await session.commit()

# ✅ Good: batch updates with single query
async def deactivate_old_users(session: Session, cutoff_date: date) -> int:
    """Deactivate users who haven't logged in since cutoff."""
    result = await session.execute(
        update(User)
        .where(User.last_login < cutoff_date)
        .values(active=False)
    )
    await session.commit()
    return result.rowcount

# ❌ Bad: updating one by one
for user_id in user_ids:
    await session.execute(
        update(User).where(User.id == user_id).values(active=False)
    )
```

## Query Analysis

Always analyze slow queries:

```python
# Get query execution plan
from sqlalchemy import text

async def explain_query(session: Session, query) -> str:
    """Get execution plan for query optimization."""
    compiled = query.compile(compile_kwargs={"literal_binds": True})
    explain = await session.execute(text(f"EXPLAIN ANALYZE {compiled}"))
    return explain.fetchall()
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| `SELECT *` | Fetches unnecessary data | Select specific columns |
| `DISTINCT` without need | Forces sorting/dedup | Use proper joins or EXISTS |
| `ORDER BY` on large sets | Full sort before limit | Add WHERE to reduce set first |
| `LIKE '%value%'` | Cannot use index | Use full-text search or prefix match |
| N+1 queries | Multiple round trips | Use eager loading or joins |
| Functions on WHERE columns | Prevents index usage | Store computed values or use functional indexes |
