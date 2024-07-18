import os
import subprocess
import psycopg2
import sys

# Ensure the root directory is in the Python path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config_private import PostgresConfig

"""
manage_db.py

This script is used to manage database setups for the Make-Life app. It supports both SQLite (for development)
and PostgreSQL (for testing and production). The script initializes the database migrations, creates an initial 
migration, and applies the migration to the database.

Usage:
    python utilities/manage_db.py [sqlite|postgres]

Arguments:
    sqlite  - Sets up the SQLite database.
    postgres - Sets up the PostgreSQL database.
"""

def run_command(command):
    """Utility function to run a system command."""
    print(f"Running: {command}")  # Added debug print
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Command failed with return code {result.returncode}")
    return result

def setup_sqlite():
    """Set up SQLite database."""
    print("Setting up SQLite database...")
    if not os.path.exists('migrations'):
        run_command('flask db init')
    else:
        print("Migrations already initialized. Skipping init step.")
    run_command('flask db migrate -m "Initial migration"')
    run_command('flask db upgrade')

def grant_postgres_privileges(dbname):
    """Grant necessary privileges to the PostgreSQL user."""
    try:
        conn = psycopg2.connect(
            dbname=dbname,
            user=PostgresConfig.POSTGRES_USER,
            password=PostgresConfig.POSTGRES_PASSWORD,
            host="localhost"
        )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute("GRANT USAGE ON SCHEMA public TO vadim;")
        cur.execute("GRANT CREATE ON SCHEMA public TO vadim;")
        cur.execute("GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO vadim;")
        cur.execute("GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO vadim;")
        cur.execute("GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO vadim;")
        cur.execute("ALTER USER vadim CREATEDB;")
        conn.commit()
        print("Privileges granted to user 'vadim'.")

        # Confirm privileges
        cur.execute("SELECT * FROM information_schema.role_table_grants WHERE grantee = 'vadim';")
        print("Granted table privileges:")
        for row in cur.fetchall():
            print(row)

        cur.close()
        conn.close()
    except psycopg2.ProgrammingError as e:
        print(f"Error granting privileges: {e}")

def check_postgres_db():
    """Check if PostgreSQL database exists and create it if it doesn't."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=PostgresConfig.POSTGRES_USER,
            password=PostgresConfig.POSTGRES_PASSWORD,
            host="localhost"
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = 'makelife_db'")
        exists = cur.fetchone()
        if not exists:
            cur.execute("CREATE DATABASE makelife_db OWNER vadim")
            print("Database 'makelife_db' created.")
        else:
            print("Database 'makelife_db' already exists.")

        cur.close()
        conn.close()

        # Grant privileges explicitly on the makelife_db
        grant_postgres_privileges("makelife_db")
    except psycopg2.OperationalError as e:
        print(f"Error checking/creating PostgreSQL database: {e}")
        print("Please ensure the credentials in config_private.py are correct.")
    except psycopg2.ProgrammingError as e:
        print(f"Error during PostgreSQL operations: {e}")

def setup_postgres():
    """Set up PostgreSQL database."""
    print("Setting up PostgreSQL database...")
    check_postgres_db()
    os.environ['FLASK_CONFIG'] = 'config.PostgresConfig'
    print(f"FLASK_CONFIG set to: {os.environ.get('FLASK_CONFIG')}")
    if not os.path.exists('migrations'):
        run_command('flask db init')
    else:
        print("Migrations already initialized. Skipping init step.")
    run_command('flask db migrate -m "Initial migration"')
    run_command('flask db upgrade')

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python utilities/manage_db.py [sqlite|postgres]")
        sys.exit(1)
    
    db_type = sys.argv[1].lower()
    if db_type == 'sqlite':
        setup_sqlite()
    elif db_type == 'postgres':
        setup_postgres()
    else:
        print("Invalid argument. Use 'sqlite' or 'postgres'.")
        sys.exit(1)
