from app.main import app
from app.views import ct_conomy, main, salad_bowl

app.register_blueprint(main)
app.register_blueprint(ct_conomy, url_prefix='/ct_conomy')
app.register_blueprint(salad_bowl, url_prefix='/yummy')