import re
import psycopg2
import random
from pathlib import Path

SQL_FILE = Path("sql/02_sample_queries.sql")

def load_queries(sql_path: Path):
    text = sql_path.read_text(encoding="utf-8")

    parts = re.split(r'(?m)^--\s*(Q\d+)\b.*$', text)
    queries = {}

    for i in range(1, len(parts), 2):
        qname = parts[i].strip()
        body = parts[i+1].strip()
        if body:
            queries[qname] = body

    return queries

def run_query(sql: str, params=None):
    conn = psycopg2.connect(
        host="localhost",
        dbname="overbooking_db",
        user="your_user",
        password="your_password"
    )
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or [])
                try:
                    rows = cur.fetchall()
                    colnames = [d[0] for d in cur.description]
                    print("Columns:", colnames)
                    for r in rows:
                        print(r)
                except psycopg2.ProgrammingError:
                    print("Query executed successfully (no result set).")
    finally:
        conn.close()

if __name__ == "__main__":
    queries = load_queries(SQL_FILE)
    print("Available queries:", sorted(queries.keys()))
    numbers = random.randint(1,21)
    q_id = "Q{}".format(numbers)

    if q_id not in queries:
        print(f"{q_id} not found in {SQL_FILE}")
    else:
        print(f"\nRunning {q_id}:\n")
        print(queries[q_id])
        print("\nResult:\n")
        run_query(queries[q_id])
