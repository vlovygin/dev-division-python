import json
import logging
from urllib.parse import urljoin

import allure
import requests
from requests_toolbelt.utils import dump

from models.user import User

logger = logging.getLogger("test")


class BaseApiClient:
    """ Base class for API clients """

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.session()
        self.logger = logger

    def get(self, path, *args, **kwargs):
        return self.request(method="GET", path=path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.request(method="POST", path=path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        return self.request(method="PUT", path=path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self.request(method="DELETE", path=path, *args, **kwargs)

    def request(self, method: str, path: str, *args, **kwargs):
        """ Request method for URLs based on base_url """

        base_url = self.base_url if self.base_url.endswith("/") else f"{self.base_url}/"
        path = path if not path.startswith("/") else path.removeprefix("/")
        url = urljoin(base_url, path)
        response = self._request(method, url, *args, **kwargs)

        return response

    @staticmethod
    def _logging_pre(prepared: requests.PreparedRequest):
        body = prepared.body
        headers = dict(prepared.headers)

        if headers.get("Content-Type") == "application/json":
            body = json.loads(body)
        elif isinstance(body, bytes) and hasattr(body, "decode"):
            body = str(body)

        data = {
            "method": prepared.method,
            "url": prepared.url,
            "headers": headers,
            "body": body
        }

        allure.attach(json.dumps(data, indent=2), "Performing request", attachment_type=allure.attachment_type.JSON)
        logger.info(f"Performing request: {data}")

    def _request(self, method: str, url: str, allow_redirects=True, timeout=None, *args, **kwargs):
        """ Base request method """

        req = requests.Request(method, url, *args, **kwargs)
        prepped = self.session.prepare_request(req)
        self._logging_pre(prepped)

        response = self.session.send(prepped, allow_redirects=allow_redirects, timeout=timeout)

        data = dump.dump_all(response)
        allure.attach(data, f"Request dump", attachment_type=allure.attachment_type.JSON)
        logger.info(f"Request dump: {data}")

        return response


class MyAppApiClient(BaseApiClient):
    """ MyApp API client """

    def login(self, username: str, password: str):
        """ Log in to application """

        path = "/login"
        payload = {"username": username, "password": password}
        return self.post(path, data=payload)

    def add_user(self, user: User):
        """ Add new user """

        path = "/api/user"
        payload = user.to_dict()
        return self.post(path, json=payload)

    def delete_user(self, username: str):
        """ Delete user """

        path = f"/api/user/{username}"
        return self.delete(path)

    def change_user_password(self, username: str, password):
        """ Change user password """

        path = f"/api/user/{username}/change-password"
        payload = {"password": password}
        return self.put(path, json=payload)

    def block_user(self, username: str):
        """ Block user """

        path = f"/api/user/{username}/block"
        return self.post(path)

    def accept_user(self, username: str):
        """ Accept user """

        path = f"/api/user/{username}/accept"
        return self.post(path)

    def get_status(self):
        """ Get application status """

        path = "/status"
        return self.get(path)


class VkMockClient(BaseApiClient):
    """ VkMock """

    def add_user(self, username, vk_id):
        """ Add user to Vk mock """

        path = f"/vk_id"
        payload = {"username": username, "vk_id": vk_id}
        return self.post(path, json=payload)
