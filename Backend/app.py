from flask import Flask
from models import db
from serializers import ma
from api import blueprint

# создание app и получение config
app = Flask(__name__, )
app.config.from_object('config.Config')
app.register_blueprint(blueprint)
db.init_app(app)
ma.init_app(app)

if __name__ == '__main__':
    app.run()
