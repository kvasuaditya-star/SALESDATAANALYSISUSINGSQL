import os
import sqlite3

def run_analysis():
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'sales_data.db')
    queries_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'queries', 'business_analysis.sql')
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    report_file_path = os.path.join(reports_dir, 'analysis_report.md')
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(queries_path, 'r') as f:
        sql_content = f.read()
        
    # Split queries by semicolon, filtering out empty blocks
    raw_queries = sql_content.split(';')
    queries = []
    
    current_comment = ""
    for q in raw_queries:
        q_strip = q.strip()
        if not q_strip:
            continue
        queries.append(q_strip)

    print("Running business analysis SQL queries and generating report...")
    
    query_sections = [
        ("Monthly Revenue Trends", ["Month", "Total Orders", "Total Revenue ($)"]),
        ("Top-Selling Products by Quantity", ["Product ID", "Product Name", "Category", "Quantity Sold"]),
        ("Top-Selling Products by Revenue", ["Product ID", "Product Name", "Category", "Quantity Sold", "Total Revenue ($)"]),
        ("Profit Margins by Product Category", ["Category", "Total Revenue ($)", "Total Cost ($)", "Total Profit ($)", "Profit Margin (%)"])
    ]
    
    markdown_content = "# Sales Data Analysis - Core Insights Report\n\n"
    markdown_content += "This report compiles the outputs of SQL analytical queries executed against the sales database.\n\n"
    
    for idx, (title, headers) in enumerate(query_sections):
        if idx >= len(queries):
            break
            
        sql = queries[idx]
        cursor.execute(sql)
        rows = cursor.fetchall()
        
        print(f" -> Executing: {title}")
        
        # Add to Markdown Report
        markdown_content += f"## {idx + 1}. {title}\n\n"
        
        # Markdown table headers
        markdown_content += "| " + " | ".join(headers) + " |\n"
        markdown_content += "| " + " | ".join(["---"] * len(headers)) + " |\n"
        
        for row in rows:
            formatted_row = []
            for val in row:
                if isinstance(val, float):
                    formatted_row.append(f"{val:,.2f}")
                else:
                    formatted_row.append(str(val))
            markdown_content += "| " + " | ".join(formatted_row) + " |\n"
        
        markdown_content += "\n"
        
    with open(report_file_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
        
    conn.close()
    print(f"\nAnalysis complete! Report successfully generated at: {report_file_path}")

if __name__ == '__main__':
    run_analysis()
