from ip2geotools.databases.noncommercial import DbIpCity
import csv
import sys

"""
Phuong Anh Nguyen pn2075
"""


class AttemptError:
    def __init__(self, ip_address, location):
        self.ip_address = ip_address
        self.location = location
        self.count = 1


if len(sys.argv)<2:
    print("Usage: script4.py file_name")
    exit(1)
file_name = sys.argv[1]

try:
    f = open(file_name, "r")
    ip_dict = {}

    for line in f:
        get = False
        get_line = False
        for word in line.split():

            if word == "from":
                get = True
            elif word == "Failed":
                get_line = True
            else:
                if get & get_line:
                    if word in ip_dict:
                        attempt = ip_dict.get(word)
                        attempt.count += 1
                    else:
                        response = DbIpCity.get(word, "free")
                        attempt = AttemptError(word, response.country)
                        ip_dict[word] = attempt
                    get = False
                    get_line = False
    f.close()

    file = open("output.csv", 'w')
    writer = csv.writer(file)
    data = []
    writer.writerow(["Country", "IP", "Location"])
    for key, value in ip_dict.items():
        if value.count >= 10:
            writer.writerow([value.count, key, value.location])
    print('finish')
except FileNotFoundError:
    print(file_name+ " is not found")
    exit(1)
