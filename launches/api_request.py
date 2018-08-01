"""
Retrieves data from the LL API and processes the result.
"""
import datetime
import json
import logging
import requests
import time


def request_launches(total=8):
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
    data_dict = request_launches()
    launches = [Launch(l) for l in data_dict['launches']]

    logging.debug(f"Generated context: {[launch.context for launch in launches]}")
    return launches


class Launch(object):
    """
    Contains all useful data about a launch.

    :data: dictionary containing all details of one launch
    """
    @staticmethod
    def _status_decoder(status_int):
        status_dict = {1: 'Green',
                       2: 'Red',
                       3: 'Success',
                       4: 'Failed'
                       }
        return status_dict[status_int]

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
            image = None
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
