from sqlalchemy import inspect, text, create_engine

def check_nulls(engine : create_engine):
    """Check for null values in critical columns."""
    conn = engine.connect()
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    for table in tables:
        columns = inspector.get_columns(table)
        for column in columns:
            if column['nullable'] is False:
                query = text(f"SELECT COUNT(*) FROM {table} WHERE {column['name']} IS NULL")
                result = conn.execute(query).scalar()
                if result > 0:
                    print(f"Table {table} has {result} null values in column {column['name']}.")