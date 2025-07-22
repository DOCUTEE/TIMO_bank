from sqlalchemy import create_engine, text

def check_foreign_keys_customer_identity(engine: create_engine):
    """Check foreign keys in customer_identity.customer_id."""
    print("\n=== FOREIGN KEY CHECK: customer_identity.customer_id → customer.customer_id ===")

    conn = engine.connect()

    query = text("""
        SELECT customer_id
        FROM customer
        WHERE customer_id NOT IN (
            SELECT customer_id FROM customer_identity
        )
    """)
    results = conn.execute(query).fetchall()
    if results:
        print(f"Found {len(results)} orphaned customer rows:")
        for row in results:
            print(f"  customer_id: {row.customer_id} does not exist in customer_identity table")
    else:
        print("All foreign keys are valid.")