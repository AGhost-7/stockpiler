from .app import app
from .routes import users, locations


app.register_blueprint(users)
app.register_blueprint(locations)
