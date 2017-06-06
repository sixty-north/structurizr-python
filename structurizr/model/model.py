from orderedset import OrderedSet
from structurizr.model.component import Component
from structurizr.model.container import Container
from structurizr.model.enterprise import Enterprise
from structurizr.model.interaction_style import InteractionStyle
from structurizr.model.location import Location
from structurizr.model.person import Person
from structurizr.model.software_system import SoftwareSystem


class _SequentialIntegerGeneratorStrategy(object):

    def generate_id(self, software_system):
        pass

    def found(self, param):
        pass


class Model:

    def __init__(self):
        self._id_generator = _SequentialIntegerGeneratorStrategy()
        self._elements_by_id = {}
        self._relationships_by_id = {}
        self._enterprise = None
        self._people = OrderedSet()
        self._software_systems = OrderedSet()

    def get_enterprise(self):
        return self._enterprise

    def set_enterprise(self, enterprise):
        if not isinstance(enterprise, Enterprise):
            raise TypeError("{!r} is not an {}".format(enterprise, Enterprise.__name__))
        self._enterprise = enterprise

    def add_software_system(self, name, description, location=Location.UNSPECIFIED):
        if self.get_software_system_with_name(name) is not None:
            raise ValueError("A software system named {} already exists".format(name))
        software_system = SoftwareSystem()
        software_system.set_location(location)
        software_system.set_name(name)
        software_system.set_description(description)
        self._software_systems.add(software_system)
        software_system.set_id(self._id_generator.generate_id(software_system))
        self._add_element_to_internal_structures(software_system)
        return software_system

    def add_person(self, name, description, location=Location.UNSPECIFIED):
        if self.get_person_with_name(name) is not None:
            raise ValueError("A person named {} already exists".format(name))
        person = Person()
        person.set_location(location)
        person.set_name(name)
        person.set_description(description)
        self._people.add(person)
        person.set_id(self._id_generator.generate_id(person))
        self._add_element_to_internal_structures(person)
        return person

    def add_container(self, software_system, name, description, technology):
        if not isinstance(software_system, SoftwareSystem):
            raise TypeError("{} is not a {}".format(software_system, SoftwareSystem.__name__))
        if self.get_container_with_name(name) is not None:
            raise ValueError("A software system named {} already exists".format(name))
        container = Container()
        container.set_name(name)
        container.set_description(description)
        container.set_technology(technology)
        container.set_parent(software_system)
        software_system.add_existing_container(container)
        container.set_id(self._id_generator.generate_id(container))
        self._add_element_to_internal_structures(container)

    def add_component_of_type(self, container, name, type_name, description, technology):
        if not isinstance(container, Container):
            raise TypeError("{} is not a {}".format(container, Container.__name__))
        component = Component()
        component.set_name(name)
        component.set_type(type_name)
        component.set_description(description)
        component.set_technology(technology)
        component.set_parent(container)
        container.add_existing_component(component)
        component.set_id(self._id_generator.generate_id(component))
        self._add_element_to_internal_structures(component)

    def add_component(self, container, name, description):
        if not isinstance(container, Container):
            raise TypeError("{} is not a {}".format(container, Container.__name__))
        component = Component()
        component.set_name(name)
        component.set_description(description)
        component.set_parent(container)
        container.add_existing_component(component)
        component.set_id(self._id_generator.generate_id(component))
        self._add_element_to_internal_structures(component)

    def add_relationship(self, source, destination, description, technology=None, interaction_style=InteractionStyle.SYNCHRONOUS):
        relationship = Relationship(source, destination, description, technology, interaction_style)
        if self.add_existing_relationship(relationship):
            return relationship
        return None

    def add_existing_relationship(self, relationship):
        if not relationship.get_source().has(relationship):
            relationship.set_id(self._id_generator.generate_id(relationship))
            relationship.get_source().add_relationship(relationship)
            self._add_relationship_to_internal_structures(relationship)
            return True
        return False

    def _add_element_to_internal_structures(self, element):
        self._elements_by_id[element.get_id()] = element
        element.set_model(self)
        self._id_generator.found(element.get_id())

    def _add_relationship_to_internal_structures(self, relationship):
        self._relationships_by_id[relationship.get_id()] = relationship
        self._id_generator.found(relationship.get_id())

    def get_elements(self):
        return set(self._elements_by_id.values())  # TODO: Returning a copy again here?

    def get_element(self, id):
        return self._elements_by_id[id]

    def get_relationships(self):
        return set(self._relationships_by_id.values())

    def get_relationship(self, id):
        return self._relationships_by_id[id]

    def get_people(self):
        return self._people.copy()

    def get_software_systems(self):
        return self._software_systems.copy()

    # TODO: Omitting the hydrate stuff for now until I have a better understanding

    def contains(self, element):
        return element in self._elements_by_id.values()

    def get_software_system_with_name(self, name):
        return next((ss for ss in self._software_systems if ss.get_name() == name), None)

    def get_software_system_with_id(self, id):
        return next((ss for ss in self._software_systems if ss.get_id() == id), None)

    def get_person_with_name(self, name):
        return next((p for p in self._people if p.get_name() == name), None)

    def add_implicit_relationships(self):
        implicit_relationships = set()

        for relationship in self.get_relationships():
            source = relationship.get_source()
            destination = relationship.get_destination()

            while source != None:
                while destination != None:
                    if not source.has_efferent_relationships_with(destination):
                        if self._propagated_relationship_is_allowed(source, destination):
                            implicit_relationship = self.add_relationship(source, destination, "")
                            if implicit_relationship is not None:
                                implicit_relationship.add(implicit_relationship)
                    destination = destination.get_parent()
                destination = relationship.get_destination()
                source = source.get_parent()

        return implicit_relationships

    def _propagated_relationship_is_allowed(self, source, destination):
        if source == destination:
            return False

        if source.get_parent() is not None:
            if destination == source.get_parent():
                return False

            if source.get_parent().get_parent() is not None:
                if destination == source.get_parent().get_parent():
                    return False

        if destination.get_parent() is not None:
            if source == destination.get_parent():
                return False

            if destination.get_parent().get_parent() is not None:
                if source == destination.get_parent().get_parent():
                    return False

        return True

    def is_empty(self):
        return (len(self._people) != 0) or (len(self._software_systems) != 0)