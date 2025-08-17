dag.py
import pandas as pd
import mysql.connector

def transform_load():
    df = pd.read_csv("C://Users/abhis/Downloads\data/transactions.csv")

    df = df.dropna(subset=["bank_id", "amount", "date"])
    df["bank_id"] = df["bank_id"].astype(str)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["amount", "date"])

    result = df.groupby([df["date"].dt.date, "bank_id"])["amount"].sum().reset_index()
    result.columns = ["date", "bank_id", "total_amount"]

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="testdb"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS daily_transactions (date DATE, bank_id VARCHAR(255), total_amount DOUBLE)")
    cursor.execute("TRUNCATE TABLE daily_transactions")
    for _, row in result.iterrows():
        cursor.execute(
            "INSERT INTO daily_transactions (date, bank_id, total_amount) VALUES (%s, %s, %s)",
            (row["date"], row["bank_id"], row["total_amount"])
        )
    conn.commit()
    cursor.close()
    conn.close()
