import datetime

import requests

"""
openeo.sessions
~~~~~~~~~~~~~~~~
This module provides a Session object to manage and persist settings when interacting with the OpenEO API.
"""


class Session():

    def __init__(self,username, endpoint):
        self.username = username
        self.endpoint = endpoint


    @property
    #@abstractmethod
    def auth(self) -> str:
        pass

    def imagecollection(self, image_collection_id) -> 'ImageCollection':
        from .rest.imagecollection import RestImageCollection
        collection = RestImageCollection({'product_id': image_collection_id}, self)
        #TODO session should be used to retrieve collection metadata (containing bands)
        collection.bands = ["B0","B1","B2"]
        collection.dates = [datetime.datetime.now()]
        return collection

    def point_timeseries(self, graph, x, y, srs):
        """Compute a timeseries for a given point location."""
        return self.post("/v0.1/timeseries/point?x={}&y={}&srs={}".format(x,y,srs),graph)

    def post(self,path,postdata):
        return requests.post(self.endpoint+path,json=postdata)




def session(username=None,endpoint:str="https://openeo.org/endpoint"):
    """
    Returns a :class:`Session` for context-management.

    :rtype: Session
    """

    return Session(username,endpoint)