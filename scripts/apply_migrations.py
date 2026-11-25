"""
Apply versioned SQL migrations in database/migrations/ against Supabase PostgreSQL.
Requires DATABASE_URL in backend/.env.
"""

import os
import sys
import glob
from dotenv import load_dotenv
import psycopg

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(PROJECT_ROOT, "backend", ".env")
MIGRATIONS_DIR = os.path.join(PROJECT_ROOT, "database", "migrations")


def normalize_psycopg_url(url: str) -> str:
    if url.startswith("postgresql+psycopg://"):
        return "postgresql://" + url[len("postgresql+psycopg://"):]
    if url.startswith("postgresql+psycopg2://"):
        return "postgresql://" + url[len("postgresql+psycopg2://"):]
    return url


def main():
    load_dotenv(ENV_PATH)
    raw_url = os.getenv("DATABASE_URL", "").strip()
    if not raw_url:
        print("ERROR: DATABASE_URL is not set in backend/.env. Please configure it first.")
        sys.exit(1)

    conn_url = normalize_psycopg_url(raw_url)
    migration_files = sorted(glob.glob(os.path.join(MIGRATIONS_DIR, "*.sql")))
    if not migration_files:
        print("ERROR: No SQL migration files found in database/migrations/")
        sys.exit(1)

    print(f"Found {len(migration_files)} migration(s) in {MIGRATIONS_DIR}")
    with psycopg.connect(conn_url, autocommit=False) as conn:
        with conn.cursor() as cur:
            for path in migration_files:
                fname = os.path.basename(path)
                print(f"Applying {fname} ...")
                with open(path, "r", encoding="utf-8") as f:
                    sql = f.read()
                cur.execute(sql)
                conn.commit()
                print(f"  OK: {fname}")

            cur.execute("SELECT extensions.PostGIS_Version();")
            pgis_ver = cur.fetchone()[0]
            print(f"\nPostGIS active: {pgis_ver}")


if __name__ == "__main__":
    main()
