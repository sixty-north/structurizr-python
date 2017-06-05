import pytest


@pytest.fixture()
def workspace():
    from structurizr import Workspace
    return Workspace("Name", "Description")


@pytest.fixture()
def model(workspace):
    return workspace.get_model()


@pytest.fixture()
def views(workspace):
    return workspace.get_views()


class TestModel:

    def test_add_software_system_throws_an_exception_when_an_empty_name_is_specified(self, model):
        with pytest.raises(TypeError):
            model.add_software_system(None, "")
