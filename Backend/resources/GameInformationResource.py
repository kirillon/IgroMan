import requests
from flask_restful import Resource
from models import Game
from serializers import GamesSchema


# ресурс для передачи боту информации об игре
class GameInformationResource(Resource):

    def get(self, app_id):
        game = Game().query.filter_by(steam_id=app_id).first_or_404()
        games_shema = GamesSchema()
        request_options = \
            requests.get(f"https://store.steampowered.com/api/appdetails?appids={app_id}").json()[str(app_id)]["data"]

        options = {"detailed_description": request_options['detailed_description'],
                   "header_image": request_options['header_image']}

        return {"success": True,
                "data": games_shema.dump(game),
                "options": options}, 200
