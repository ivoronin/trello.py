"""Trello Card"""
import arrow
from .resource import Resource


class Card(Resource):
    """
    Card class

    Attributes:
        due (arrow.Arrow): Card due datetime or None
        last_activity (arrow.Arrow): Card last activity datetime or None
        due_complete (bool): Card due complete flag
    """
    _path = 'cards'

    _custom_field_value_constructors = {
        'text': str,
        'date': arrow.get,
        'number': int,
        'checkbox': bool,
        'list': list
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self._json['due']:
            self.due = arrow.get(self._json['due'])
        else:
            self.due = None

        if self._json['dateLastActivity']:
            self.last_activity = arrow.get(self._json['dateLastActivity'])
        else:
            self.last_activity = None

        self.due_complete = self._json.get('dueComplete', None)

    def get_custom_field(self, custom_field):
        """
        Returns custom_field value if its present or None.
        Return value type depends on custom field flavor:

        - text: str
        - date: arrow.Arrow
        - number: int
        - checkbox: bool
        - list: list

        Args:
            custom_field (:class:`trello.CustomField`): Custom field instance
        """
        items = self._json.get('customFieldItems')
        if not items:
            return None

        card_custom_field = next((i for i in items if i['idCustomField'] == custom_field.id), None)
        if card_custom_field is None:
            return None

        value_type, value_value = next(iter(card_custom_field['value'].items()))
        value = self._custom_field_value_constructors[value_type](value_value)
        return value


    def add_label(self, label):
        """
        Adds label

        Args:
            label (:class:`trello.Label`): Label to add
        """
        self._api.make_request('POST', f'cards/{self.id}/idLabels', {'value': label.id})

    def remove_label(self, label):
        """
        Removes label

        Args:
            label (:class:`trello.Label`): Label to remove
        """
        self._api.make_request('DELETE', f'cards/{self.id}/idLabels/{label.id}')

    def is_in_list(self, lst):
        """
        Returns True if card is in list

        Args:
            lst (:class:`trello.List`): Trello List
        Returns:
            bool
        """
        return self._json['idList'] == lst.id

    def has_label(self, label):
        """
        Returns True if card has label

        Args:
            lst (:class:`trello.Label`): Trello label
        Returns:
            bool
        """
        return next((True for c in self._json['labels'] if c['id'] == label.id), False)

    def move_to_list(self, target_list):
        """
        Moves card to the target list

        Args:
            target_list (:class:`trello.List`): Target list
        """
        self._api.make_request('PUT', f'cards/{self.id}', {'idList': target_list.id})
