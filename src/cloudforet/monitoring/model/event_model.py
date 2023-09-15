from schematics.models import Model
from schematics.types import StringType, ModelType, DateTimeType


class OpsCruiseAdditionalInfo(Model):
    ticket_escalation = StringType(default='')
    instance_ip = StringType(default='')
    pod_name = StringType(default='')


class ResourceModel(Model):
    resource_type = StringType()
    name = StringType()


class EventModel(Model):
    event_key = StringType(required=True)
    event_type = StringType(choices=['RECOVERY', 'ALERT'], default='ALERT')
    title = StringType(required=True)
    description = StringType(default='')
    severity = StringType(choices=['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'NOT_AVAILABLE'], default=None)
    resource = ModelType(ResourceModel)
    rule = StringType(default='')
    occurred_at = DateTimeType()
    additional_info = ModelType(OpsCruiseAdditionalInfo)
    image_url = StringType(default='')
