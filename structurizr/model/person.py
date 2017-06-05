from orderedset import OrderedSet

from structurizr.model import tags
from structurizr.model.element import Element, CANONICAL_NAME_SEPARATOR
from structurizr.model.location import Location


class Person(Element):

    def __init__(self):
        super().__init__()
        self._location = Location.UNSPECIFIED

    def get_parent(self):
        return None

    def get_location(self):
        return self._location

    def set_location(self, location):
        self._location = location if location is not None else Location.UNSPECIFIED

    def get_canonical_name(self):
        return CANONICAL_NAME_SEPARATOR + self._format_for_canonical_name(self.get_name())

    def get_required_tags(self):
        return OrderedSet(tags.ELEMENT, tags.PERSON)

    def delivers(self, destination, description, technology=None, interaction_style=None):
        # TODO: This is weird. The Java original raises UnsupportedOperationException for this override
        raise NotImplementedError

    def interacts_with(self, destination, description, technology=None, interaction_style=None):
        return self.get_model().add_relationship(destination, description, technology, interaction_style)
