import pytest


class TestWorkspace:

    @pytest.mark.xfail(reason="Not yet implemented")
    def test_set_source_does_not_throw_an_exception_when_a_none_url_is_specified(self, workspace):
        workspace.set_source(None)

    @pytest.mark.xfail(reason="Not yet implemented")
    def test_set_source_does_not_throw_an_exception_when_an_empty_url_is_specified(self, workspace):
        workspace.set_source("")
