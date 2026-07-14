# 📊 Sales Data Analysis Using SQL - Day 1: Schema Design & ERD Setup

An end-to-end relational database analysis project designed to extract actionable business intelligence from structured sales, customer, and payment data.

This project implements a fully relational database structured with primary keys, foreign keys, checks, and cascade rules to analyze sales trends and customer behavior.

---

## 🏗️ Database Architecture

The project schema represents a typical retail e-commerce database with 5 interconnected tables.

```mermaid
erDiagram
    customers ||--o{ orders : "places"
    orders ||--|{ order_items : "contains"
    products ||--o{ order_items : "ordered in"
    orders ||--o| payments : "paid by"

    customers {
        integer customer_id PK
        text first_name
        text last_name
        text email UK
        text phone
        text city
        text state
        text join_date
    }
    products {
        integer product_id PK
        text product_name
        text category
        real price
        real cost
        integer stock_quantity
    }
    orders {
        integer order_id PK
        integer customer_id FK
        text order_date
        text status
        real total_amount
    }
    order_items {
        integer order_item_id PK
        integer order_id FK
        integer product_id FK
        integer quantity
        real unit_price
    }
    payments {
        integer payment_id PK
        integer order_id FK
        text payment_date
        text payment_method
        real payment_amount
    }
```

### Table Definitions
1. **`customers`**: Stores profile information, location details, and registration dates.
2. **`products`**: Maintains catalog items with sales prices, acquisition costs (for margin calculation), and stock counts.
3. **`orders`**: Logs transactional metadata including order timestamps, completion statuses, and overall totals.
4. **`order_items`**: Resolves the many-to-many relationship between orders and products, capturing quantity and historical price at transaction time.
5. **`payments`**: Details receipt values, dates, and payment methods.
