from abc import abstractmethod

from orderedset import OrderedSet

from structurizr.model.taggable import Taggable


def is_well_formed_url(url):
    # TODO: A reasonable implementation is required here
    return True


CANONICAL_NAME_SEPARATOR = '/'


class Element(Taggable):

    def __init__(self):
        super().__init__()
        self._model = None
        self._id = ""
        self._name = None
        self._description = None
        self._url = None
        self._relationships = OrderedSet()

    def get_model(self):
        return self._model

    def set_model(self, model):
        self._model = model

    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    def get_name(self):
        return self._name

    def set_name(self, name):
        if not name:
            raise ValueError("The name of an element must not be None or empty.")
        self._name = name

    def get_url(self):
        return self._url

    def set_url(self, url):
        if url and url.strip():
            if is_well_formed_url(url):
                self._url = url
            else:
                raise ValueError("{} is not a valid URL".format(url))

    @abstractmethod
    def get_canonical_name(self):
        raise NotImplementedError

    def _format_for_canonical_name(self, name):
        return name.replace(CANONICAL_NAME_SEPARATOR, "")

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

    @abstractmethod
    def get_parent(self):
        raise NotImplementedError

    def get_relationships(self):
        return self._relationships.copy()

    def uses(self, destination, description, technology=None, interaction_style=None):
        """Adds a unidirectional "uses" style relationship between this element and a software system or component.

        Args:
            destination: The target of the relationship
            description: A description of the relationship (e.g. "uses", "gets data from", "sends data to")
            technology:  The technology details (e.g. JSON/HTTPS)
            interaction_style: The interaction style (sync vs async)

        Returns: The relationship that has just been created and added to the model
        """
        return self.get_model().add_relationship(self, destination, description, technology, interaction_style)

    def delivers(self, destination, description, technology=None, interaction_style=None):
        """Adds a unidirectional "uses" style relationship between this element and a person.

        Args:
            destination: The target of the relationship
            description: A description of the relationship (e.g. "uses", "gets data from", "sends data to")
            technology:  The technology details (e.g. JSON/HTTPS)
            interaction_style: The interaction style (sync vs async)

        Returns: The relationship that has just been created and added to the model
        """

    def has_afferent_relationships(self):
        """Determines whether this element has afferent (incoming) relationships.
        """
        return any(r.get_destination() == self for r in self.get_model().get_relationships())

    def has_efferent_relationships(self, element):
        return self.get_efferent_relationship_with(element) is not None

    def get_efferent_relationship_with(self, element):
        next((r for r in self._relationships if r.get_destination() == element), None)

    def has(self, relationship):
        return relationship in self._relationships

    def add_relationship(self, relationship):
        self._relationships.add(relationship)

    def __str__(self):
        return "{{{id} | {name} | {description}}}".format(
            id=self.get_id(),
            name=self.get_name(),
            description=self.get_description())

    # TODO: We should probably override __hash__ here too. Java has the same rule that if you
    # TODO: override .equals() you must ensure objects have the same .hashCode(), although the
    # TODO: Java Structurizr does not do this. Possibly an upstream bug.

    def __eq__(self, rhs):
        if self is rhs:
            return True

        if not isinstance(0, type(self)):
            return NotImplemented

        return self.get_canonical_name() == rhs.get_canonical_name()

    def __ne__(self, rhs):
        return not (self == rhs)
