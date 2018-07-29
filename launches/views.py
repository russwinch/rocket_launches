import logging
from flask import render_template

from . import api_request


def index():
    return("index is working")


def upcoming_launch(key):
    logging.debug(key)
    key = int(key)
    launches = api_request.get_launches()
    launch = launches[key]
    prev_launch, next_launch = key - 1, key + 1
    if prev_launch < 0:
        prev_launch = len(launches) - 1
    if next_launch > len(launches) - 1:
        next_launch = 0
    launch.context['next'] = next_launch
    launch.context['prev'] = prev_launch
    return render_template("launch.html", **launch.context)


def launch_map():
    return render_template("map.html")
