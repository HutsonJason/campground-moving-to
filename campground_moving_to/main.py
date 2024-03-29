import pandas as pd
import pandas.core.frame
import streamlit as st
import streamlit.runtime.uploaded_file_manager


def main():
    st.set_page_config(
        page_title="Campground Moving To",
        page_icon="⛺",
        menu_items={
            "About": "[GitHub Repository](https://github.com/HutsonJason/campground-moving-to)"
        },
    )
    st.title("⛺ Campground Moving To")
    with st.container():
        st.write("Upload the 'Due In Report.csv' and the 'Due Out Report.csv'.")
        st.write("It will return a table with who is staying, and on what sites.")

    if "file_state" not in st.session_state:
        st.session_state["file_state"] = False

    def change_due_in_state():
        """Changes streamlit file_state on change of file_uploader."""
        st.session_state["file_state"] = True

    with st.container():
        file_upload_list = st.file_uploader(
            label="Both can be uploaded at the same time by drag and drop, or clicking the box to open the file browser and selecting the files there.",
            type=["csv"],
            accept_multiple_files=True,
            on_change=change_due_in_state,
        )

    if st.session_state["file_state"]:
        # Update the status message.
        file_names_list = []
        for i in range(len(file_upload_list)):
            file_names_list.append(file_upload_list[i].name)
        get_file_status_message(file_names_list)
        file_status_message = get_file_status_message(file_names_list)
        match file_status_message[0]:
            case "error":
                st.error(file_status_message[1], icon="⚠️")
            case "success":
                st.success(file_status_message[1], icon="✔️")
            case "info":
                st.info(file_status_message[1], icon="ℹ️")
            case _:
                st.info(file_status_message[1], icon="ℹ️")

        if correct_files(file_names_list):
            if file_upload_list[0].name == "Due In Report.csv":
                due_in_df = get_due_in(file_upload_list[0])
                due_out_df = get_due_out(file_upload_list[1])
            else:
                due_in_df = get_due_in(file_upload_list[1])
                due_out_df = get_due_out(file_upload_list[0])

            combined_df = get_who_is_staying(due_in_df, due_out_df)
            with st.container():
                st.dataframe(data=combined_df, use_container_width=True)

    else:
        st.info("Please upload the Due In and Due Out Reports.", icon="ℹ️")

    with st.container():
        st.markdown(
            "[GitHub Repository](https://github.com/HutsonJason/campground-moving-to)"
        )
        st.markdown(
            "[Information on file uploads](https://docs.streamlit.io/knowledge-base/using-streamlit/where-file-uploader-store-when-deleted)"
        )


def get_due_in(
    due_in_csv: streamlit.runtime.uploaded_file_manager.UploadedFile,
) -> pandas.core.frame.DataFrame:
    """Gets a pandas dataframe of Due In Report.

    Takes the 'Due In Report.csv' that is retrieved as a streamlit file_uploader object
    (streamlit.runtime.uploaded_file_manager.UploadedFile) and converts it into a pandas dataframe.
    The dataframe is created using only the 'Name' column and 'Site arriving' column.
    These are titled on the csv as 'txtdetailssmallfont-Name' and 'txtdetailssmallfont-unit_name'.

    Args:
        due_in_csv: The 'Due In Report' csv file retrieved as a streamlit file_uploader object.

    Returns:
        A pandas dataframe with only the 'Name' column and 'Site arriving' column.
    """
    due_in_df = pd.read_csv(
        due_in_csv,
        usecols=["txtdetailssmallfont-Name", "txtdetailssmallfont-unit_name"],
    )
    return due_in_df.rename(
        columns={
            "txtdetailssmallfont-Name": "Name",
            "txtdetailssmallfont-unit_name": "Site arriving",
        },
    )


def get_due_out(
    due_out_csv: streamlit.runtime.uploaded_file_manager.UploadedFile,
) -> pandas.core.frame.DataFrame:
    """Gets a pandas dataframe of Due Out Report.

    Takes the 'Due Out Report.csv' that is retrieved as a streamlit file_uploader object
    (streamlit.runtime.uploaded_file_manager.UploadedFile) and converts it into a pandas dataframe.
    The dataframe is created using only the 'Name' column and 'Site leaving' column.
    These are titled on the csv as 'txtdetails-Customer' and 'txtdetails-unit_name'.

    Args:
        due_out_csv: The 'Due Out Report' csv file retrieved as a streamlit file_uploader object.

    Returns:
        A pandas dataframe with only the 'Name' column and 'Site leaving' column.
    """
    due_out_df = pd.read_csv(
        due_out_csv, usecols=["txtdetails-Customer", "txtdetails-unit_name"]
    )
    return due_out_df.rename(
        columns={"txtdetails-Customer": "Name", "txtdetails-unit_name": "Site leaving"}
    )


def get_who_is_staying(
    due_in_df: pandas.core.frame.DataFrame,
    due_out_df: pandas.core.frame.DataFrame,
) -> pandas.core.frame.DataFrame:
    """Creates a pandas dataframe of which customers are staying.

    Compares the 'Due Out Report' to the 'Due In Report' and merges the rows with the
    same customer names to a new dataframe. The new dataframe has a 'Name' column of the
    customer, a 'Site leaving' column with the site they are leaving from, and a 'Site arriving'
    column with the new site they are moving to. It also sorts the dataframe by 'Site leaving'.

    Args:
        due_in_df: The 'Due In Report' pandas dataframe.
        due_out_df: The 'Due Out Report' pandas dataframe.

    Returns:
        A merged pandas dataframe sorted by 'Site leaving' of the customers that are staying.
    """
    return (
        pd.merge(due_out_df, due_in_df, on=["Name"], how="inner")
        .sort_values(by=["Site leaving"])
        .set_index("Name")
    )


def get_file_status_message(file_names_list: list[str]) -> tuple[str, str]:
    """Gets the Streamlit message to display based on the uploaded files.

    Uses the length of the file_names_list to determine how many files were uploaded with streamlit file uploader.
    Runs a match case statement based on the number of files uploaded. The specific match it's looking for is 2.
    In the case of 2, the valid/success check is 1 file named 'Due In Report.csv' and 1 'Due Out Report.csv'.
    All other checks are for incorrect number of files and correct file names. A tuple is returned with a string
    value of the streamlit message type to use (error, success, info), and the message to display.

    Args:
        file_names_list: A list of strings of the names of the files uploaded with streamlit file uploader.

    Returns:
        A tuple with the specific streamlit message type to use, and the message to display.
    """
    match len(file_names_list):
        case 2:
            if file_names_list[0] == file_names_list[1]:
                return (
                    "error",
                    "Duplicate reports uploaded. Please upload 1 'Due In Report.csv' and 1 'Due Out Report.csv'",
                )
            for i in range(2):
                if not (
                    file_names_list[i] == "Due In Report.csv"
                    or file_names_list[i] == "Due Out Report.csv"
                ):
                    return (
                        "error",
                        "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
                    )
            return "success", "Found the correct files!"
        case 1:
            match file_names_list[0]:
                case "Due In Report.csv":
                    return "error", "'Due Out Report.csv' needs to be uploaded too."
                case "Due Out Report.csv":
                    return "error", "'Due In Report.csv' needs to be uploaded too."
                case _:
                    return (
                        "error",
                        "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
                    )
        case _ if len(file_names_list) > 2:
            return "error", "Too many files uploaded. Remove extras."
        case _:
            return "info", "Please upload the Due In and Due Out Reports."


def correct_files(file_names_list: list[str]) -> bool:
    """Checks if the correct files were uploaded.

    Checks the file names in the list to determine if the correct files were uploaded.
    It's only looking for 2 files, so the first check is to ensure that there are only 2.
    The next check is to ensure that the correct file names were uploaded ('Due In Report.csv'
    and 'Due Out Report.csv')

    Args:
        file_names_list: A list of strings of the names of the files uploaded with streamlit file uploader.

    Returns:
        A boolean (True) if correct files found, (False) if not.
    """
    if len(file_names_list) == 2:
        if (
            file_names_list[0] == "Due In Report.csv"
            and file_names_list[1] == "Due Out Report.csv"
        ):
            return True
        elif (
            file_names_list[0] == "Due Out Report.csv"
            and file_names_list[1] == "Due In Report.csv"
        ):
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    main()
