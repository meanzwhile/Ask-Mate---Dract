from base64 import b64decode, b64encode
from operator import itemgetter


def get_table_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(",") for element in lines]
    decoded_table = encode_decode_b64(table, "decode")
    return decoded_table


def write_table_to_file(table, file_name):
    encoded_table = encode_decode_b64(table, "encode")
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


def sort_table(table_input, col, way):
    table_input.sort(key=itemgetter(int(col)))
    if way == "desc":
        table_input.reverse()
    return table_input
