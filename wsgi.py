from app.flask_app import app as application

# Used to serve application with gunicorn
if __name__ == "__main__":
	print('running gunic')
    application.run()