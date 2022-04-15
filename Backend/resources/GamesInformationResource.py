from models import Game
from flask_restful import Resource
from serializers import GamesSchema


class GamesInformationResource(Resource):

    def get(self):
        games = Game.query.all()
        games_shema = GamesSchema(many=True)
        return {"success": True, "data": games_shema.dump(games)}, 200
