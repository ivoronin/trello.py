"""Trello Board"""
from .resource import Resource
from .card import Card
from .list import List
from .label import Label
from .customfield import CustomField

class Board(Resource):
    """Board class"""
    _path = 'boards'

    def get_cards(self):
        """
        Get cards

        Returns:
            :class:`trello.ResourceCollection`: dict with card names
            as keys and :class:`trello.Card` instances as values
        """
        return self._get_child_collection(Card, params={'customFieldItems': 'true'}).values()

    def get_labels(self):
        """
        Get labels

        Returns:
            :class:`trello.ResourceCollection`: dict with label names
            as keys and :class:`trello.Label` instances as values
        """
        return self._get_child_collection(Label)

    def get_lists(self):
        """
        Get lists

        Returns:
            :class:`trello.ResourceCollection`: dict with list names
            as keys and :class:`trello.List` instances as values
        """
        return self._get_child_collection(List)

    def get_custom_fields(self):
        """
        Get custom fields

        Returns:
            :class:`trello.ResourceCollection`: dict with field names
            as keys and :class:`trello.CustomField` instances as values
        """
        return self._get_child_collection(CustomField)
