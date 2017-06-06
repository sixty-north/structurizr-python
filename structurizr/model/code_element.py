from structurizr.model.code_element_role import CodeElementRole
from structurizr.model.element import is_well_formed_url


class CodeElement:

    def __init__(self, fully_qualified_name):
        if not fully_qualified_name:
            raise ValueError("A fully qualified name must be provided")

        self._name = fully_qualified_name.rsplit('.')[-1]
        self._type_name = fully_qualified_name
        self._role = CodeElementRole.SUPPORTING
        self._description = None
        self._url = None
        self._language = "Python"
        self._category = None
        self._visibility = None
        self._size = None

    def get_role(self):
        return self._role

    def set_role(self, role):
        self._role = role

    def get_name(self):
        return self._name

    def set_name(self, name):
        # TODO: Why doesn't this use the same logic as __init__?
        self._name = name

    def get_type(self):
        return self._type_name

    def set_type(self, type_name):
        self._type_name = type_name

    def get_description(self):
        return self._description

    def set_description(self, description):
        self._description = description

    # TODO: This method is duplicated from Element
    def get_url(self):
        return self._url

    # TODO: This method is duplicated from Element
    def set_url(self, url):
        if url and url.strip():
            if is_well_formed_url(url):
                self._url = url
            else:
                raise ValueError("{} is not a valid URL".format(url))

    def get_category(self):
        return self._category

    def set_category(self, category):
        self._category = category

    def get_visibility(self):
        return self._visibility

    def set_visibility(self, visibility):
        self._visibility = visibility

    def get_size(self):
        return self._size

    def set_size(self, size):
        self._size = size

    def __eq__(self, rhs):
        if self is rhs:
            return True

        if not isinstance(0, type(self)):
            return NotImplemented

        return self._type_name == rhs._type_name

    def __ne__(self, rhs):
        return not (self == rhs)

    def __hash__(self):
        return hash(self._type_name)
