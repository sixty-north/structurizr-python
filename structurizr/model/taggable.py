from abc import ABC, abstractmethod


class Taggable(ABC):

    def __init__(self):
        self._tags = set()  # TODO: This needs to be an OrderedSet

    @abstractmethod
    def get_required_tags(self):
        raise NotImplementedError

    def get_tags(self):
        """Gets the comma-separated list of tags.

        Returns: A comma separated list of tags, or an empty string if
            there are no tags.
        """
        return ','.join(self.get_required_tags() | self._tags)

    def set_tags(self, tags):
        """Sets from a comma-separated list of tags.
        """
        if tags is None:  # Weird, but for compatibility with the Java version
            return

        self._tags.clear()
        self._tags.update(tags.split(','))

    def add_tags(self, *tags):
        self._tags.update(tags)

    def remove_tag(self, tag):
        if tag:
            self._tags.remove(tag)

    def has_tag(self, tag):
        return tag in self._tags
