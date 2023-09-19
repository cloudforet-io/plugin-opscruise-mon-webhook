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
        additional_info = load_yaml(text)

        results = []

        event_key = additional_info['Ticket ID']
        event_type = self._generate_event_type(additional_info.get('Header Message Type'))
        title = additional_info['Summary']
        description = self._generate_description(additional_info)
        severity = self._generate_severity(additional_info.get('Ticket Priority'))
        resource = self._generate_resource(additional_info)
        occurred_at = self._get_occurred_at(additional_info.get('Ticket Updated'))

        event_dict = {
            'event_key': event_key,
            'event_type': event_type,
            'title': title,
            'description': description,
            'severity': severity,
            'resource': resource,
            'occurred_at': occurred_at,
            'additional_info': self._change_string_value(additional_info)
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

    def _generate_description(self, additional_info):
        top_text = additional_info.get('Description', '')

        middle_descriptions = []
        custom_middle_description = {
            '대상': additional_info.get('Target Name', ''),
            '노드 이름': additional_info.get('Target Node', ''),
            '네임스페이스': additional_info.get('Target Namespace', ''),
            '파드 이름': additional_info.get('Target Pod', ''),
            '컨테이너 이름': additional_info.get('Target Container', ''),
        }
        for key, value in custom_middle_description.items():

            if value is None:
                value = ''

            middle_descriptions.append(f'{key}: {value}')

        bottom_descriptions = []
        custom_bottom_description = {
            '발생 시간': self._change_datetime_to_str(additional_info.get('Ticket Created')),
            '업데이트 시간': self._change_datetime_to_str(additional_info.get('Ticket Updated')),
            'Ticket URL': additional_info.get('Ticket URL', '')
        }
        for key, value in custom_bottom_description.items():
            bottom_descriptions.append(f'{key}: {value}')

        middle_text = '\n'.join(middle_descriptions)
        bottom_text = '\n'.join(bottom_descriptions)

        total_text = [top_text, middle_text, bottom_text]

        return '\n\n'.join(total_text)

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

    def _change_string_value(self, opscruise_data):
        additional_info = {}

        for key, value in opscruise_data.items():
            if isinstance(value, datetime):
                value = str(self._change_datetime_to_str(value))
            elif value is None:
                value = ''
            additional_info[key] = value

        return additional_info

    @staticmethod
    def _get_occurred_at(updated):
        if updated:
            return updated
        else:
            return datetime.now()

    @staticmethod
    def _change_datetime_to_str(time):
        return time.strftime('%Y-%m-%d %H:%M:%S')
