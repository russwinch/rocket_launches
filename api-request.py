"""
Retrieves data from the LL API and processes the result.
"""

import requests


def request_launches(total=5):
    url = f"https://launchlibrary.net/1.4/launch?mode=verbose&next={total}"
    data = requests.get(url, timeout=5)
    return data.json()


def get_launches():
    data_dict = request_launches()
    launches = [Launch(l) for l in data_dict['launches']]

    for k, l in enumerate(launches):
        print(k, l.name, l.location, l.t0, l.status_desc, l.rocket_img)
        print('----------')


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
        self.id = data['id']
        self.name = data['name']
        self.location = data['location']['name']
        self.t0 = data['net']
        image = data['rocket']['imageURL']
        if 'placeholder' in image:
            image = None
        self.rocket_img = image
        self.status_code = data['status']  # (1 Green, 2 Red, 3 Success, 4 Failed)
        self.status_desc = self._status_decoder(self.status_code)
        self.hold_reason = data['holdreason']
        self.fail_reason = data['failreason']


if __name__ == '__main__':
    get_launches()
