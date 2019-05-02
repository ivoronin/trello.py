"""Trello Client"""
from os import getenv
from furl import furl
import requests
from .board import Board
from .resource import ResourceCollection

class _Session(requests.Session):
    """Session with timeout"""
    def request(self, method, url, **kwargs): # pylint: disable=W0221
        if kwargs.get('timeout') is None:
            kwargs['timeout'] = 30
        return super().request(method, url, **kwargs)


class API:
    """Trello API"""
    def __init__(self, key=None, token=None):
        self._key = key
        self._token = token
        self._session = _Session()

    def _build_url(self, path_segments, params, version=1):
        url = furl('https://api.trello.com')
        url.path.segments = [version, *path_segments]
        url.args = {**{'key': self._key, 'token': self._token}, **(params or {})}
        return url.url

    def get_collection(self, cls, path_segments, params=None):
        """
        Get collection of resources

        Arguments:
            cls (class): Resourc class
            path_segments (list): URL path segments
            params (dict): Query parameters

        Returns:
            :class:`trello.resource.ResourceCollection`
        """
        response = self.make_request('GET', path_segments, params)
        json_objs = response.json()
        return ResourceCollection.from_json(cls, json_objs, self)

    def make_request(self, method, path_segments, params=None):
        """
        Make HTTP request

        Arguments:
            method (str): HTTP method
            path_segments (list): URL path segments
            params (dict, optional): Query parameters

        Returns:
            requests.Response
        """
        url = self._build_url(path_segments, params)
        response = self._session.request(method, url)
        response.raise_for_status()
        return response

    def close(self):
        """Close HTTP connections"""
        self._session.close()


class Client:
    """Trello client class"""
    def __init__(self, key=None, token=None):
        """
        Visit https://trello.com/app-key to get API key and token

        Args:
            key (str): Key
            token (str): Token
        Note:
            Uses **TRELLO_API_KEY** and **TRELLO_API_TOKEN** environment
            variables if **key** or **token** arguments are missing
        """
        api_key = key or getenv('TRELLO_API_KEY', None)
        if not api_key:
            raise Exception("TRELLO_API_KEY environment variable is missing")

        api_token = token or getenv('TRELLO_API_TOKEN', None)
        if not api_token:
            raise Exception("TRELLO_API_TOKEN environment variable is missing")

        self._api = API(api_key, api_token)

    def close(self):
        """Close HTTP connections"""
        self._api.close()

    def get_my_boards(self):
        """
        Get boards

        Returns:
            :class:`trello.ResourceCollection`: dict with board names
            as keys and :class:`trello.Board` instances as values
        """
        return self._api.get_collection(Board, ['members', 'me', 'boards'])
