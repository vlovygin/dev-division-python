import allure
import pytest

from ui.base_case import BaseTestUI
from ui.exceptions import PageNotLoadError
from ui.page_objects.dashbord_page import DashboardPage
from ui.page_objects.main_page import MainPage
from ui.page_objects.segments_list_page import SegmentsListPage
from utils.fake import random_uuid


class TestNegativeLogin(BaseTestUI):
    authorize = False

    def test_negative_login(self, negative_user):
        main_page = self.get_page(MainPage)
        with pytest.raises(PageNotLoadError):
            main_page.login(negative_user.login, negative_user.password)


class TestCampaign(BaseTestUI):

    @pytest.fixture()
    @allure.step("Create a new campaign")
    def create_new_campaign(self, request):
        campaign_name = random_uuid()
        upload_file = str(request.config.rootpath.joinpath("files", "art.jpg"))

        dashboard_page = self.get_page(DashboardPage)
        campaign_new_page = dashboard_page.navigate_to_new_campaign_create()
        campaign_new_page.create_reach_campaign(name=campaign_name, image_path=upload_file)

        return campaign_name

    def test_campaign_create(self, request):
        campaign_name = request.getfixturevalue("create_new_campaign")

        dashboard_page = self.get_page(DashboardPage, load=False)
        dashboard_page.search_campaign(campaign_name)
        assert campaign_name in dashboard_page.campaigns_name_list, "Created campaign not found in campaigns list"


class TestSegment(BaseTestUI):

    @pytest.fixture()
    def create_new_segment(self):
        segment_name = random_uuid()
        segments_page = self.get_page(SegmentsListPage)
        segment_new_page = segments_page.navigate_to_create_segment()
        segment_new_page.create_new_segment(name=segment_name)

        return segment_name

    def test_segment_create(self, request):
        segment_name = request.getfixturevalue("create_new_segment")

        segment_list_page = self.get_page(SegmentsListPage, load=False)
        segment_list_page.search_segment(segment_name)
        assert segment_name in segment_list_page.segments_name_list, "Created segment not found in segments list"

    def test_segment_delete(self, request):
        segment_name = request.getfixturevalue("create_new_segment")

        segment_list_page = self.get_page(SegmentsListPage, load=False)
        segment_list_page.search_segment(segment_name)
        segment_list_page.delete_segment()

        assert not segment_list_page.segments_name_list, "Deleted segment found in segments list"
