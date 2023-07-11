"""
String Utils Test
"""

import pytest

import text_utils as sut


@pytest.mark.parametrize(
    "source, max_length, expected",
    [
        ("string", 6, "string"),
        ("string", 7, "string"),
        ("string", 5, "st..."),
        ("string", 3, "..."),
    ],
)
def test_truncate_string(source, max_length, expected):
    assert sut.truncate_string(source, max_length) == expected


@pytest.mark.parametrize("source, max_length", [("", 0), ("", 1), ("string", 2)])
def test_truncate_string_raises_value_error(source, max_length):
    with pytest.raises(ValueError):
        sut.truncate_string(source, max_length)


def test_get_transitive_report_section_transitive_marker():
    report = "Some initial content. Transitive: Here is the transitive content."
    assert (
        sut.get_transitive_report_section(report) == ": Here is the transitive content."
    )


def test_get_transitive_report_section_transitive_marker_at_start():
    report = "Transitive: Here is the transitive content."
    assert (
        sut.get_transitive_report_section(report) == ": Here is the transitive content."
    )


def test_get_transitive_report_section_transitive_marker_at_end():
    report = "Some initial content. Transitive"
    assert sut.get_transitive_report_section(report) == ""


def test_get_transitive_report_section_transitive_marker_not_present():
    report = "Some initial content. No transitive marker present."
    assert sut.get_transitive_report_section(report) is None


def test_get_transitive_report_section_transitive_empty_string():
    report = ""
    assert sut.get_transitive_report_section(report) is None


def test_get_transitive_report_section_transitive_multiple_markers():
    report = "Transitive: First marker. Транзитив: Second marker."
    assert (
        sut.get_transitive_report_section(report)
        == ": First marker. Транзитив: Second marker."
    )


def test_get_transitive_report_section_transitive_other_language_marker():
    report = "Some initial content. Транзитив: Here is the transitive content."
    assert (
        sut.get_transitive_report_section(report) == ": Here is the transitive content."
    )


def test_get_transitive_dep_info_valid():
    report_line = "> Microsoft.NETCore.App 3.1.0"
    assert sut.get_transitive_dep_info(report_line) == (
        "Microsoft.NETCore.App",
        "3.1.0",
    )


def test_get_transitive_dep_info_invalid():
    report_line = "> Microsoft.NETCore.App"
    assert sut.get_transitive_dep_info(report_line) is None
