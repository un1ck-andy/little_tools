import gspread


def main():
    # some hardcoded variables for this year
    spreadsheet = "2021-2022 3 курс цив процес"
    update_range = "U1:U33"
    groups = [  # are similar to worksheet names
        "18-19-02",
        "18-19-03",
        "18-19-04",
        "18-19-05",
        "04-19-12",
        "04-19-13",
    ]
    worksheet = []

    print("Let's calculate points for students")
    # authorization
    sa = gspread.service_account(filename="credentials.json")
    # open the google spreadsheet
    sh = sa.open(spreadsheet)

    # select the sheet
    while True:
        group = input("What group? (type 'all' for all groups): ")
        if group == "all":
            worksheet = groups
            break
        elif group in groups:
            worksheet.append(group)
            break
        else:
            print("Wrong group!")

    # do the cycle
    print("Working with the data...")
    for sheet in worksheet:
        wks = sh.worksheet(sheet)
        raw_list = calculate_points(wks)
        points_list = clean_points_list(raw_list)
        # update spreadsheet
        wks.batch_update([{"range": update_range, "values": points_list}])
        print(f"{sheet} was updated!")
    print("Job is done")


def calculate_points(wks: object) -> object:
    # get values
    values = wks.get_all_values()
    # count the points
    raw_list = []
    for row in values:
        points = 0
        for cell in row:
            if "онлайн" in cell:
                break
            elif not "+" in cell and not "." in cell:
                pass
            else:
                cell = cell.lower()
                if "н" in cell:
                    points += cell.count("+") * 3
                    points += cell.count(".") * 2
                else:
                    points += cell.count("+") * 5
                    points += cell.count(".") * 2
        raw_list.append(points)
    return raw_list


def clean_points_list(raw_list):
    # cleaning the list
    raw_list[0] = "TOTAL POINTS"
    raw_list[1] = ""
    raw_list.pop()
    raw_list.pop()
    return list(map(lambda el: [el], raw_list))


if __name__ == "__main__":
    main()
