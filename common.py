from base64 import b64decode, b64encode
from operator import itemgetter
import datetime
import time


def get_table_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(",") for element in lines]
    decoded_table = encode_decode_b64(table, "decode")
    decoded_table = timestamp_converter(decoded_table, "timestamp_to_datetime")
    return decoded_table


def write_table_to_file(table, file_name):
    encoded_table = encode_decode_b64(table, "encode")
    encoded_table = timestamp_converter(encoded_table, "datetime_to_timestamp")
    with open(file_name, "w") as file:
        for record in table:
            row = ','.join(record)
            file.write(row + "\n")


def ID_generator(table):
    IDs_in_table = [int(id_number[0]) for id_number in table]
    if not IDs_in_table:
        return str(1)
    else:
        return str(max(IDs_in_table) + 1)


def encode_decode_b64(table, method):
    if method == "decode":
        for element in table:
            for idx, item in enumerate(element):
                if idx == 4:
                    element[4] = b64decode(element[4]).decode("utf-8")
                if idx == 5:
                    element[5] = b64decode(element[5]).decode("utf-8")
                if idx == 6:
                    element[6] = b64decode(element[6]).decode("utf-8")
    if method == "encode":
        for element in table:
            for idx, item in enumerate(element):
                if idx == 4:
                    element[4] = b64encode(bytes(element[4], 'utf-8')).decode("utf-8")
                if idx == 5:
                    element[5] = b64encode(bytes(element[5], "utf-8")).decode("utf-8")
                if idx == 6:
                    element[6] = b64encode(bytes(element[6], "utf-8")).decode("utf-8")
    return table


def general_vote_up(element_id, database, vote_index):
    table = get_table_from_file(database)
    for element in table:
        if element[0] == element_id:
            element[vote_index] = int(element[vote_index])
            (element[vote_index]) += 1
            element[vote_index] = str(element[vote_index])
    write_table_to_file(table, database)


def general_vote_down(element_id, database, vote_index):
    table = get_table_from_file(database)
    for element in table:
        if element[0] == element_id:
            element[vote_index] = int(element[vote_index])
            (element[vote_index]) -= 1
            element[vote_index] = str(element[vote_index])
    write_table_to_file(table, database)


def sort_table(table_input, col, way):
    if int(col) in [7, 2, 3]:
        for element in table_input:
            table_input[table_input.index(element)][int(col)] = int(element[int(col)])
    table_input.sort(key=itemgetter(int(col)))
    if way == "desc":
        table_input.reverse()
    return table_input


def sort_table_answer(table_input, col, way):
    for element in table_input:
        table_input[table_input.index(element)][int(col)] = int(element[int(col)])
    table_input.sort(key=itemgetter(int(col)))
    if way == "desc":
        table_input.reverse()
    return table_input


def timestamp_converter(table, method):
    if method == "timestamp_to_datetime":
        for element in table:
            element[1] = datetime.datetime.fromtimestamp(int(element[1])).strftime('%Y-%m-%d %H:%M:%S')
    if method == "datetime_to_timestamp":
        for element in table:
            element[1] = str(time.mktime(datetime.datetime.strptime(element[1], '%Y-%m-%d %H:%M:%S').timetuple()))
            element[1] = element[1][0:-2]
    return table
