from sqlalchemy import inspect, text, create_engine

def check_uniqueness(engine: create_engine):
    print("\n=== UNIQUENESS CHECK (PRIMARY KEYS) ===")
    conn = engine.connect()
    inspector = inspect(engine)
    
    for table_name in inspector.get_table_names():
        print(f"\nTable: {table_name}")
        pk_columns = inspector.get_pk_constraint(table_name).get("constrained_columns", [])
        
        if not pk_columns:
            print("  No primary key defined.")
            continue

        # Build GROUP BY clause
        pk_clause = ", ".join(pk_columns)
        query = text(f"""
            SELECT {pk_clause}, COUNT(*) as cnt
            FROM {table_name}
            GROUP BY {pk_clause}
            HAVING COUNT(*) > 1
        """)
        results = conn.execute(query).fetchall()

        if results:
            print(f"  Primary Key combination {pk_columns} has duplicates:")
            for row in results:
                pk_values = ", ".join(f"{col}={val}" for col, val in zip(pk_columns, row[:-1]))
                print(f"    {pk_values} appears {row[-1]} times")
        else:
            print(f"  Primary Key combination {pk_columns} is unique")