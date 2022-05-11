from flask import Blueprint

from flask_restful import Api
from resources.GameInformationResource import GameInformationResource
from resources.GamesInformationResource import GamesInformationResource
from resources.GameSearchResource import GameSearchResource
from resources.GamesTopForeverInformationResource import GamesTopForeverInformationResource
from resources.GamesTopTwoWeeksInformationResource import GamesTopTwoWeeksInformationResource

blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

# добавление ресурсов
api.add_resource(GameInformationResource, "/getGames/<app_id>")
api.add_resource(GamesInformationResource, "/getGames")
api.add_resource(GameSearchResource, "/searchGames/")
api.add_resource(GamesTopForeverInformationResource, "/topForeverGames/")
api.add_resource(GamesTopTwoWeeksInformationResource, "/top2weeks")
