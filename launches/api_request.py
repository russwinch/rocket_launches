"""
Retrieves and processes data from the Launch Library API.
"""
import datetime
from flask import current_app as app
import json
import logging
import os
import re
import requests
from requests.exceptions import ReadTimeout, ConnectionError, HTTPError
import time

import launches.image_scrape as image_scrape


def request_launches(total=8):
    """
    Makes a request to the Launch Library API.
    Returns a dictionary.

    :total: the number of launches to retrieve
    """
    url = f"https://launchlibrary.net/1.4/launch?mode=verbose&next={total}"
    try:
        data = requests.get(url, timeout=5)
        logging.info('requested data')
    except Exception:
        # catch timeout etc here
        pass
    logging.debug(f"JSON: {json.dumps(data.json(), indent=2)}")
    return data.json()


def get_launches():
    """
    Wrapper for the LL request and creation of Launch objects.
    Returns a list of Launch objects.
    """
    data_dict = request_launches()
    launches = [Launch(l) for l in data_dict['launches']]

    logging.debug(f"Generated context: {[launch.context for launch in launches]}")
    return launches


class Launch(object):
    """
    Contains all useful data about a launch within the context dicionary.
    """
    @staticmethod
    def _status_decoder(status_int):
        """Decodes status codes into strings"""
        status_dict = {1: 'Green',
                       2: 'Red',
                       3: 'Success',
                       4: 'Failed'
                       }
        return status_dict[status_int]

    @staticmethod
    def _rocket_img_url(rocket_name):
        """
        Supplies a url for the image of a rocket.
        This will be the local path; if it's not found there an attempt will be made
        to scrape Google image search.

        :rocket_name: the name of the rocket, as supplied by the Launch Library API
        """
        static_path = f"{app.static_folder}/rocket_images/{rocket_name}.jpg"
        if not os.access(static_path, os.R_OK):
            # scrape the image from google if it doesn't exist in the static folder
            image_scrape.get_rocket_img(rocket_name, static_path)
        return f"{app.static_url_path}/rocket_images/{rocket_name}.jpg"

    def __init__(self, data):
        self.context = {
            'id': data['id'],
            'name': data['name'],
            'location': data['location']['name'],
            'pad_latitude': data['location']['pads'][0]['latitude'],
            'pad_longitude': data['location']['pads'][0]['longitude'],
            'pad_name': data['location']['pads'][0]['name'],
            'status_code': data['status'],  # (1 Green, 2 Red, 3 Success, 4 Failed)
            'status_desc': self._status_decoder(data['status']),
            'hold_reason': data['holdreason'],
            'fail_reason': data['failreason'],
            'rocket_name': data['rocket']['name'],
            'utc_t0': data['net'],
            'tbd_date': data['tbddate'],
            'tbd_time': data['tbdtime']
        }

        utc_launch_time = datetime.datetime.strptime(f"{data['isonet']}+0000",
                                                     "%Y%m%dT%H%M%SZ%z")
        launch_timestamp = utc_launch_time.timestamp()
        local_launch_time = time.localtime(launch_timestamp)
        self.context['t0_timestamp'] = launch_timestamp
        self.context['t0_local'] = time.strftime("%a %d %b %y %H:%M %Z",
                                                 local_launch_time)
        self.context['t0_month'] = time.strftime("%b", local_launch_time)

        image = data['rocket']['imageURL']

        if 'placeholder' in image:
            try:
                image = self._rocket_img_url(self.context['rocket_name'])
            except (TypeError, ConnectionError, ReadTimeout, HTTPError) as e:
                # just use the placeholder for now and try again next time
                logging.exception(e)
        else:
            # get the smallest image possible
            smallest_image = data['rocket']['imageSizes'][0]
            image_re = re.compile(r'(.*_)\d*(.jpg)$')
            image = image_re.sub(r'\g<1>'+str(smallest_image)+r'\g<2>', image)
        self.context['rocket_img'] = image

        missions = []
        for k, m in enumerate(data['missions']):
            missions.append({'mission_key': k,
                             'mission_name': m['name'],
                             'mission_desc': m['description'],
                             'mission_type': m['typeName']
                             })
        self.context['missions'] = missions


if __name__ == '__main__':
    get_launches()
