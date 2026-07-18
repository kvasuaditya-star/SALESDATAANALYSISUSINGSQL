# 📊 Sales Data Analysis Using SQL - Day 3: Mock Data Generation & Seeding

An end-to-end relational database analysis project designed to extract actionable business intelligence from structured sales, customer, and payment data.

This project implements a fully relational database structured with primary keys, foreign keys, checks, and cascade rules to analyze sales trends and customer behavior.

---

## 🏗️ Database Architecture

The project schema represents a typical retail e-commerce database with 5 interconnected tables.

*(See Day 1 branch for full Mermaid ER diagram)*

---

## 🚀 How to Run the Project

This project runs out of the box using Python's standard library (no pip installations required).

### 1. Initialize the Database
Build the schema and create the SQLite database file:
```bash
python scripts/db_setup.py
```

### 2. Populate Mock Data
Generate a realistic 12-month transaction history:
```bash
python scripts/generate_data.py
```
*Seeds the database with mock customers, products, orders, and payments.*
