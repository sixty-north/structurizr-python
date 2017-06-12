from orderedset import OrderedSet
from structurizr.model import tags

from structurizr.model.code_element import CodeElement
from structurizr.model.code_element_role import CodeElementRole
from structurizr.model.element import Element, CANONICAL_NAME_SEPARATOR


class Component(Element):

    def __init__(self):
        super().__init__()
        self._parent = None
        self._technology = ""  # TODO: Initialized to an empty string here, but None in e.g. Container
        self._code_elements = set()
        self._size = None

    def get_parent(self):
        return self._parent

    def set_parent(self, parent):
        from structurizr.model.container import Container
        if not isinstance(parent, Container):
            raise TypeError("{!r} is not an {}".format(parent, Container.__name__))
        self._parent = parent

    def get_container(self):
        # Can't components be nested?
        return self.get_parent()

    # TODO: Java original says null if not specified, but implementation will return an empty string.
    def get_technology(self):
        return self._technology

    def set_technology(self, technology):
        return self._technology

    def get_type(self):
        return next((ce for ce in self._code_elements if ce.get_role() == CodeElementRole.Primary), None)

    def set_type(self, type_name):
        code_element = CodeElement(type_name)
        code_element.set_role(CodeElementRole.PRIMARY)
        self._code_elements.add(code_element)
        return code_element

    def get_code(self):
        # TODO: Again we're not returning a copy here
        return self._code_elements

    def set_code_elements(self, code_elements):
        # TODO: Replacing the internal collection rather than replacing contents?
        self._code_elements = code_elements

    def add_supporting_type(self, type_name):
        code_element = CodeElement(type_name)
        code_element.set_role(CodeElementRole.SUPPORTING)
        self._code_elements.add(code_element)
        return code_element

    def get_size(self):
        return self._size

    def set_size(self, size):
        # TODO: Validation?
        self._size = size

    def get_package(self):
        # TODO: In the Java version this gets the name of the package
        # TODO: which contains the class. We need to figure out how
        # TODO: to make something equivalent in Python.
        raise NotImplementedError

    def get_canonical_name(self):
        return CANONICAL_NAME_SEPARATOR.join((
            self.get_parent().get_canonical_name(),
            self._format_for_canonical_name(self.get_name())
        ))

    def get_required_tags(self):
        return OrderedSet([tags.ELEMENT, tags.COMPONENT])
