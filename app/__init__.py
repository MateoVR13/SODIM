from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
ma = Marshmallow(app)

from app.routes import prescriptions, distribution, inventory, non_pos
from app.routes.auth import bp as auth_bp

app.register_blueprint(prescriptions.bp)
app.register_blueprint(distribution.bp)
app.register_blueprint(inventory.bp)
app.register_blueprint(non_pos.bp)
app.register_blueprint(auth_bp)
