import functools
from spaceone.core import utils
from spaceone.api.monitoring.plugin import event_pb2
from spaceone.core.pygrpc.message_type import *
from cloudforet.monitoring.model import EventModel

__all__ = ['EventInfo', 'EventsInfo']


def EventInfo(event_data: EventModel):
    info = {
        'event_key': event_data['event_key'],
        'event_type': event_data['event_type'],
        'title': event_data['title'],
        'description': event_data.get('description'),
        'severity': event_data['severity'],
        'resource': change_struct_type(event_data.get('resource')),
        'rule': event_data.get('rule'),
        'occurred_at': utils.datetime_to_iso8601(event_data.get('occurred_at')),
        'additional_info': change_struct_type(event_data.get('additional_info')),
        'image_url': event_data.get('image_url')
    }
    return event_pb2.EventInfo(**info)


def EventsInfo(event_Info_vos, **kwargs):
    return event_pb2.EventsInfo(results=list(map(functools.partial(EventInfo, **kwargs), event_Info_vos)))
