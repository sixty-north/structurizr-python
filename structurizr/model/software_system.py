from orderedset import OrderedSet

from structurizr.model.element import Element, CANONICAL_NAME_SEPARATOR
from structurizr.model.location import Location


class SoftwareSystem(Element):

    def __init__(self):
        super().__init__()
        self._location = Location.UNSPECIFIED
        self._containers = OrderedSet()

    def get_parent(self):
        return None

    # TODO: This is duplicated in Person
    def get_location(self):
        return self._location

    # TODO: This is duplicated in Person
    def set_location(self, location):
        self._location = location if location is not None else Location.UNSPECIFIED

    def add_existing_container(self, container):
        self._containers.add(container)

    def get_containers(self):
        return self._containers.copy()

    def add_container(self, name, description, technology):
        return self.get_model().add_container(self, name, description, technology)

    def get_container_with_name(self, name):
        return next((c for c in self.get_containers() if c.get_name() == name), None)

    def get_container_with_id(self, id):
        return next((c for c in self.get_containers() if c.get_id() == id), None)

    # TODO: This is duplicated in Person
    def get_canonical_name(self):
        return CANONICAL_NAME_SEPARATOR + self._format_for_canonical_name(self.get_name())