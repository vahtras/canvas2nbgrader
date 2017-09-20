#!/usr/bin/env python
"""Import student id from Canvas (Exported Grade table)"""
import sys
import csv

def get_records(csv_file):
    return list(csv.DictReader(csv_file))

def split_names(records):
    new = []
    for r in records:
        s = r['Student']
        if s == 'Studenttest' or s.strip() == 'Points Possible':
            pass
        else:
            last, first = r['Student'].split(', ')
            d = dict(first_name=first, last_name=last)
            new.append({**r, **d})
    return new

def out_dict(records):
    select = []
    for r in records:
        select.append(
            {
                'id': r["ID"],
                'first_name': r["first_name"],
                'last_name': r["last_name"],
                "email": r["SIS Login ID"],
            }
        )
    with open('students.csv', 'w') as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=["id", "first_name", "last_name", "email"]
        )
        writer.writeheader()
        for r in select:
            writer.writerow(r)

def main():
    try:
        csv_file = sys.argv[1]
    except IndexError:
        print("Usage: {} csv_file".format(sys.argv[0]))
        sys.exit(1)

    
    with open(csv_file) as f:
        #Remove BOM character in file
        lines = [line.replace('\ufeff', '') for line in f]
        records = split_names(get_records(lines))
 


    out_dict(records)

if __name__ == "__main__":
    sys.exit(main())
