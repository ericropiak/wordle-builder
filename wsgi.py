from app.main import app as application

# Used to serve application with gunicorn
if __name__ == "__main__":
    application.run()