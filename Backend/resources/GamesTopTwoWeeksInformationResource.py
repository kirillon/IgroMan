import random

from flask import request

from models import Game
from flask_restful import Resource
from serializers import GamesSchema
import requests


class GamesTopTwoWeeksInformationResource(Resource):

    def get(self):
        top_game_information = []
        top_2weeks_request = list(requests.get("https://steamspy.com/api.php?request=top100in2weeks").json())
        limit = request.args.get('limit', default=10, type=int)
        # top_2weeks_request = random.sample(top_2weeks_request, limit)
        top_2weeks_request = top_2weeks_request[:limit]

        # top_game_information = Game.query.filter(Game.steam_id.in_(top_forever_request)).all()
        games_shema = GamesSchema()
        for app_id in top_2weeks_request:
            try:
                top_game_information.append(games_shema.dump(Game().query.filter_by(steam_id=app_id).first_or_404()))
            except:
                print(app_id)
                continue

        return {"success": True, "data": top_game_information}, 200
