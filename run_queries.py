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
