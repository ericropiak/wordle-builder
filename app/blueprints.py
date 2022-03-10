from app.main import app
from app.views import main, subpage

app.register_blueprint(main)
app.register_blueprint(subpage, url_prefix='/subpage')
