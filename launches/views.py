import logging
from flask import render_template

from . import api_request


def index():
    return("index is working")


def upcoming_launch(key):
    logging.debug(key)
    try:
        launches = api_request.get_launches()
        launch = launches[key]
    except Exception as e:
        raise e
        # more error catching here
        pass
    prev_launch, next_launch = key - 1, key + 1
    if prev_launch < 0:
        prev_launch = len(launches) - 1
    if next_launch > len(launches) - 1:
        next_launch = 0
    launch.context['next'] = next_launch
    launch.context['prev'] = prev_launch
    return render_template("launch.html", key=key, **launch.context)


def mission_details(key, mkey):
    try:
        launches = api_request.get_launches()
    except Exception:
        # more error catching here
        pass
    launch = launches[key]
    context = launch.context['missions'][mkey]
    return render_template("mission.html", key=key, **context)


def launch_map(key):
    try:
        launches = api_request.get_launches()
    except Exception:
        # more error catching here
        pass
    launch = launches[key]
    context = {
        'latitude': launch.context['pad_latitude'],
        'longitude': launch.context['pad_longitude'],
        'pad_name': launch.context['pad_name']
    }
    return render_template("map.html", key=key, **context)
