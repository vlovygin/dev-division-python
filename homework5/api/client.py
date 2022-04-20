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
        return self._request(method="GET", path=path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        return self._request(method="POST", path=path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        return self._request(method="DELETE", path=path, *args, **kwargs)

    def _request_logging(self, response):
        """Report for request and response information"""

        response_dump = dump.dump_all(response)

        self.logger.info(response_dump)
        allure.attach(response.request.url, "Request URL", attachment_type=allure.attachment_type.URI_LIST)
        allure.attach(response_dump, f"Request dump", attachment_type=allure.attachment_type.JSON)

    def _request(self, method: str, path: str, *args, **kwargs):
        """Base request method for URLs based on base_url"""

        url = urljoin(self.base_url, path)

        response = self.session.request(method, url, *args, **kwargs)
        self._request_logging(response)

        return response

    def _custom_request(self, method: str, url, *args, **kwargs):
        """Custom request method for any URL"""

        response = self.session.request(method, url, *args, **kwargs)
        self._request_logging(response)

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

        response = self._custom_request("POST", url, data=data, headers=headers, allow_redirects=False)

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
