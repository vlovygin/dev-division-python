import logging

import pytest
from requests import Response

from api.client import ApiClient
from models.segment import SegmentRelationObjectType
from utils.data_manager import DataManager


class BaseCase:
    """Base class for all tests"""

    @pytest.fixture(autouse=True)
    def setup_base(self, api_client, logger, app_config, tmp_path):
        """Setup for API testing"""

        self.api_client: ApiClient = api_client
        self.logger: logging.Logger = logger
        self.data_manager = DataManager(tmp_path)
        self.app_config: dict = app_config

    def create_new_segment(self) -> dict:
        """Create new segment"""

        relation = self.data_manager.segment_relation(object_type=SegmentRelationObjectType.REMARKETING_PLAYER)
        segment = self.data_manager.segment(relations=relation)
        response = self.api_client.create_segment(data=segment)
        response.raise_for_status()

        return response.json()

    def delete_campaign(self, id_campaign) -> Response:
        """Delete campaign"""

        response = self.api_client.delete_campaign(id_campaign)
        response.raise_for_status()

        return response
