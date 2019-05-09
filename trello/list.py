"""Trello List"""
from .resource import Resource
from .card import Card

class List(Resource):
    """List class"""
    _path = 'lists'

    def get_cards(self):
        """
        Returns:
            :class:`trello.ResourceCollection`: dict with card names
            as keys and :class:`trello.Card` instances as values
        """
        return self._get_child_collection(Card, {'customFieldItems': 'true'}).values()
