import logging
from spaceone.core.utils import load_yaml
from datetime import datetime
from spaceone.core.manager import BaseManager
from cloudforet.monitoring.model import EventModel

_LOGGER = logging.getLogger(__name__)


class EventManager(BaseManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, raw_data):
        text = raw_data.get('text')
        data = load_yaml(text)

        results = []

        event_key = data['Ticket ID']
        event_type = self._generate_event_type(data.get('Header Message Type'))
        title = data['Summary']
        description = data.get('Description')
        severity = self._generate_severity(data.get('Ticket Priority'))
        resource = self._generate_resource(data)
        additional_info = self._generate_additional_info(data)
        occurred_at = self._get_occurred_at(data.get('Ticket Updated'))

        event_dict = {
            'event_key': event_key,
            'event_type': event_type,
            'title': title,
            'description': description,
            'severity': severity,
            'resource': resource,
            'occurred_at': occurred_at,
            'additional_info': additional_info
        }

        event_result_model = EventModel(event_dict, strict=False)
        event_result_model.validate()
        event_vo = event_result_model.to_primitive()

        _LOGGER.debug(f'[EventManager] parse Event : {event_dict}')

        results.append(event_vo)

        return results

    @staticmethod
    def _generate_event_type(msg_type):
        if msg_type == 'Open':
            event_type = 'ALERT'
        elif msg_type == 'Resolved':
            event_type = 'RECOVERY'
        elif msg_type == 'Closed':
            event_type = 'RECOVERY'
        else:
            event_type = 'ALERT'
        return event_type

    @staticmethod
    def _generate_severity(priority):
        if priority == 'High':
            severity = 'CRITICAL'
        elif priority == 'Medium':
            severity = 'WARNING'
        elif priority == 'Low':
            severity = 'INFO'
        else:
            severity = 'NONE'
        return severity

    @staticmethod
    def _generate_resource(data):
        resource = {}

        if resource_type := data.get('Target Type'):
            resource['resource_type'] = resource_type

        if name := data.get('Target Name'):
            resource['name'] = name
        return resource

    @staticmethod
    def _generate_additional_info(data):
        additional_info = {}

        if ticket_escalation := data.get('Ticket Escalation'):
            additional_info['ticket_escalation'] = ticket_escalation
        if instance_ip := data.get('Target Node'):
            additional_info['instance_ip'] = instance_ip
        if pod_name := data.get('Target Pod'):
            additional_info['pod_name'] = pod_name

        return additional_info

    @staticmethod
    def _get_occurred_at(updated):
        if updated:
            return updated
        else:
            return datetime.now()
