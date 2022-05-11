import random

from flask import request

from models import Game
from flask_restful import Resource
from serializers import GamesSchema
import requests


# список лучших игр за все время
class GamesTopForeverInformationResource(Resource):

    def get(self):
        top_game_information = []
        top_forever_request = list(requests.get("https://steamspy.com/api.php?request=top100forever").json())
        limit = request.args.get('limit', default=10, type=int)
        top_forever_request = random.sample(top_forever_request, limit)

        games_shema = GamesSchema()
        for app_id in top_forever_request:
            try:
                top_game_information.append(games_shema.dump(Game().query.filter_by(steam_id=app_id).first_or_404()))
            except:
                continue

        return {"success": True, "data": top_game_information}, 200
