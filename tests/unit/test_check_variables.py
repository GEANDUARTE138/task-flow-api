import pytest
from unittest.mock import patch
from shared.constants import check_variables


@pytest.mark.parametrize(
    "mocked_env_vars, should_raise",
    [
        (
            {
                "SERVICE_NAME": "Task Flow",
                "APP_ENV": "development",
                "PROJECT_ENV": "production",
            },
            False,
        ),
        (
            {"SERVICE_NAME": "", "APP_ENV": "development", "PROJECT_ENV": "production"},
            True,
        ),
        ({"SERVICE_NAME": "Task Flow", "APP_ENV": "", "PROJECT_ENV": ""}, True),
        ({"SERVICE_NAME": "", "APP_ENV": "", "PROJECT_ENV": ""}, True),
    ],
)
def test_check_variables(mocked_env_vars, should_raise):
    with patch.dict("os.environ", mocked_env_vars):
        if should_raise:
            with pytest.raises(OSError) as excinfo:
                check_variables()
            assert "please verify these variables without values" in str(excinfo.value)
        else:
            check_variables()
