import pytest

from models.campaign import CampaignObjective, CampaignAdvFormat
from models.segment import SegmentRelationObjectType
from ui.base_case import BaseCase
from ui.page_objects import MainPage, CampaignNewPage
from ui.page_objects.segments_list_page import SegmentsListPage

pytestmark = pytest.mark.UI


class TestNegativeLogin(BaseCase):
    authorize = False

    def test_auth_with_invalid_login(self, user):
        """Authorization with invalid login"""

        invalid_login_redirect_url = self.app_config["login_url"]

        main_page = self.get_page(MainPage)
        page = main_page.login(self.data_manager.fake.email(), user.password)
        assert invalid_login_redirect_url in page.current_url, \
            f'User must be redirected to page {invalid_login_redirect_url}'

    def test_auth_with_invalid_password(self, user):
        """Authorization with invalid password"""

        invalid_login_redirect_url = self.app_config["login_url"]

        main_page = self.get_page(MainPage)
        page = main_page.login(user.login, self.data_manager.fake.password())
        assert invalid_login_redirect_url in page.current_url, \
            f'User must be redirected to page {invalid_login_redirect_url}'

    def test_auth_with_empty_login(self, user):
        """Authorization with empty login"""

        main_page = self.get_page(MainPage)
        main_page.login("", user.password)
        assert main_page.is_submit_login_button_disabled(), "Login button is active"

    def test_auth_with_empty_password(self, user):
        """Authorization with empty password"""

        main_page = self.get_page(MainPage)
        main_page.login(user.login, "")
        assert main_page.is_submit_login_button_disabled(), "Login button is active"


class TestCampaign(BaseCase):

    def test_campaign_create(self):
        """Create new reach campaign"""

        campaign_name = self.data_manager.uuid()

        campaign_new_page = self.get_page(CampaignNewPage)
        campaign_new_page.select_campaign_objective(CampaignObjective.REACH)
        campaign_new_page.set_objective_url("https://www.python.org/")
        campaign_new_page.set_campaign_name(campaign_name)
        campaign_new_page.set_budget_per_date("1000")
        campaign_new_page.set_budget_total("10000")
        campaign_new_page.select_adv_format(CampaignAdvFormat.TEASER)
        campaign_new_page.set_adv_title(self.data_manager.fake.bothify(text="????? ###"))
        campaign_new_page.set_adv_text(self.data_manager.fake.bothify(text="????? ?? ?? ?????? ??? ???? #########"))
        campaign_new_page.upload_adv_image(self.data_manager.image(width=100, height=100)[1])

        dashboard_page = campaign_new_page.submit_create_campaign()
        dashboard_page.search_campaign(campaign_name)
        assert campaign_name in dashboard_page.get_campaigns_list(), "Created campaign not found in campaigns list"


class TestSegment(BaseCase):

    def test_segment_delete(self):
        """Delete exists segment"""

        segment_name = self.data_manager.uuid()

        # create new segment
        relation = self.data_manager.segment_relation(object_type=SegmentRelationObjectType.REMARKETING_PLAYER)
        segment = self.data_manager.segment(name=segment_name, relations=relation)
        self.api_client.create_segment(data=segment).raise_for_status()

        segment_list_page = self.get_page(SegmentsListPage)
        segment_list_page.search_segment(segment_name)
        segment_list_page.delete_segment()

        assert not segment_list_page.get_segments_list(timeout=0), "Deleted segment found in segments list"
