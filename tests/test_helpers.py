import pytest

from helpers import (
    get_message_id_from_id_or_url,
    prepare_text,
)


class TestGetMessageIdFromIdOrUrl:
    @pytest.mark.parametrize(
        "message_id_or_url, expected_message_id",
        (
            ("100500", 100500),
            ("https://discord.com/channels/644645112692867073/665817309478125583/856879535811067954", 856879535811067954),
            ("1", 1),
        )
    )
    def test_happy_path(self, message_id_or_url, expected_message_id):
        # act
        result = get_message_id_from_id_or_url(message_id_or_url)

        # assert
        assert result == expected_message_id

    @pytest.mark.parametrize(
        "message_id_or_url",
        (
            "foo",
            "https://discord.com/channels/644645112692867073/665817309478125583/856879535811067954/",
            "https://discord.com/channels/644645112692867073/665817309478125583/856879535dasdasd811067954",
            "123123sadasd15213",
            "",
        )
    )
    def test_contains_nondigits__raises_value_error(self, message_id_or_url):
        # act & assert
        with pytest.raises(ValueError):
            get_message_id_from_id_or_url(message_id_or_url)


@pytest.mark.parametrize(
    "source, expected",
    (
        ("Hello There", "hellothere"),
        ("123onetwothree4", "123onetwothree4"),
        (r"!@#$%^&*()", r"!#*"),  # unknown chars cleanup
        ("Why are we there? Just to suffer?", "whyarewethere?justto"),  # complex testcase
        ("1234567890123456789012345", "12345678901234567890"),  # over char limit
        ("12345", "12345"),  # lower than char limit
        ("12345678901234567890", "12345678901234567890"),  # equal to char limit
    )
)
def test_prepare_text(source, expected):
    # act
    result = prepare_text(source)

    # assert
    assert result == expected
