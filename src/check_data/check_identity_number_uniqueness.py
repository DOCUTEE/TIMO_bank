from sqlalchemy import create_engine, inspect, text

def check_identity_number_uniqueness(engine: create_engine):
    """Check uniqueness of national_id in Customer table."""
    conn = engine.connect()
    query = text("""
        SELECT identity_number, COUNT(*) as count
        FROM customer_identity
        WHERE identity_type = 'national_id'
        GROUP BY identity_number
        HAVING COUNT(*) > 1
    """)
    results = conn.execute(query).fetchall()

    if results:
        print("National ID duplicates found:")
        for row in results:
            print(f"  National ID {row[0]} appears {row[1]} times")
    else:
        print("All National IDs are unique.")