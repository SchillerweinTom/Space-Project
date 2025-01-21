import os
from flask import Flask
from blueprints.api import app as api_app
from blueprints.web import app as web_app
from models.conn import db
from dotenv import load_dotenv
from flask_migrate import Migrate
from models.models import init_db
from flask_cors import CORS
load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', "terces")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', "")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', "False")

app.register_blueprint(web_app, url_prefix="/")
app.register_blueprint(api_app, url_prefix="/api")

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True)