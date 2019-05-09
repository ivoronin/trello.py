"""Trello Resources"""
from orderedmultidict import omdict


class ResourceCollection(omdict): # pylint: disable=R0901
    """ResourceCollection class"""
    @classmethod
    def from_json(cls, resource_cls, objs_json, api):
        """
        Create resource collection from json array

        Args:
            resource_cls (class): Resource class
            objs_json (dict): JSON array
            client (:class:`trello.Client`): Client instance
        Returns:
            :class:`trello.ResourceCollection`
        """
        collection = cls()
        for obj_json in objs_json:
            obj = resource_cls(obj_json, api)
            collection.add(obj.name, obj)
        return collection


class Resource:
    """
    Abstract base resource class
    """
    def __init__(self, json, api):
        self._json = json
        self._api = api

    @property
    def id(self): # pylint: disable=C0103
        """str: Object id"""
        return self._json['id']

    @property
    def name(self):
        """str: Object name"""
        return self._json['name']

    def _get_child_collection(self, cls, params=None):
        path_segment = f'{self._path}/{self.id}/{cls._path}' # pylint: disable=E1101,W0212
        return self._api.get_collection(cls, path_segment, params)

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return NotImplemeted # pylint: disable=E0602
        return self.id == other.id
