from csv import DictReader
import os
import grp
import pwd
import re
DEFAULT_SHELL = "/bin/bash"
SPECIAL_SHELL = "/bin/csh"


class User:
    def __init__(self, ID, Last_name, First_name, Office, Phone, Department, group):
        self.ID = ID
        self.user_name=""
        self.Last_name = Last_name
        self.First_name = First_name
        self.Office = Office
        self.Phone = Phone
        self.Department = Department
        self.group = group
	


def hasNumbers(inputString):
    return bool(re.search(r'\d',inputString))

def add_user(user):
    if hasNumbers(user.Department) or hasNumbers(user.Last_name) or hasNumbers(user.First_name) or user.Department=="" or user.Last_name=="" or user.First_name=='':
        os.system("echo 'BAD RECORD: EmployeeID= "+user.ID+"'")
        return
    shell = DEFAULT_SHELL
    os.system("sudo groupadd -f " + user.Department)
    if user.group == "office" or user.Department == "ceo":
        shell = SPECIAL_SHELL
    user_name = (user.First_name[0]+user.Last_name).lower()
    user_name= re.sub(r'[^a-zA-Z0-9_]',"",user_name)
    os.system("sudo mkdir -p /home/"+user.Department)
    i = 0
    actual_name= user_name
    while True:
        try:
            if i!=0: user_name=actual_name+str(i)
            pwd.getpwnam(user_name)
            i+=1
        except KeyError:
            os.system(
                "sudo useradd -m -d /home/" + user.Department + "/" + user_name + " -s " + shell + " -g " + user.Department + " -c " + '"' + user.First_name + "" + user.Last_name + '"' + " " + user_name)
            break
    passwd=user_name[::-1]
    os.system("echo " + passwd  + " |sudo passwd --stdin " + user_name)
    os.system(("sudo passwd -e " + user_name))


def main():
    user_list = []
    with open("Lab02_Users.csv", 'r') as read_obj:
        csv_dict_reader = DictReader(read_obj)
        for row in csv_dict_reader:
            user_list.append(User(row["EmployeeID"], row["LastName"], row["FirstName"], row["Office"], row["Phone"],
                                  row["Department"], row["Group"]))
    for user in user_list:

        add_user(user)


main()
