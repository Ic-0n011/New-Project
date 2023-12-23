# import os
fielname = 'records.txt'


class Record:
    def __init__(self):
        self.old_records = []
        self.new_records = []

    def print_records(self):
        for record in self.old_records:
            print(f"Name: {record[name]}, Score: {record[score]}")

    def sort_records(self):
        self.old_records.sort(key=lambda x: int(x.split(' ')[1]), reverse=True)
        with open('records.txt', 'w') as file:
            for record in self.old_records[:10]:
                file.write(record + '\n')

    def update_record(self, name, score):
        pass


record_table = Record()
with open(fielname, 'r') as file:
    for record in file.readlines():
        name, score = record.split()
        record_table.new_records.append([name, score])
record_table.print_records()
print(record_table.old_records, " == ", record_table.new_records)
