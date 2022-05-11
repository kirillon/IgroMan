from flask_marshmallow import Marshmallow

from models import Game

ma = Marshmallow()


# создание сериалайзера
class GamesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Game
        include_fk = True
