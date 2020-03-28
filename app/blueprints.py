from app.main import app
from app.views import main, salad_bowl

app.register_blueprint(main)
app.register_blueprint(salad_bowl, url_prefix='/yummy')