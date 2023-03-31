from campground_moving_to.main import correct_files, get_file_status_message


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
