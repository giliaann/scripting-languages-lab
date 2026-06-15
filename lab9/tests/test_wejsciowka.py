import pytest
from TimeSeries import TimeSeries

def test_get_item_type_error(create_time_series):
    ts = create_time_series()

    invalid_index = 'wrong'

    with pytest.raises(TypeError) as ex_info:
        _ = ts[invalid_index]
    
    assert f"Invalid index type: str" in str(ex_info.value)


