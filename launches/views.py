"""
Views for the routes.
Most logic is held in the imported files.
"""
import logging
from flask import render_template

from . import api_request


def index():
    """TBC page which will need forwarding onto the first launch."""
    return("index is working")


def upcoming_launch(key):
    """
    Shows details of each launch. The main page.

    :key: index of the launch within the list of Launch objects
    """
    logging.debug(key)
    try:
        launches = api_request.get_launches()
        context = launches[key]
    except Exception as e:
        # TODO: more error catching here
        raise e
    prev_launch, next_launch = key - 1, key + 1
    if prev_launch < 0:
        prev_launch = len(launches) - 1
    if next_launch > len(launches) - 1:
        next_launch = 0
    context['next'] = next_launch
    context['prev'] = prev_launch
    return render_template("launch.html", key=key, **context)


def mission_details(key, mkey):
    """
    Details of the mission. Linked from the launch page.

    :key: index of the launch within the list of Launch objects
    :mkey: index of the mission for that launch (there can be several)
    """
    try:
        launches = api_request.get_launches()
    except Exception:
        # more error catching here
        pass
    launch = launches[key]
    context = launch['missions'][mkey]
    return render_template("mission.html", key=key, **context)


def launch_map(key):
    """
    Displays a full screen map of the launch site. Linked from the launch page.

    :key: index of the launch within the list of Launch objects
    """
    try:
        launches = api_request.get_launches()
    except Exception:
        # more error catching here
        pass
    launch = launches[key]
    context = {
        'pad_latitude': launch['pad_latitude'],
        'pad_longitude': launch['pad_longitude'],
        'pad_name': launch['pad_name']
    }
    return render_template("map.html", key=key, **context)
