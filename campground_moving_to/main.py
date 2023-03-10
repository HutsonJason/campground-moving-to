import csv


def main():
    due_in_report = "C:\\Users\\Jason\\Desktop\\camping report\\Due In Report.csv"
    due_out_report = "C:\\Users\\Jason\\Desktop\\camping report\\Due Out Report.csv"

    who_is_staying = get_who_is_staying(due_in_report, due_out_report)
    print(who_is_staying)


def get_who_is_staying(due_in: str, due_out: str) -> list[dict]:
    due_in_name_header = "txtdetailssmallfont-Name"
    due_in_site_header = "txtdetailssmallfont-unit_name"
    due_out_name_header = "txtdetails-Customer"
    due_out_site_header = "txtdetails-unit_name"
    due_in_list = []
    due_out_list = []
    staying_list = []

    with open(due_in, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            due_in_list.append(
                {
                    "Name": row[due_in_name_header],
                    "Site arriving": row[due_in_site_header],
                }
            )

    with open(due_out, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            due_out_list.append(
                {
                    "Name": row[due_out_name_header],
                    "Site leaving": row[due_out_site_header],
                }
            )

    for in_row in due_in_list:
        for out_row in due_out_list:
            if in_row["Name"] in out_row["Name"]:
                staying_list.append(
                    {
                        "Name": in_row["Name"],
                        "Site leaving": out_row["Site leaving"],
                        "Site arriving": in_row["Site arriving"],
                    }
                )

    return sorted(staying_list, key=lambda d: d["Site leaving"])


if __name__ == "__main__":
    main()
