import os
import sqlite3

def run_audit():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sales_data.db')
    audit_sql_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts', 'data_quality.sql')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(audit_sql_path, 'r') as f:
        queries = f.read().split(';')
        
    print("==================================================")
    print("          DATABASE DATA QUALITY AUDIT             ")
    print("==================================================")
    
    query_titles = [
        "1. Duplicate Emails check",
        "2. Duplicate Names check (Potential duplicate accounts)",
        "3. Orphan Orders check (Missing customer mappings)",
        "4. Orphan Order Items check (Missing order/product mappings)",
        "5. Price Discrepancies check (Items price vs catalog price)",
        "6. Order Total Discrepancies check (Items total vs order sum)",
        "7. Temporal Order-Join anomalies (Order date < Join date)",
        "8. Temporal Payment-Order anomalies (Payment date < Order date)",
        "9. Duplicate Payments check"
    ]
    
    anomalies_found = False
    
    for title, query in zip(query_titles, queries):
        clean_query = query.strip()
        if not clean_query:
            continue
            
        print(f"\nRunning: {title}...")
        cursor.execute(clean_query)
        results = cursor.fetchall()
        
        if results:
            anomalies_found = True
            print(f"WARNING: ANOMALIES FOUND! Count: {len(results)}")
            # print up to 5 examples
            for row in results[:5]:
                print(f"   - {row}")
            if len(results) > 5:
                print(f"   ... and {len(results) - 5} more.")
        else:
            print("PASSED: No issues detected.")
            
    print("\n==================================================")
    if anomalies_found:
        print("Audit Complete: Some anomalies were detected.")
    else:
        print("Audit Complete: DATABASE IS 100% HEALTHY & CLEAN!")
    print("==================================================")
    
    conn.close()

if __name__ == '__main__':
    run_audit()
