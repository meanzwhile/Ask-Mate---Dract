def get_table_from_file(file_name="stories.csv"):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(";") for element in lines]
    return table


def write_table_to_file(table, file_name="stories.csv"):
    with open(file_name, "w") as file:
        for record in table:
            row = ';'.join(record)
            file.write(row + "\n")


def ID_generator(table):
    IDs_in_table = [int(id_number[0]) for id_number in table]
    if not IDs_in_table:
        return str(1)
    else:
        return str(max(IDs_in_table) + 1)