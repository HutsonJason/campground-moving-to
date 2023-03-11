import pandas as pd
import streamlit as st


def main():
    st.set_page_config(page_title="Campground Moving To", page_icon="⛺")
    st.title("⛺ Campground Moving To")
    with st.container():
        st.write("Upload the 'Due In Report.csv' and the 'Due Out Report.csv'.")
        st.write("It will return a table with who is staying, and on what sites.")

    if "file_state" not in st.session_state:
        st.session_state["file_state"] = False

    def change_due_in_state():
        st.session_state["file_state"] = True

    with st.container():
        file_upload_list = st.file_uploader(
            label="Both can be uploaded at the same time by drag and drop, or clicking the box to open the file browser and selecting the files there.",
            type=["csv"],
            accept_multiple_files=True,
            on_change=change_due_in_state,
        )

    if st.session_state["file_state"]:
        if len(file_upload_list) == 1:
            if file_upload_list[0].name == "Due In Report.csv":
                st.error("⚠️ 'Due Out Report.csv' needs to be uploaded too.")
            elif file_upload_list[0].name == "Due Out Report.csv":
                st.error("⚠️ 'Due In Report.csv' needs to be uploaded too.")
            else:
                st.error(
                    "⚠️ Please only upload 'Due In Report.csv' or 'Due Out Report.csv'."
                )
        elif len(file_upload_list) == 2:
            if file_upload_list[0].name == file_upload_list[1].name:
                st.error(
                    "⚠️ Duplicate reports uploaded. Please upload 1 'Due In Report.csv' and 1 'Due Out Report.csv'"
                )
            for i in range(2):
                if (
                    file_upload_list[i].name == "Due In Report.csv"
                    or file_upload_list[i].name == "Due Out Report.csv"
                ):
                    pass
                else:
                    st.error(
                        "⚠️ Please only upload 'Due In Report.csv' or 'Due Out Report.csv'."
                    )
            if (
                file_upload_list[0].name == "Due In Report.csv"
                and file_upload_list[1].name == "Due Out Report.csv"
            ):
                st.success("Found the correct files!")
                due_in_report = file_upload_list[0]
                due_out_report = file_upload_list[1]
                combined_df = get_who_is_staying(due_in_report, due_out_report)
                with st.container():
                    st.dataframe(data=combined_df, use_container_width=True)

            elif (
                file_upload_list[0].name == "Due Out Report.csv"
                and file_upload_list[1].name == "Due In Report.csv"
            ):
                st.success("Found the correct files!")
                due_in_report = file_upload_list[1]
                due_out_report = file_upload_list[0]
                combined_df = get_who_is_staying(due_in_report, due_out_report)
                with st.container():
                    st.dataframe(data=combined_df, use_container_width=True)
        elif len(file_upload_list) > 2:
            st.error("⚠️ Too many files uploaded. Remove extras.")
    else:
        st.info("Please upload the Due In and Due Out Reports.")


def get_due_in(due_in_csv):
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


def get_due_out(due_out_csv):
    due_out_df = pd.read_csv(
        due_out_csv, usecols=["txtdetails-Customer", "txtdetails-unit_name"]
    )
    due_out_df.rename(
        columns={"txtdetails-Customer": "Name", "txtdetails-unit_name": "Site leaving"},
        inplace=True,
    )
    return due_out_df


def get_who_is_staying(due_in, due_out):
    due_in_df = get_due_in(due_in)
    due_out_df = get_due_out(due_out)

    return (
        pd.merge(due_out_df, due_in_df, on=["Name"], how="inner")
        .sort_values(by=["Site leaving"])
        .set_index("Name")
    )


if __name__ == "__main__":
    main()
