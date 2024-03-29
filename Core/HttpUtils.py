import urllib3


class HttpUtils(object):
    def __init__(self, base_url: str = ''):
        self.base_url = base_url
        self.client = urllib3.PoolManager()

    def get(self, url: str):
        response = self.client.request('GET', self.base_url + url)
        if response.status == 200:
            return response.data

    def return_fleet(self, fleet_id: str):
        return self.get(
            f'/game/index.php?page=ingame&component=movement&return={fleet_id}'
        )
