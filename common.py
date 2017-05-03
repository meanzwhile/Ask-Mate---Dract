from base64 import encode, decode


def get_table_from_file(file_name="data/question.csv"):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(",") for element in lines]
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


def read_and_add_form_data():
    table = get_table_from_file()
    data_list = []
    data_list.insert(0, common.ID_generator(table))
    request_names = ['story-title', 'user-story', 'accept-crit',
                     'bussines-value', 'estimation', 'status']
    for name in request_names:
        data_list.append(request.form[name])
    cleared_data_list = common.clear_input(data_list)
    table.append(cleared_data_list)
    write_table_to_file(table)
