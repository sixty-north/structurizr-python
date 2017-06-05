class Enterprise:

    def __init__(self, name):
        if len(name.strip()) == 0:
            raise ValueError("Name must be specified.")

        self._name = name

    def get_name(self):
        return self._name
