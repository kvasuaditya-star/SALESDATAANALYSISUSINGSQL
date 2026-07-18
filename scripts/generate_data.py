import os
import sqlite3
import random
from datetime import datetime, timedelta

def generate_mock_data():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sales_data.db')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    print("Generating mock data...")

    # 1. Populate Products Table
    products_data = [
        # Electronics
        ("Laptop Pro 15", "Electronics", 1299.99, 850.00, 50),
        ("Smartphone X", "Electronics", 799.99, 480.00, 100),
        ("Wireless Headphones", "Electronics", 149.99, 85.00, 150),
        ("Smartwatch Sport", "Electronics", 249.99, 140.00, 80),
        ("Bluetooth Speaker", "Electronics", 89.99, 45.00, 120),
        
        # Home Appliances
        ("Robotic Vacuum Cleaner", "Home Appliances", 349.99, 210.00, 40),
        ("Digital Espresso Maker", "Home Appliances", 189.99, 110.00, 60),
        ("Air Purifier HEPA", "Home Appliances", 129.99, 75.00, 90),
        ("Microwave Oven", "Home Appliances", 109.99, 65.00, 75),
        
        # Office Supplies
        ("Ergonomic Office Chair", "Office Supplies", 299.99, 175.00, 35),
        ("Standing Desk (Motorized)", "Office Supplies", 449.99, 260.00, 25),
        ("LED Desk Lamp with USB", "Office Supplies", 39.99, 18.00, 110),
        ("Hardcover Dotted Journal", "Office Supplies", 14.99, 5.00, 200),
        
        # Apparel
        ("Classic Leather Jacket", "Apparel", 199.99, 110.00, 45),
        ("All-Weather Running Shoes", "Apparel", 119.99, 68.00, 85),
        ("Travel Backpack 40L", "Apparel", 79.99, 42.00, 95)
    ]
    
    cursor.executemany(
        "INSERT INTO products (product_name, category, price, cost, stock_quantity) VALUES (?, ?, ?, ?, ?);",
        products_data
    )
    conn.commit()
    print(f"Inserted {len(products_data)} products.")

    # 2. Populate Customers Table
    first_names = [
        "Liam", "Noah", "Oliver", "Elijah", "William", "James", "Benjamin", "Lucas", "Henry", "Alexander",
        "Olivia", "Emma", "Charlotte", "Amelia", "Sophia", "Isabella", "Ava", "Mia", "Evelyn", "Harper",
        "Ethan", "Mason", "Michael", "Daniel", "Jacob", "Logan", "Jackson", "Levi", "Sebastian", "Jack",
        "Emily", "Elizabeth", "Sofia", "Avery", "Ella", "Scarlett", "Grace", "Chloe", "Victoria", "Madison"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
        "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin",
        "Lee", "Perez", "Thompson", "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson",
        "Walker", "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores"
    ]
    
    cities_states = [
        ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"), 
        ("Phoenix", "AZ"), ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"), 
        ("Dallas", "TX"), ("San Jose", "CA"), ("Austin", "TX"), ("Jacksonville", "FL"), 
        ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"), ("San Francisco", "CA"), 
        ("Indianapolis", "IN"), ("Seattle", "WA"), ("Denver", "CO"), ("Boston", "MA")
    ]
    
    customers = []
    emails_used = set()
    
    # Let's generate 120 customers
    start_date = datetime(2025, 1, 1)
    for i in range(120):
        first = random.choice(first_names)
        last = random.choice(last_names)
        
        # Ensure unique email
        email = f"{first.lower()}.{last.lower()}{random.randint(10, 99)}@example.com"
        while email in emails_used:
            email = f"{first.lower()}.{last.lower()}{random.randint(100, 999)}@example.com"
        emails_used.add(email)
        
        phone = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
        city, state = random.choice(cities_states)
        
        # Join date between Jan 1, 2025 and June 30, 2026
        days_offset = random.randint(0, 545)
        join_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        
        customers.append((first, last, email, phone, city, state, join_date))
        
    cursor.executemany(
        "INSERT INTO customers (first_name, last_name, email, phone, city, state, join_date) VALUES (?, ?, ?, ?, ?, ?, ?);",
        customers
    )
    conn.commit()
    print(f"Inserted {len(customers)} customers.")

    # Fetch products to reference their prices and costs
    cursor.execute("SELECT product_id, price, cost FROM products;")
    products_db = cursor.fetchall()
    
    # Fetch customer IDs and join dates to ensure order date is after join date
    cursor.execute("SELECT customer_id, join_date FROM customers;")
    customers_db = cursor.fetchall()

    # 3. Populate Orders, Order Items, and Payments Tables
    # We will generate ~600 orders from July 2025 to July 2026
    orders_inserted = 0
    order_items_inserted = 0
    payments_inserted = 0
    
    order_statuses = ['Delivered', 'Delivered', 'Delivered', 'Shipped', 'Pending', 'Cancelled']
    payment_methods = ['Credit Card', 'Debit Card', 'UPI', 'PayPal', 'Net Banking']
    
    for _ in range(600):
        cust_id, join_date_str = random.choice(customers_db)
        join_date = datetime.strptime(join_date_str, "%Y-%m-%d")
        
        # Order date must be after customer join date, up to July 10, 2026
        max_order_date = datetime(2026, 7, 10)
        if join_date >= max_order_date:
            continue
            
        days_between = (max_order_date - join_date).days
        order_days_offset = random.randint(0, days_between)
        order_date_dt = join_date + timedelta(days=order_days_offset)
        order_date = order_date_dt.strftime("%Y-%m-%d")
        
        status = random.choice(order_statuses)
        
        # Create order with dummy total_amount (we will update it after inserting items)
        cursor.execute(
            "INSERT INTO orders (customer_id, order_date, status, total_amount) VALUES (?, ?, ?, 0.0);",
            (cust_id, order_date, status)
        )
        order_id = cursor.lastrowid
        orders_inserted += 1
        
        # Generate 1 to 4 items for this order
        num_items = random.randint(1, 4)
        chosen_products = random.sample(products_db, num_items)
        
        order_total = 0.0
        for prod in chosen_products:
            prod_id, prod_price, prod_cost = prod
            quantity = random.randint(1, 3)
            item_total = prod_price * quantity
            order_total += item_total
            
            cursor.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?);",
                (order_id, prod_id, quantity, prod_price)
            )
            order_items_inserted += 1
            
        # Update total amount in orders table
        cursor.execute(
            "UPDATE orders SET total_amount = ? WHERE order_id = ?;",
            (round(order_total, 2), order_id)
        )
        
        # Create payment record (unless status is Pending or Cancelled, then maybe no payment)
        if status in ['Delivered', 'Shipped']:
            pay_method = random.choice(payment_methods)
            # Payment date is usually the same day or 1 day after order
            pay_days_offset = random.randint(0, 1)
            pay_date = (order_date_dt + timedelta(days=pay_days_offset)).strftime("%Y-%m-%d")
            
            cursor.execute(
                "INSERT INTO payments (order_id, payment_date, payment_method, payment_amount) VALUES (?, ?, ?, ?);",
                (order_id, pay_date, pay_method, round(order_total, 2))
            )
            payments_inserted += 1
        elif status == 'Pending' and random.random() > 0.5:
            # 50% of pending orders are pre-paid
            pay_method = random.choice(payment_methods)
            cursor.execute(
                "INSERT INTO payments (order_id, payment_date, payment_method, payment_amount) VALUES (?, ?, ?, ?);",
                (order_id, order_date, pay_method, round(order_total, 2))
            )
            payments_inserted += 1
            
    conn.commit()
    conn.close()
    
    print(f"Data Generation Successful:")
    print(f" - Orders created: {orders_inserted}")
    print(f" - Order Items created: {order_items_inserted}")
    print(f" - Payments logged: {payments_inserted}")

if __name__ == '__main__':
    generate_mock_data()
