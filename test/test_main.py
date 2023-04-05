from io import BytesIO

import pandas as pd
import pytest
from streamlit.runtime.uploaded_file_manager import UploadedFile, UploadedFileRec

from campground_moving_to.main import (
    correct_files,
    get_due_in,
    get_due_out,
    get_file_status_message,
)


class TestGetFileStatusMessage:
    def test_zero_file_names(self):
        """Test for 0 file names in list."""
        file_names_list = []
        assert get_file_status_message(file_names_list) == (
            "info",
            "Please upload the Due In and Due Out Reports.",
        )

    def test_one_file_name(self):
        """Test for 1 file name in list."""
        file_names_list = ["Due In Report.csv"]
        assert get_file_status_message(file_names_list) == (
            "error",
            "'Due Out Report.csv' needs to be uploaded too.",
        )
        file_names_list = ["Due Out Report.csv"]
        assert get_file_status_message(file_names_list) == (
            "error",
            "'Due In Report.csv' needs to be uploaded too.",
        )
        file_names_list = ["Wrong file.csv"]
        assert get_file_status_message(file_names_list) == (
            "error",
            "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
        )

    def test_two_file_names(self):
        """Test for 2 file names in list."""
        # Correct files.
        file_names_list = ["Due In Report.csv", "Due Out Report.csv"]
        assert get_file_status_message(file_names_list) == (
            "success",
            "Found the correct files!",
        )
        file_names_list = ["Due Out Report.csv", "Due In Report.csv"]
        assert get_file_status_message(file_names_list) == (
            "success",
            "Found the correct files!",
        )
        # Wrong file uploaded.
        file_names_list = ["Wrong file.csv", "Due In Report.csv"]
        assert get_file_status_message(file_names_list) == (
            "error",
            "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
        )
        file_names_list = ["Due In Report.csv", "Wrong file.csv"]
        assert get_file_status_message(file_names_list) == (
            "error",
            "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
        )
        file_names_list = ["Wrong file.csv", "Another wrong file.csv"]
        assert get_file_status_message(file_names_list) == (
            "error",
            "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
        )
        # Duplicate file uploaded.
        file_names_list = ["Due In Report.csv", "Due In Report.csv"]
        assert get_file_status_message(file_names_list) == (
            "error",
            "Duplicate reports uploaded. Please upload 1 'Due In Report.csv' and 1 'Due Out Report.csv'",
        )
        file_names_list = ["Due Out Report.csv", "Due Out Report.csv"]
        assert get_file_status_message(file_names_list) == (
            "error",
            "Duplicate reports uploaded. Please upload 1 'Due In Report.csv' and 1 'Due Out Report.csv'",
        )

    def test_more_than_two_file_names(self):
        """Check for more than 2 file names in list."""
        file_names_list = [
            "Due In Report.csv",
            "Due Out Report.csv",
            "Another report.csv",
        ]
        assert get_file_status_message(file_names_list) == (
            "error",
            "Too many files uploaded. Remove extras.",
        )


def test_correct_files():
    file_names_list = ["Due In Report.csv", "Due Out Report.csv"]
    assert correct_files(file_names_list)
    file_names_list = ["Due Out Report.csv", "Due In Report.csv"]
    assert correct_files(file_names_list)
    file_names_list = ["Due In Report.csv", "Due In Report.csv"]
    assert not correct_files(file_names_list)
    file_names_list = ["Wrong file.csv", "Due In Report.csv"]
    assert not correct_files(file_names_list)
    file_names_list = ["Due In Report.csv"]
    assert not correct_files(file_names_list)
    file_names_list = ["Due In Report.csv", "Due Out Report.csv", "Extra file.csv"]
    assert not correct_files(file_names_list)


@pytest.fixture()
def due_in_df():
    return pd.DataFrame(
        {
            "txtdetailssmallfont-Name": [
                "Michael Scott",
                "Dwight Schrute",
                "Jim Halpert",
            ],
            "txtdetailssmallfont-unit_name": [1, 2, 3],
        }
    )


@pytest.fixture()
def due_in_file(due_in_df):
    due_in_buff = BytesIO()
    due_in_df.to_csv(due_in_buff)
    due_in_buff.seek(0)
    due_in_file_rec = UploadedFileRec(
        1, "Due In Report.csv", "csv", due_in_buff.getvalue()
    )
    return UploadedFile(due_in_file_rec)


def test_get_due_in(due_in_df, due_in_file):
    df = due_in_df.rename(
        columns={
            "txtdetailssmallfont-Name": "Name",
            "txtdetailssmallfont-unit_name": "Site arriving",
        },
    )
    assert df.equals(get_due_in(due_in_file))


@pytest.fixture()
def due_out_df():
    return pd.DataFrame(
        {
            "txtdetails-Customer": [
                "Pam Beesly",
                "Stanley Hudson",
                "Kevin Malone",
            ],
            "txtdetails-unit_name": [10, 11, 12],
        }
    )


@pytest.fixture()
def due_out_file(due_out_df):
    due_out_buff = BytesIO()
    due_out_df.to_csv(due_out_buff)
    due_out_buff.seek(0)
    due_out_file_rec = UploadedFileRec(
        2, "Due Out Report.csv", "csv", due_out_buff.getvalue()
    )
    return UploadedFile(due_out_file_rec)


def test_get_due_out(due_out_df, due_out_file):
    df = due_out_df.rename(
        columns={
            "txtdetails-Customer": "Name",
            "txtdetails-unit_name": "Site leaving",
        },
    )
    assert df.equals(get_due_out(due_out_file))
