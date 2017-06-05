import pytest


@pytest.fixture(scope="function")
def workspace():
    from structurizr import Workspace
    return Workspace("Name", "Description")

