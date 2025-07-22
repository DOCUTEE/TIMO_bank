from sqlalchemy import create_engine, text

def check_foreign_keys_transaction_log_device(engine: create_engine):
    """Check foreign keys in transaction_log.device_id."""
    print("\n=== FOREIGN KEY CHECK: transaction_log.device_id → device.device_id ===")

    conn = engine.connect()

    query = text("""
        SELECT transaction_id, device_id
        FROM transaction_log
        WHERE device_id NOT IN (
            SELECT device_id FROM device
        )    
    """)

    results = conn.execute(query).fetchall()
    if results:
        print(f"Found {len(results)} orphaned transaction rows:")
        for row in results:
            print(f"  transaction_id: {row.transaction_id}, invalid device_id: {row.device_id}")
    else:
        print("All foreign keys are valid.")
    
