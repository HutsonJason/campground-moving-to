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
        # TODO Change the get status to accept tuple.
        get_file_status_message(file_names_list)

        # if len(file_upload_list) == 1:
        #     if file_upload_list[0].name == "Due In Report.csv":
        #         st.error("⚠️ 'Due Out Report.csv' needs to be uploaded too.")
        #     elif file_upload_list[0].name == "Due Out Report.csv":
        #         st.error("⚠️ 'Due In Report.csv' needs to be uploaded too.")
        #     else:
        #         st.error(
        #             "⚠️ Please only upload 'Due In Report.csv' or 'Due Out Report.csv'."
        #         )
        # elif len(file_upload_list) == 2:
        #     if file_upload_list[0].name == file_upload_list[1].name:
        #         st.error(
        #             "⚠️ Duplicate reports uploaded. Please upload 1 'Due In Report.csv' and 1 'Due Out Report.csv'"
        #         )
        #     for i in range(2):
        #         if (
        #             file_upload_list[i].name == "Due In Report.csv"
        #             or file_upload_list[i].name == "Due Out Report.csv"
        #         ):
        #             pass
        #         else:
        #             st.error(
        #                 "⚠️ Please only upload 'Due In Report.csv' or 'Due Out Report.csv'."
        #             )
        #     if (
        #         file_upload_list[0].name == "Due In Report.csv"
        #         and file_upload_list[1].name == "Due Out Report.csv"
        #     ):
        #         st.success("Found the correct files!")
        #         due_in_report = file_upload_list[0]
        #         due_out_report = file_upload_list[1]
        #         combined_df = get_who_is_staying(due_in_report, due_out_report)
        #         with st.container():
        #             st.dataframe(data=combined_df, use_container_width=True)
        #
        #     elif (
        #         file_upload_list[0].name == "Due Out Report.csv"
        #         and file_upload_list[1].name == "Due In Report.csv"
        #     ):
        #         st.success("Found the correct files!")
        #         due_in_report = file_upload_list[1]
        #         due_out_report = file_upload_list[0]
        #         combined_df = get_who_is_staying(due_in_report, due_out_report)
        #         with st.container():
        #             st.dataframe(data=combined_df, use_container_width=True)
        # elif len(file_upload_list) > 2:
        #     st.error("⚠️ Too many files uploaded. Remove extras.")

        match len(file_upload_list):
            case 2:
                if file_upload_list[0].name == file_upload_list[1].name:
                    ...

                for i in range(2):
                    if not (
                        file_upload_list[i].name == "Due In Report.csv"
                        or file_upload_list[i].name == "Due Out Report.csv"
                    ):
                        ...

                due_in_report = ""
                due_out_report = ""
                if file_upload_list[0].name == "Due In Report.csv":
                    due_in_report = file_upload_list[0]
                    due_out_report = file_upload_list[1]
                elif file_upload_list[1].name == "Due In Report.csv":
                    due_in_report = file_upload_list[1]
                    due_out_report = file_upload_list[0]

                # st.success("Found the correct files!")
                combined_df = get_who_is_staying(due_in_report, due_out_report)
                with st.container():
                    st.dataframe(data=combined_df, use_container_width=True)
            case 1:
                match file_upload_list[0]:
                    case "Due In Report.csv":
                        ...
                    case "Due Out Report.csv":
                        ...
                    case _:
                        ...
            case _ if len(file_upload_list) > 2:
                ...
            case _:
                ...
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
    due_in_df.rename(
        columns={
            "txtdetailssmallfont-Name": "Name",
            "txtdetailssmallfont-unit_name": "Site arriving",
        },
        inplace=True,
    )
    return due_in_df


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
    due_out_df.rename(
        columns={"txtdetails-Customer": "Name", "txtdetails-unit_name": "Site leaving"},
        inplace=True,
    )
    return due_out_df


def get_who_is_staying(
    due_in: streamlit.runtime.uploaded_file_manager.UploadedFile,
    due_out: streamlit.runtime.uploaded_file_manager.UploadedFile,
) -> pandas.core.frame.DataFrame:
    """
    Creates a pandas dataframe of which customers are staying.

    Compares the 'Due Out Report' to the 'Due In Report' and merges the rows with the
    same customer names to a new dataframe. The new dataframe has a 'Name' column of the
    customer, a 'Site leaving' column with the site they are leaving from, and a 'Site arriving'
    column with the new site they are moving to. It also sorts the dataframe by 'Site leaving'.

    Args:
        due_in: The 'Due In Report' csv file retrieved as a streamlit file_uploader object.
        due_out: The 'Due Out Report' csv file retrieved as a streamlit file_uploader object.

    Returns:
        A merged pandas dataframe sorted by 'Site leaving' of the customers that are staying.
    """
    due_in_df = get_due_in(due_in)
    due_out_df = get_due_out(due_out)

    return (
        pd.merge(due_out_df, due_in_df, on=["Name"], how="inner")
        .sort_values(by=["Site leaving"])
        .set_index("Name")
    )

    # def check_file_state(file_upload_list):
    ...


def get_file_status_message(file_names_list: list[str]) -> tuple[str, str]:
    match len(file_names_list):
        case 2:
            if file_names_list[0] == file_names_list[1]:
                return (
                    "error",
                    "Duplicate reports uploaded. Please upload 1 'Due In Report.csv' and 1 'Due Out Report.csv'",
                )
                # return st.error(
                #     "Duplicate reports uploaded. Please upload 1 'Due In Report.csv' and 1 'Due Out Report.csv'",
                #     icon="⚠️",
                # )

            for i in range(2):
                if not (
                    file_names_list[i] == "Due In Report.csv"
                    or file_names_list[i] == "Due Out Report.csv"
                ):
                    return (
                        "error",
                        "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
                    )
                    # return st.error(
                    #     "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
                    #     icon="⚠️",
                    # )

            return "success", "Found the correct files!"
            # return st.success("Found the correct files!", icon="✔️")
        case 1:
            match file_names_list[0]:
                case "Due In Report.csv":
                    return "error", "'Due Out Report.csv' needs to be uploaded too."
                    # return st.error(
                    #     "'Due Out Report.csv' needs to be uploaded too.", icon="⚠️"
                    # )
                case "Due Out Report.csv":
                    return "error", "'Due In Report.csv' needs to be uploaded too."
                    # return st.error(
                    #     "'Due In Report.csv' needs to be uploaded too.", icon="⚠️"
                    # )
                case _:
                    return (
                        "error",
                        "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
                    )
                    # return st.error(
                    #     "Please only upload 'Due In Report.csv' or 'Due Out Report.csv'.",
                    #     icon="⚠️",
                    # )
        case _ if len(file_names_list) > 2:
            return "error", "Too many files uploaded. Remove extras."
            # return st.error("Too many files uploaded. Remove extras.", icon="⚠️")
        case _:
            return "info", "Please upload the Due In and Due Out Reports."
            # return st.info("Please upload the Due In and Due Out Reports.", icon="ℹ️")


if __name__ == "__main__":
    main()
