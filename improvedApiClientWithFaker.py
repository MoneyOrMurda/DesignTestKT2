import requests
import pprint
from faker import Faker

class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url
        self.fake = Faker()

    def _request(self, url, request_type, data=None, expected_error=False):
        try:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, json=data)
            else:
                response = requests.delete(url)

            response.raise_for_status()

            if not expected_error and response.status_code == 200:
                return response
            elif expected_error:
                return response
        except requests.RequestException as e:
            pprint.pprint(f"Request failed: {e}")
            return None

    def get(self, endpoint, endpoint_id, expected_error=False):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        return response.json() if response else None

    def post(self, endpoint, body):
        url = f'{self.base_url}/{endpoint}'
        response = self._request(url, 'POST', data=body)
        return response.json() if response else None

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        return response.json() if response else None

    def generate_random_user_data(self):
        return {
            "name": self.fake.name(),
            "username": self.fake.user_name(),
            "email": self.fake.email()
        }

BASE_URL_JSONPLACEHOLDER = 'https://jsonplaceholder.typicode.com'
base_request = BaseRequest(BASE_URL_JSONPLACEHOLDER)

random_user_data = base_request.generate_random_user_data()
response_create_user = base_request.post('users', random_user_data)

random_user_id = base_request.fake.random_int(min=1, max=10)
user_info = base_request.get('users', random_user_id)

random_user_id_to_delete = base_request.fake.random_int(min=1, max=10)
response_delete_user = base_request.delete('users', random_user_id_to_delete)

pprint.pprint(user_info)