from sqlalchemy import create_engine, text

def check_national_id_format(engine: create_engine):
    """Check format of national_id in Customer table."""
    conn = engine.connect()
    query = text("""
        SELECT identity_number
        FROM customer_identity
        WHERE identity_type = 'national_id'
        AND NOT identity_number REGEXP '^(0\d{2})([0-3])(\d{2})(\d{6})$'
    """)
    results = conn.execute(query).fetchall()

    if results:
        print("Invalid National ID formats found:")
        for row in results:
            print(f"  Invalid National ID: {row[0]}")
    else:
        print("All National IDs are in valid format.")