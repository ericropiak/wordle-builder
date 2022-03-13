from app.main import app
from app.views import guessing_game, main

app.register_blueprint(main)
app.register_blueprint(guessing_game, url_prefix='/guessing_game')
