from orderedset import OrderedSet

from structurizr.model import tags
from structurizr.model.component import Component
from structurizr.model.element import Element, CANONICAL_NAME_SEPARATOR
from structurizr.model.software_system import SoftwareSystem


class Container(Element):

    def __init__(self):
        super().__init__()
        self._parent = None  # TODO: Can parent be hoisted into Element, or extracted into a Nestable ABC?
        self._technology = None
        self._components = OrderedSet()

    def get_parent(self):
        return self._parent

    # TODO: Argument (method, even) would be better named software_system
    def set_parent(self, parent):
        if not isinstance(parent, Component):
            raise TypeError("{!r} is not an {}".format(parent, SoftwareSystem.__name__))
        self._parent = parent

    def get_software_system(self):
        return self.get_parent()

    def get_technology(self):
        return self._technology

    def set_technology(self, technology):
        self._technology = technology

    def add_component(self, name, description, technology=None):
        c = self.get_model().add_component(self, name, description)
        c.set_technology(technology)
        return c

    def add_component_of_type(self, name, type_name, description, technology):
        return self.get_model().add_component_of_type(self, name, type_name, description, technology)

    def add_component_of_object(self, name, obj, description, technology):
        return self.get_model().add_component_of_type(self, name, obj, description, technology)

    def add_existing_component(self, component):
        if not isinstance(component, Component):
            raise TypeError("{!r} is not an {}".format(component, Component.__name__))
        # TODO: _components is a set, so we can't add it twice anyway, so isn't this check redundant
        # TODO: If Element.__hash__ was defined, we could probably do away with this check
        if self.get_component_with_name(component.get_name()) is None:
            self._components.add(component)

    def get_components(self):
        # TODO: Other similar methods return a copy of the collection, why not here?
        return self._components

    def get_component_with_name(self, name):
        return next((c for c in self.get_components() if c.get_name() == name), None)

    def get_component_of_type(self, type_name):
        return next((c for c in self.get_components() if c.get_type() == type_name), None)

    def get_canonical_name(self):
        return CANONICAL_NAME_SEPARATOR.join((
            self.get_parent().get_canonical_name(),
            self._format_for_canonical_name(self.get_name())))

    def get_required_tags(self):
        # TODO: Could chain this through the class hierachy using super(), so we don't need to mention tags.ELEMENT here
        return OrderedSet([tags.ELEMENT, tags.CONTAINER])
