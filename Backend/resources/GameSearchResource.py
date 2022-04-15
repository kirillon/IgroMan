from models import Game
from flask_restful import Resource
from serializers import GamesSchema
from flask import request


class GameSearchResource(Resource):

    def get(self):
        search = request.args['search']
        games = Game.query.filter(Game.title.ilike(f"%{search}%")).all()

        games_shema = GamesSchema(many=True)
        return {"success": True, "data": games_shema.dump(games)}, 200
