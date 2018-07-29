"""
Retrieves data from the LL API and processes the result.
"""

import logging
import requests


def request_launches(total=5):
    url = f"https://launchlibrary.net/1.4/launch?mode=verbose&next={total}"
    try:
        data = requests.get(url, timeout=5)
        logging.info('requested data')
    except Exception:
        # catch timeout etc here
        pass
    return data.json()


def get_launches():
    data_dict = request_launches()
    launches = [Launch(l) for l in data_dict['launches']]

    # for k, l in enumerate(launches):
    #     logging.debug(k, l.name, l.location, l.t0, l.status_desc, l.rocket_img)

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
                       4: 'Failed'}
        return status_dict[status_int]

    def __init__(self, data):
        self.context = {}
        self.context['id'] = data['id']
        self.context['name'] = data['name']
        self.context['location'] = data['location']['name']
        self.context['pad_latitude'] = data['location']['pads'][0]['latitude']
        self.context['pad_longitude'] = data['location']['pads'][0]['longitude']
        self.context['t0'] = data['net']

        self.context['rocket_name'] = data['rocket']['name']
        image = data['rocket']['imageURL']
        if 'placeholder' in image:
            image = None
        self.context['rocket_img'] = image

        self.context['missions'] = [data['missions'][m]['name'] for m, _ in
                enumerate(data['missions'])]
        self.context['status_code'] = data['status']  # (1 Green, 2 Red, 3 Success, 4 Failed)
        self.context['status_desc'] = self._status_decoder(self.context['status_code'])
        self.context['hold_reason'] = data['holdreason']
        self.context['fail_reason'] = data['failreason']


if __name__ == '__main__':
    get_launches()
