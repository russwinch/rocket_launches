from flask import Flask
import logging
from logging.handlers import RotatingFileHandler

from . import views


def create_app():
    log_stream_handler = logging.StreamHandler()
    log_file_handler = RotatingFileHandler('logs/launch_api.log',
                                           maxBytes=10485760,  # 10MB
                                           backupCount=2)
    logging.basicConfig(handlers=(log_stream_handler, log_file_handler),
                        # level=logging.INFO,
                        level=logging.DEBUG,
                        format="%(asctime)s:%(levelname)s:%(module)s%(message)s")

    app = Flask(__name__)

    app.add_url_rule('/', 'index', views.index)
    app.add_url_rule('/launch/<int:key>', 'upcoming_launch', views.upcoming_launch)
    app.add_url_rule('/map', 'launch_map', views.launch_map)
    app.add_url_rule('/launch/<int:key>/mission/<int:mkey>', 'mission_details', views.mission_details)

    return app
