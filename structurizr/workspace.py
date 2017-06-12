from abc import ABC, abstractmethod

from structurizr.model.element import is_well_formed_url
from structurizr.model.model import Model


class AbstractWorkspace(ABC):

    @abstractmethod
    def __init__(self, name, description):
        self._id = None
        self._description = description
        self._name = name
        self._version = None
        self._thumbnail = None
        self._source = None
        self._api = None

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

    def get_version(self):
        return self._version

    def set_version(self, version):
        self._version = version

    def get_thumbnail(self):
        return self._thumbnail

    def set_thumbnail(self, thumbnail):
        self._thumbnail = thumbnail

    def get_source(self):
        return self._source

    def set_source(self, url):
        if url and url.strip():
            if is_well_formed_url(url):
                self._source = url
            else:
                raise ValueError("{} is not a valid URL".format(url))

    def has_source(self):
        return self._source and self._source.strip()

    def get_api(self):
        return self._api

    def set_api(self, url):
        if url and url.strip():
            if is_well_formed_url(url):
                self._api = url
            else:
                raise ValueError("{} is not a valid URL".format(url))

    def has_api(self):
        return self._api and self._api.strip()


class Workspace(AbstractWorkspace):
    """A Structizr workspace.

    A wrapper for a software architecture model, views and documentation.
    """

    def __init__(self, name, description):
        super().__init__(name, description)
        self._model = Model()
        #self._view_set = ViewSet()
        #self._documentation = StructurizrDocumentation()

    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model



