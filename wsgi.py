from app import create_app

# Initialize the app with PostgreSQL status check disabled for Heroku
app = create_app(check_postgres_status=False)
