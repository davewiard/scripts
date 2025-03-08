#!/usr/bin/env python3

import csv
import uuid

def read_data():
    lines = []
    with open('security_202412232225.csv', mode ='r') as file:
        csvFile = csv.reader(file)
        for line in csvFile:
            lines.append(line)

    return lines


def write_data(data):
    with open('security_202412230000.csv', mode = 'w') as file:
        for l in data:
            file.write(','.join(l))
            file.write('\n')


if __name__ == '__main__':
    data = read_data()

    first_line = True
    for l in data:
        if first_line:
            first_line = False
        else:
            l[1] = str(uuid.uuid4())

    write_data(data)
