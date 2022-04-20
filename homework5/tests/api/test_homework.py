import pytest
from api.base_case import BaseCase
from models.campaign import CampaignObjective
from models.segment import SegmentRelationObjectType

pytestmark = pytest.mark.API


class TestCampaignApi(BaseCase):

    def test_create_reach_campaign(self):
        """Тест на создание кампании через API, кампания после теста автоматически удаляется"""

        # upload file to static
        filepath = self.data_manager.image(width=90, height=75)[1]
        upload_static = self.api_client.upload_static_file(filepath)
        upload_static.raise_for_status()

        # prepare banner object
        banner = self.data_manager.banner(
            primary_id=30741099,  # Что за зверь?
            title_25=self.data_manager.fake.bothify(text="???? ##"),
            image_90x75_id=upload_static.json()['id']
        )

        campaign = self.data_manager.campaign(
            objective=CampaignObjective.REACH,
            package_id=1030,  # Не знаю как достать package_id смапенный на objective, поэтому хардкод package_id
            banners=banner
        )

        r = self.api_client.create_campaign(data=campaign, params={"fields": "id, name"})

        print(r.json())
        assert r.status_code == 200
        assert r.json()["id"], "Expected campaign id at response"
        assert r.json()["name"] == campaign["name"], f'Expected {campaign["name"]} campaign name'

        self.delete_campaign(id_campaign=r.json()["id"])


class TestSegmentApi(BaseCase):

    def test_create_new_segment(self):
        """Тест на создание сегмента через API и проверку что сегмент создан"""

        relation = self.data_manager.segment_relation(object_type=SegmentRelationObjectType.REMARKETING_PLAYER)
        segment = self.data_manager.segment(relations=relation)
        r = self.api_client.create_segment(data=segment, params={"fields": "id, name"})

        assert r.status_code == 200
        assert r.json()["id"], "Expected segment id at response for new segment"
        assert r.json()["name"] == segment["name"], f'Expected {segment["name"]} segment name'

    def test_delete_segment(self):
        """Тест на удаление сегмента"""

        created_segment = self.create_new_segment()
        r = self.api_client.delete_segment(created_segment["id"])

        assert r.status_code == 204
