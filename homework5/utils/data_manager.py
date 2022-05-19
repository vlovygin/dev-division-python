import os
import random
import datetime
import faker
import uuid

from PIL import Image
from models.segment import SegmentRelationParamsType


class DataManager:

    def __init__(self, path):
        self.path = path
        self.fake = faker.Faker('ru_RU')

    @staticmethod
    def uuid():
        """Generate a random UUID"""

        return uuid.uuid4().hex

    @staticmethod
    def current_date(fmt="%Y-%m-%d"):
        """Current datetime with set format"""

        return datetime.datetime.today().strftime(fmt)

    def random_integer(self, start=-2147483648, end=2147483647):
        """Return random long int (int32) value"""

        return random.randint(start, end)

    def image(self, name=None, width=100, height=100, color=None):
        if name is None:
            name = self.fake.lexify('????????.png')

        path = os.path.join(self.path, name)

        img = Image.new('RGB', (width, height), color=color or self.fake.color())
        img.save(path)

        return img, path

    def campaign(self, package_id, objective, name=None, banners=None) -> dict:
        """Campaign data"""

        _campaign = dict()
        _campaign["name"] = name if name else f"Campaign name {self.uuid()}"

        _campaign["package_id"] = package_id
        _campaign["objective"] = objective

        if banners:
            if not isinstance(banners, list):
                banners = [banners]
            _campaign["banners"] = banners

        return _campaign

    def banner(self, primary_id=None, title_25=None, image_90x75_id=None, name=None):
        """Campaign banner"""

        _banner = dict()

        if primary_id:
            _banner["urls"] = {"primary": {"id": primary_id}}

        if title_25:
            _banner["textblocks"] = {"title_25": {"text": title_25}}

        if image_90x75_id:
            _banner["content"] = {"image_90x75": {"id": image_90x75_id}}

        if name:
            _banner["name"] = name

        return _banner

    def segment(self, name=None, pass_condition=None, relations=None, logic_type=None) -> dict:
        """Segment data"""

        _segment = dict()
        _segment["name"] = name if name else f"Segment name {self.uuid()}"

        if relations:
            if not isinstance(relations, list):
                relations = [relations]
            _segment["relations"] = relations

        if pass_condition:
            _segment["pass_condition"] = pass_condition
        else:
            _segment["pass_condition"] = self.random_integer(start=0, end=len(_segment["relations"]))

        if logic_type:
            _segment["logicType"] = logic_type

        return _segment

    def segment_relation(self, object_type, type_=None, right=None, left=None) -> dict:
        """Segment relation object"""

        _relation = dict()
        # Required param, because object_type affects to required params
        _relation["object_type"] = object_type

        _relation["params"] = dict()
        _relation["params"]["type"] = type_ if type_ else SegmentRelationParamsType.POSITIVE
        _relation["params"]["right"] = right if right else self.random_integer(start=0, end=365)
        _relation["params"]["left"] = left if left else self.random_integer(start=_relation["params"]["right"], end=365)

        return _relation
