from sqlalchemy import text, create_engine

def check_foreign_keys_transaction_log_account(engine: create_engine):
    print("\n=== FOREIGN KEY CHECK: transaction_log.account_id → account.account_id ===")

    conn = engine.connect()

    query = text("""
        SELECT transaction_id, account_id
        FROM transaction_log
        WHERE account_id NOT IN (
            SELECT account_id FROM account
        )
    """)
    results = conn.execute(query).fetchall()
    if results:
        print(f"Found {len(results)} orphaned transaction rows:")
        for row in results:
            print(f"  transaction_id: {row.transaction_id}, invalid account_id: {row.account_id}")
    else:
        print("All foreign keys are valid.")
