import json
import logging
from urllib.parse import urljoin

import allure
import pytest
import requests
from requests_toolbelt.utils import dump

from config import app_config

logger = logging.getLogger("test")


class BaseApiClient:
    """Base class for API clients"""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.session()
        self.logger = logger

    def get(self, path, *args, **kwargs):
        return self.request(method="GET", path=path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self.request(method="POST", path=path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self.request(method="DELETE", path=path, *args, **kwargs)

    def request(self, method: str, path: str, *args, **kwargs):
        """Request method for URLs based on base_url"""

        url = urljoin(self.base_url, path)
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
        """Base request method"""

        req = requests.Request(method, url, *args, **kwargs)
        prepped = self.session.prepare_request(req)
        self._logging_pre(prepped)

        response = self.session.send(prepped, allow_redirects=allow_redirects, timeout=timeout)

        data = dump.dump_all(response)
        allure.attach(data, f"Request dump", attachment_type=allure.attachment_type.JSON)
        logger.info(f"Request dump: {data}")

        return response


class ApiClient(BaseApiClient):
    """Api client for myTarget"""

    @allure.step("Get csrf token")
    def get_csrf(self):
        """Get csrf token"""
        return self.get(path="/csrf")

    @allure.step("Authenticate by user")
    def auth(self, login, password):
        """Authenticate by user"""
        url = urljoin(app_config["auth_url"], "/auth")
        headers = {"Referer": self.base_url}

        data = {
            "email": login,
            "password": password,
            "continue": self.base_url
        }

        response = self._request("POST", url, data=data, headers=headers, allow_redirects=False)

        if not response.ok:
            pytest.fail(f"Authorization failed with [{response.status_code}]: {response.text}")

        # Save csrf token
        self.csrf_token = self.get_csrf().cookies['csrftoken']

        return response

    @allure.step("Create new campaign")
    def create_campaign(self, data, params=None):
        """Create new campaign"""

        path = "api/v2/campaigns.json"
        headers = {"X-CSRFToken": self.csrf_token}

        if not params:
            params = {
                "fields": "id,name,delivery,price,budget_limit,budget_limit_day,pads_ots_limits,created,issues,prices,"
                          "status,package_id,interface_read_only,read_only,objective,user_id,"
                          "targetings__split_audience,targetings__pads,enable_utm,utm,age_restrictions,"
                          "package_priced_event_type,autobidding_mode,pricelist_id"}

        response = self.post(path, json=data, params=params, headers=headers)
        return response

    @allure.step("Delete campaign")
    def delete_campaign(self, campaign_id):
        """Delete campaign"""

        path = f"/api/v2/campaigns/{campaign_id}.json"
        headers = {"X-CSRFToken": self.csrf_token}

        response = self.delete(path, headers=headers)
        return response

    @allure.step("Create new segment")
    def create_segment(self, data, params=None):
        """Create new segment"""

        path = "/api/v2/remarketing/segments.json"
        headers = {"X-CSRFToken": self.csrf_token}

        if not params:
            params = {
                "fields": "relations__object_type,relations__object_id,relations__params,relations__params__score,"
                          "relations__id,relations_count,id,name,pass_condition,created,campaign_ids,users,flags"}

        response = self.post(path, json=data, params=params, headers=headers)
        return response

    @allure.step("Delete segment")
    def delete_segment(self, segment_id):
        """Delete segment"""

        path = f"/api/v2/remarketing/segments/{segment_id}.json"
        headers = {"X-CSRFToken": self.csrf_token}

        response = self.delete(path, headers=headers)
        return response

    @allure.step("Upload static file")
    def upload_static_file(self, filepath):
        """Upload static file"""

        path = "/api/v2/content/static.json"
        headers = {"X-CSRFToken": self.csrf_token}

        with open(filepath, "rb") as f:
            response = self.post(path, files={"file": f}, headers=headers)

        return response
