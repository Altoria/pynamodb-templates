from pynamodb.attributes import UnicodeAttribute
from pynamodb.constants import PAY_PER_REQUEST_BILLING_MODE

from pynamodb_templates.models import *
from .setup_dynamodb_local import *
from .test_attributes import *


class TimeTrackedTestModel(TimeTrackedModel):
    class Meta:
        host = "http://localhost:8000"
        table_name = "test"
        billing_mode = PAY_PER_REQUEST_BILLING_MODE

    hash = UnicodeULIDAttribute(hash_key=True, default=ULID)
    data = UnicodeAttribute(null=True)


class ModelUnittest(DynamodbLocalTest):
    PYNAMODB_MODEL = [
        TimeTrackedTestModel,
    ]

    def test_models(self):
        ulid = ULID()

        TimeTrackedTestModel(ulid).save()

        item = TimeTrackedTestModel.get(hash_key=ulid)

        # new record
        self.assertIn("created_at", item.attribute_values)
        self.assertIn("modified_at", item.attribute_values)
        self.assertNotIn("deleted_at", item.attribute_values)

        ititial_mod_time = item.modified_at

        item.update(actions=[TimeTrackedTestModel.data.set("Test DATA")])

        # check modified
        self.assertNotEqual(ititial_mod_time, item.modified_at)

        # check record exists
        items = [i for i in TimeTrackedTestModel.scan()]
        self.assertTrue(len(items) == 1, msg=str(items))

        item.delete(force=False)

        # check deleted
        self.assertIn("deleted_at", item.attribute_values)

        # check record deleted and filtered properly
        items = [i for i in TimeTrackedTestModel.scan()]
        self.assertTrue(len(items) == 0, msg=str(items))
