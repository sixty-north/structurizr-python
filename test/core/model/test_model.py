import pytest


class TestModel:

    @pytest.mark.xfail(reason="Not yet implemented")
    def test_add_software_system_raises_a_value_error_when_an_empty_name_is_specified(self, model):
        with pytest.raises(ValueError):
            model.add_software_system(None, "")
