from sqlalchemy import text, create_engine

def check_foreign_keys_account_customer(engine: create_engine):
    print("\n=== FOREIGN KEY CHECK: account.customer_id → customer.customer_id ===")

    conn = engine.connect()

    query = text("""
        SELECT account_id, customer_id
        FROM account
        WHERE customer_id NOT IN (
            SELECT customer_id FROM customer
        )
    """)
    results = conn.execute(query).fetchall()
    if results:
        print(f"Found {len(results)} orphaned account rows:")
        for row in results:
            print(f"  account_id: {row.account_id}, invalid customer_id: {row.customer_id}")
    else:
        print("All foreign keys are valid.")
