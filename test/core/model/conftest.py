import pytest


@pytest.fixture()
def model(workspace):
    return workspace.get_model()


@pytest.fixture()
def views(workspace):
    return workspace.get_views()

