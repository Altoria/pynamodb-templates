import json
from pathlib import Path

from pynamodb.attributes import DynamicMapAttribute, ListAttribute
from pynamodb.constants import PAY_PER_REQUEST_BILLING_MODE
from ulid import ULID

from pynamodb_templates.attributes import *
from pynamodb_templates.models import TimeTrackedModel
from tests.setup_dynamodb_local import DynamodbLocalTest

parent = Path(__file__).resolve().parent


class TestModel(TimeTrackedModel):
    class Meta:
        host = "http://localhost:8000"
        table_name = "TestAttributeTable"
        billing_mode = PAY_PER_REQUEST_BILLING_MODE

    ulid = UnicodeULIDAttribute(hash_key=True, default_for_new=ULID)
    dict = DynamicMapAttribute()
    list = ListAttribute()


class ModelUnittest(DynamodbLocalTest):
    PYNAMODB_MODEL = [
        TestModel,
    ]

    def test_models(self):
        with open(parent / "test.json") as f:
            data = json.load(f)

        item = TestModel(dict=data, list=[1, 2, 3, 4])

        print(item.dict)

        self.assertEqual(data, json.loads(item.to_json())["dict"])


if __name__ == "__main__":
    with open(parent / "test.json") as f:
        j = json.load(f)
