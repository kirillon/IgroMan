from flask_marshmallow import Marshmallow

from models import Game

ma = Marshmallow()


class GamesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        include_fk = True
