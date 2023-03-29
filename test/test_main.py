import pytest
import streamlit as st

from campground_moving_to.main import get_file_status_message


def test_get_file_status_message():
    file_names_list = ["Due Out Report.csv"]
    assert get_file_status_message(file_names_list) == (
        "error",
        "'Due Out Report.csv' needs to be uploaded too.",
    )
